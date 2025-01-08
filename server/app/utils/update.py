from django.conf import settings
import requests, time
from bs4 import BeautifulSoup
from .fetch_users import fetchUserData
from .fetch_course_list import fetchCourseList, fix_course_lh

requests.packages.urllib3.disable_warnings()

def check_room_allotment(curr_room_allotment):
    
    class_schedule_url = "https://timetable.iitd.ac.in/class-schedule"
    response = requests.get(class_schedule_url, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")
    for l in links:
        if "Room Allotment Chart for Semester II, 2024-25" in l:
            room_allotment = l
            break
    if room_allotment.get('href') == curr_room_allotment:
        return False, curr_room_allotment
    else:
        with open(f"{settings.BASE_DIR}/app/utils/Room Allotment.pdf", "wb") as file:
            response = requests.get(room_allotment.get('href'), verify=False)
            file.write(response.content)
        return True, room_allotment.get('href')
    
def check_course_update(last_course_update):
    course_list_url = "https://ldapweb.iitd.ac.in/LDAP/courses/"
    response = requests.get(course_list_url, verify=False)
    if response.status_code != 200:
        print("VPN not connected.")
        return False, last_course_update
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("tr")
    for l in links:
        if '2402-' in str(l):
            course_update = l
            break
    course_update = course_update.find_all("td", attrs={'align' : 'right'})[0].text
    if course_update == last_course_update:
        return False, course_update
    else:
        return True, course_update

def run():
    
    curr_room_allotment = "https://web.iitd.ac.in/~tti/timetable/Room_Allotment_Chart_2024_2025.pdf"
    last_course_update = "2025-01-08 02:26  "

    while True:

        course_update_needed, last_course_update = check_course_update(last_course_update)
        lh_update_needed, curr_room_allotment = check_room_allotment(curr_room_allotment)

        if course_update_needed:
            print("Course update is needed.")
            print("Refreshing user data.")
            fetchUserData()
            print("Refreshing course data.")
            fetchCourseList("2402")
        
        if lh_update_needed:
            print("LH update is needed.")
            fix_course_lh("2402")

        print("Update complete.")

        time.sleep(60*10) # Check every 10 minutes

