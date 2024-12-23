from django.contrib import admin
from .models import *

# Register your models here.

class UserDataAdmin(admin.ModelAdmin):
    list_display = ('kerberos', 'name')
    search_fields = ('kerberos', 'name')
    ordering = ('department', 'group', 'kerberos')

class CourseListAdmin(admin.ModelAdmin):
    list_display = ('semesterCode', 'courseCode', 'courseSlot', 'lectureRoom', 'tutorialRoom')
    search_fields = ('courseCode',)
    ordering = ('-semesterCode', 'courseCode', 'courseSlot')
    list_filter = ('overrideRoomChange', 'overrideSlotChange')

admin.site.register(UserData, UserDataAdmin)
admin.site.register(SlotTiming)
admin.site.register(CourseList, CourseListAdmin)
admin.site.register(Notification)