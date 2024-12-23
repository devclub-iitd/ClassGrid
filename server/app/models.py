from django.db import models

# Create your models here.

class UserData(models.Model):

    department = models.CharField(max_length=20)
    group = models.CharField(max_length=20)
    kerberos = models.CharField(max_length=20)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class SlotTiming(models.Model):
    
        slot = models.CharField(max_length=10, unique=True)
        lectureTiming = models.CharField(max_length=50, blank=True, null=True)
        tutorialTiming = models.CharField(max_length=50, blank=True, null=True)
        labTiming = models.CharField(max_length=50, blank=True, null=True)
        # Read NOTE #1 below on how to use the timings field.
    
        def __str__(self):
            return self.slot
    
class CourseList(models.Model):

    # TODO : Lecture Hall/Location of Class/Tutorial can be added as another field.

    semesterCode = models.CharField(max_length=10)
    courseCode = models.CharField(max_length=10)
    totalCredits = models.FloatField()
    creditStructure = models.CharField(max_length=100) # Format: "L-T-P" where L, T, P are floats.
    courseSlot = models.ForeignKey(SlotTiming, on_delete=models.CASCADE, related_name="course_slot")
    lectureRoom = models.CharField(max_length=50, blank=True, null=True)
    tutorialRoom = models.CharField(max_length=50, blank=True, null=True)
    labRoom = models.CharField(max_length=50, blank=True, null=True)
    overrideRoomChange = models.BooleanField(default=False)
    overrideSlotChange = models.BooleanField(default=False)
    students = models.ManyToManyField(UserData, blank=True, related_name="user_courses")

    def __str__(self):
        return f"{self.semesterCode}-{self.courseCode}"
    
class Notification(models.Model):
    
    semesterCode = models.CharField(max_length=10, default="2402")
    visibility = models.CharField(max_length=100)
    message = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self):
        if len(self.message) > 50:
            return self.message[:50] + "..."
        return self.message
    
'''
NOTE #1
Timings will be represented as comma separated values for multiple days. Each day will be represented by a 9-digit number with the following specifications:
First Digit - Represent the day (1 - Monday, 2 - Tuesday, 3 - Wednesday, 4 - Thursday, 5 - Friday)
Next 4 digits - Represent the starting time of the class in 24-hour format (0000 - 2359)
Last 4 digits - Represent the ending time of the class in 24-hour format (0000 - 2359)
All timings will be in IST.
Example: For A Slot, Lecture Timing will be represented as 108000930,408000930 which means the lecture will be held on Monday from 8:00 AM to 9:30 AM and on Thursday from 8:00 AM to 9:30 AM.

NOTE #2
Tutorials and Labs are held in cycles. The first cycle means "the group which will have the tutorial/lab on a Monday". It will be a single digit number from 1 to 4.
Example: For F Slot, Group 2 will have the tutorial on Monday. So, firstCycle will be 2.
Further, Group 3 will have the tutorial on Tuesday, Group 4 on Thursday, and Group 1 on Friday. There are no tutorials/labs on Wednesday. So, the cycle will repeat after 4 days.
'''