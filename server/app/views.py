from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .utils import create_calendar

@api_view(["GET"])
def get_user_courses(request):
    # import time ; time.sleep(1)
    kerberos = request.GET.get("kerberos")
    if not kerberos:
        return Response("Kerberos not provided!", status=status.HTTP_400_BAD_REQUEST)
    if not UserData.objects.filter(kerberos=kerberos).exists():
        return Response("User not found!", status=status.HTTP_404_NOT_FOUND)
    user = UserData.objects.get(kerberos=kerberos)
    courses = user.user_courses.all()
    l = []
    for course in courses:
        l.append(course.courseCode)
    return Response({"name": user.name, "courses": l}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_user_timetable(request):

    kerberos = request.GET.get("kerberos")
    if not kerberos:
        return Response("Kerberos not provided!", status=status.HTTP_400_BAD_REQUEST)
    if not UserData.objects.filter(kerberos=kerberos).exists():
        return Response("User not found!", status=status.HTTP_404_NOT_FOUND)
    user = UserData.objects.get(kerberos=kerberos)
    courses = user.user_courses.all()

    days_map = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday"}
    l = []

    for course in courses:

        d = {
            "courseCode": course.courseCode,
            "slot": course.courseSlot.slot,
            "lecture": False,
            "tutorial": False,
            "lab": False,
            "lectureRoom": course.lectureRoom,
            "tutorialRoom": course.tutorialRoom,
        }
        creditStructure = course.creditStructure.split("-")
        if float(creditStructure[0]) != 0:
            d["lecture"] = True
        if float(creditStructure[1]) != 0:
            d["tutorial"] = True
        if float(creditStructure[2]) != 0:
            d["lab"] = True

        lectureTiming = []
        tutorialTiming = []

        if float(creditStructure[0]) != 0 and course.courseSlot.lectureTiming:
            lT = course.courseSlot.lectureTiming.split(",")
        else:
            lT = []
        day_list = list(days_map.values())
        for t in lT:
            day = days_map[int(t[0])]
            start = t[1:5]
            end = t[5:]
            lectureTiming.append({"day": day, "start": start, "end": end})
            day_list.remove(day)
        for day in day_list:
            lectureTiming.append({"day": day, "start": None, "end": None})

        d["lectureTiming"] = lectureTiming

        if float(creditStructure[1]) != 0 and course.courseSlot.tutorialTiming:
            tT = course.courseSlot.tutorialTiming.split(",")
        else:
            tT = []
        day_list = list(days_map.values())
        for t in tT:
            day = days_map[int(t[0])]
            start = t[1:5]
            end = t[5:]
            tutorialTiming.append({"day": day, "start": start, "end": end})
            day_list.remove(day)
        for day in day_list:
            tutorialTiming.append({"day": day, "start": None, "end": None})

        d["tutorialTiming"] = tutorialTiming

        if float(creditStructure[2]) != 0:
            labTiming = None
            d["labTiming"] = labTiming

        l.append(d)

    return Response({"name": user.name, "courses": l}, status=status.HTTP_200_OK)

@api_view(["POST"])
def generate_calendar(request):
    data = request.data
    cal = create_calendar.generate_calendar(data)
    return Response(cal.serialize(), status=status.HTTP_200_OK)