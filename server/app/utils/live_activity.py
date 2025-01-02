import re

from django.utils import timezone
from django.db.models import Q

from .create_calendar import working_days
from ..models import SlotTiming, CourseList, Notification

def get_active_slots(time):
    curr_year = str(time.year)
    curr_month = str(time.month).zfill(2)
    curr_day = str(time.day).zfill(2)
    curr_date = f"{curr_day}{curr_month}"

    timetable_day = None
    for day, dates in working_days.items():
        if curr_date in dates:
            timetable_day = day
            break

    if not timetable_day:
        return {
            "lecture": [],
            "tutorial": [],
            "lab": []
        }

    day_map = {
        "Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5
    }

    cg_time_string = f"{day_map[timetable_day]}{str(time.hour).zfill(2)}"

    slots = SlotTiming.objects.all()
    
    lecture_slots = set()
    tutorial_slots = set()
    lab_slots = set()

    for slot in slots:
        lt = slot.lectureTiming.split(",") if slot.lectureTiming else []
        tt = slot.tutorialTiming.split(",") if slot.tutorialTiming else []
        lbt = slot.labTiming.split(",") if slot.labTiming else []
        for t in lt:
            if t[0] == cg_time_string[0]:
                start_time = timezone.datetime(int(curr_year), int(curr_month), int(curr_day), int(t[1:3]), int(t[3:5]), 0)
                end_time = timezone.datetime(int(curr_year), int(curr_month), int(curr_day), int(t[5:7]), int(t[7:]), 0)
                if start_time <= time <= end_time:
                    lecture_slots.add(slot)
        for t in tt:
            if t[0] == cg_time_string[0]:
                start_time = timezone.datetime(int(curr_year), int(curr_month), int(curr_day), int(t[1:3]), int(t[3:5]), 0)
                end_time = timezone.datetime(int(curr_year), int(curr_month), int(curr_day), int(t[5:7]), int(t[7:]), 0)
                if start_time <= time <= end_time:
                    tutorial_slots.add(slot)
        for t in lbt:
            if t[0] == cg_time_string[0]:
                start_time = timezone.datetime(int(curr_year), int(curr_month), int(curr_day), int(t[1:3]), int(t[3:5]), 0)
                end_time = timezone.datetime(int(curr_year), int(curr_month), int(curr_day), int(t[5:7]), int(t[7:]), 0)
                if start_time <= time <= end_time:
                    lab_slots.add(slot)

    return {
        "lecture": list(lecture_slots),
        "tutorial": list(tutorial_slots),
        "lab": list(lab_slots)
    }

def get_all_lh():
    courses = CourseList.objects.filter(
        Q(lectureRoom__startswith="LH") | Q(tutorialRoom__startswith="LH") | Q(labRoom__startswith="LH")
    )
    lh_set = set()
    for course in courses:
        if course.lectureRoom:
            lectureRoomSplit = course.lectureRoom.split("/")
            for room in lectureRoomSplit:
                lh_set.add(room) if room.startswith("LH") and "." not in room else None
        if course.tutorialRoom:
            tutorialRoomSplit = course.tutorialRoom.split("/")
            for room in tutorialRoomSplit:
                lh_set.add(room) if room.startswith("LH") and "." not in room else None
        if course.labRoom:
            labRoomSplit = course.labRoom.split("/")
            for room in labRoomSplit:
                lh_set.add(room) if room.startswith("LH") and "." not in room else None

    return list(lh_set)

def get_free_lh(active_slots):
    # time = timezone.now() + timezone.timedelta(hours=5, minutes=30)
    # lecture_slots, tutorial_slots, lab_slots = get_active_slots(time)
    lecture_slots = active_slots["lecture"]
    tutorial_slots = active_slots["tutorial"]
    lab_slots = active_slots["lab"]

    lecture_halls = get_all_lh()

    lectures = CourseList.objects.filter(courseSlot__in=lecture_slots)
    tutorials = CourseList.objects.filter(courseSlot__in=tutorial_slots)
    labs = CourseList.objects.filter(courseSlot__in=lab_slots)

    for e in lectures:
        if e.lectureRoom:
            lectureRoomSplit = e.lectureRoom.split("/")
            for room in lectureRoomSplit:
                lecture_halls.remove(room) if room in lecture_halls else None
    for e in tutorials:
        if e.tutorialRoom:
            tutorialRoomSplit = e.tutorialRoom.split("/")
            for room in tutorialRoomSplit:
                lecture_halls.remove(room) if room in lecture_halls else None
    for e in labs:
        if e.labRoom:
            labRoomSplit = e.labRoom.split("/")
            for room in labRoomSplit:
                lecture_halls.remove(room) if room in lecture_halls else None

    return lecture_halls

def get_live_user_class(user, active_slots):

    courses = user.user_courses.filter(semesterCode="2402")
    
    lecture_slots = active_slots["lecture"]
    tutorial_slots = active_slots["tutorial"]
    lab_slots = active_slots["lab"]

    for course in courses:
        
        creditStructure = course.creditStructure.split("-")
        
        lectureCredits = float(creditStructure[0])
        tutorialCredits = float(creditStructure[1])
        labCredits = float(creditStructure[2])

        if course.courseSlot in lecture_slots and lectureCredits != 0:
            return course, "Lecture", course.lectureRoom
        if course.courseSlot in tutorial_slots and tutorialCredits != 0:
            return course, "Tutorial", course.tutorialRoom
        if course.courseSlot in lab_slots and labCredits != 0:
            return course, "Lab", course.labRoom
        
    return None, None, None

def get_user_notifs(user):

    courses = user.user_courses.filter(semesterCode="2402")
    l = []
    for course in courses:
        l.append(course.courseCode)

    notifs = Notification.objects.filter(semesterCode="2402").order_by("-added_at")
    res = []

    for notif in notifs:
        
        visibilities = notif.visibility.split(",")
        
        for v in visibilities:
            
            flag = False
            
            for course in l:
                if re.match(v, course):
                    res.append(notif.message)
                    flag = True
                    break

            if flag: break

    return res or None