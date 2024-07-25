from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.get_user_courses, name='get_user_courses'),
    path('timetable/', views.get_user_timetable, name='get_user_timetable'),
    path('calendar/', views.generate_calendar, name='generate_calendar'),
    path('live/', views.live, name='live'),
    # path('name/', views.get_user_name, name='get_user_name'),
]