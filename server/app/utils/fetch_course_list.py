from app.models import CourseList, SlotTiming, UserData
from .. import logs

import csv
import requests
from bs4 import BeautifulSoup

def isKerberos(kerberos):
    if len(kerberos) == 9 and kerberos[:2].isalpha() and kerberos[3:].isdigit():
        return True
    return False

def fetchCourseList(semesterCode):

    log_file = logs.create_new_log_file()

    url = "https://ldapweb.iitd.ac.in/LDAP/courses/%s-%s.shtml"
    
    with open("/Users/shashank/Shashank/GitHub/DevClub/ClassGrid/server/app/utils/Courses_Offered.csv", "r") as file:

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
                courseObj.students.clear() ; courseObj.save()
            else:
                courseObj = CourseList.objects.create(semesterCode=semesterCode, courseCode=courseCode, totalCredits=totalCredits, creditStructure=creditStructure, courseSlot=courseSlot)
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