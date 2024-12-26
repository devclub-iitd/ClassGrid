from app.models import CourseList, SlotTiming, UserData
from .. import logs

import csv
import requests
from bs4 import BeautifulSoup

from .get_lh import get_room_number

def isKerberos(kerberos):
    if len(kerberos) == 9 and kerberos[:2].isalpha() and kerberos[3:].isdigit():
        return True
    return False

def fetchCourseList(semesterCode):

    log_file = logs.create_new_log_file()

    url = "https://ldapweb.iitd.ac.in/LDAP/courses/%s-%s.shtml"
    
    with open("/home/ubuntu/ClassGrid/server/app/utils/Courses_Offered.csv", "r") as file:

        reader = csv.reader(file)
        next(reader)

        occuranceCount = 0 ; lastCourse = None

        for row in reader:

            courseCode = row[1].split('-')[-1]
            if courseCode.endswith('P'):
                logs.write_log(log_file, f"ERROR: {courseCode} - Practical course detected. Requires manual intervention.")
                continue
            
            creditStructure = row[5]
            l_creditStructure = creditStructure.split('-')
            totalCredits = float(l_creditStructure[0]) + float(l_creditStructure[1]) + (float(l_creditStructure[2]) / 2)

            slot = row[3]
            if not SlotTiming.objects.filter(slot=slot).exists():
                SlotTiming.objects.create(slot=slot)
                logs.write_log(log_file, f"ACTION: Slot {slot} created.")
            courseSlot = SlotTiming.objects.get(slot=slot)

            lectureRoom, tutorialRoom, labRoom = None, None, None

            response = requests.get(url % (semesterCode, courseCode), verify=False)
            if response.status_code == 404 or lastCourse == courseCode[:6]:
                if lastCourse == courseCode[:6]:
                    occuranceCount += 1
                else:
                    occuranceCount = 1 ; lastCourse = courseCode[:6]
                courseCode = lastCourse + chr(64+occuranceCount)
                response = requests.get(url % (semesterCode, courseCode), verify=False)
                if response.status_code == 404:
                    logs.write_log(log_file, f"ERROR: {courseCode} - Could not fetch course.")
                    continue
            else:
                occuranceCount = 1 ; lastCourse = courseCode[:6]

            soup = BeautifulSoup(response.text, "html.parser")
            students = soup.find_all("td", attrs={'align' : 'LEFT'})
            l = len(students)
            if CourseList.objects.filter(semesterCode=semesterCode, courseCode=courseCode).exists():
                courseObj = CourseList.objects.get(semesterCode=semesterCode, courseCode=courseCode)
                if not courseObj.overrideSlotChange:
                    courseObj.courseSlot = courseSlot
                courseObj.students.clear() ; courseObj.save()
            else:
                lectureRoom = get_room_number(f"{courseCode}", "L")
                tutorialRoom = get_room_number(f"{courseCode}", "T")
                courseObj = CourseList.objects.create(semesterCode=semesterCode, courseCode=courseCode, totalCredits=totalCredits, creditStructure=creditStructure, courseSlot=courseSlot, lectureRoom=lectureRoom, tutorialRoom=tutorialRoom, labRoom=labRoom)
            for student in students:
                if not isKerberos(student.text):
                    l -= 1
                else:
                    try:
                        student = UserData.objects.get(kerberos=student.text)
                    except UserData.DoesNotExist:
                        logs.write_log(log_file, f"ERROR: User with kerberos {student.text} not found in the database. Not added to course {courseCode}.")
                        continue
                    courseObj.students.add(student)
            courseObj.save()
            logs.write_log(log_file, f"UPDATE: {l} students added to {courseCode}.")

    return {'status': 200, 'message': 'Course list fetched successfully.', 'log_file': log_file}

def manualFetchCourse(url, saveToID):

    if not CourseList.objects.filter(id=saveToID).exists():
        return {'status': 404, 'message': f"Course with ID {saveToID} not found."}
    
    response = requests.get(url, verify=False)
    if response.status_code == 404:
        return {'status': 404, 'message': 'URL not found.'}

    soup = BeautifulSoup(response.text, "html.parser")
    students = soup.find_all("td", attrs={'align' : 'LEFT'})
    l = len(students)
    courseObj = CourseList.objects.get(id=saveToID)
    courseObj.students.clear() ; courseObj.save()
    for student in students:
        if not isKerberos(student.text): l -= 1
        else:
            try:
                student = UserData.objects.get(kerberos=student.text)
            except UserData.DoesNotExist:
                continue
            courseObj.students.add(student)
    courseObj.save()
    return {'status': 200, 'message': f"{l} students added to {courseObj.courseCode}."}

def createEmptyCourse(semesterCode, courseCode, creditStructure, slot):

    if CourseList.objects.filter(semesterCode=semesterCode, courseCode=courseCode).exists():
        return {'status': 409, 'message': f"Course {courseCode} already exists in semester {semesterCode}."}

    if SlotTiming.objects.filter(slot=slot).exists():
        courseSlot = SlotTiming.objects.get(slot=slot)
    else:
        courseSlot = SlotTiming.objects.create(slot=slot)

    totalCredits = 0
    l_creditStructure = creditStructure.split('-')
    totalCredits = float(l_creditStructure[0]) + float(l_creditStructure[1]) + (float(l_creditStructure[2]) / 2)
    
    course = CourseList.objects.create(semesterCode=semesterCode, courseCode=courseCode, totalCredits=totalCredits, creditStructure=creditStructure, courseSlot=courseSlot)

    return {'status': 201, 'course_id': course.id}

def fix_course_lh(semesterCode):
    
    log_file = logs.create_new_log_file()

    courses = CourseList.objects.filter(semesterCode=semesterCode, overrideRoomChange=False).order_by('courseCode')
    for course in courses:
        course.lectureRoom = get_room_number(f"{course.courseCode}", "L")
        course.tutorialRoom = get_room_number(f"{course.courseCode}", "T")
        course.save()
        logs.write_log(log_file, f"UPDATE: Course {course.courseCode} updated.")
    return {'status': 200, 'message': 'Course locations updated.'}