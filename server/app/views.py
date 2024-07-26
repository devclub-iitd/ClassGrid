from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from .models import *
from .utils import create_calendar, live_activity

@api_view(["GET"])
def get_user_courses(request):
    kerberos = request.kerberos
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
    kerberos = request.kerberos
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
    kerberos = request.kerberos
    if not kerberos:
        return Response("Kerberos not provided!", status=status.HTTP_400_BAD_REQUEST)
    if not UserData.objects.filter(kerberos=kerberos).exists():
        return Response("User not found!", status=status.HTTP_404_NOT_FOUND)
    data = request.data
    cal = create_calendar.generate_calendar(data)
    return Response(cal.serialize(), status=status.HTTP_200_OK)

@api_view(["GET"])
def live(request):
    kerberos = request.kerberos
    if not kerberos:
        return Response("Kerberos not provided!", status=status.HTTP_400_BAD_REQUEST)
    if not UserData.objects.filter(kerberos=kerberos).exists():
        return Response("User not found!", status=status.HTTP_404_NOT_FOUND)
    
    req_time = timezone.now() + timezone.timedelta(hours=5, minutes=30)
    req_time = req_time.replace(tzinfo=None)
    if req_time.second == 0:
        req_time = req_time.replace(second=1)
    w_day = f"{str(req_time.day).zfill(2)}{str(req_time.month).zfill(2)}"
    
    user = UserData.objects.get(kerberos=kerberos)

    active_slots = live_activity.get_active_slots(req_time)
    live_course, live_course_type, live_course_room = live_activity.get_live_user_class(user, active_slots)

    if req_time.hour < 19 and req_time.hour >= 8:
        for day, dates in create_calendar.working_days.items():
            if w_day in dates:
                free = live_activity.get_free_lh(active_slots) ; free = sorted(free)
                break
        else:
            free = None
    else: free = None

    if live_course:
        res = {
            "courseCode": live_course.courseCode,
            "courseType": live_course_type,
            "room": live_course_room
        }
    else: res = None

    return Response({"name": user.name, "free_lh": free, "live_course": res}, status=status.HTTP_200_OK)