from django.conf import settings
import requests, time
from bs4 import BeautifulSoup
from .fetch_users import fetchUserData
from .fetch_course_list import fetchCourseList, fix_course_lh

requests.packages.urllib3.disable_warnings()

def check_room_allotment():

    response = requests.get("https://web.iitd.ac.in/~tti/timetable/Room_Allotment_Chart_2025_2026_1.pdf", verify=False)
    if response.status_code != 200:
        return False
    
    if response.content == open(f"{settings.BASE_DIR}/app/utils/Room Allotment.pdf", "rb").read():
        return False
    
    with open(f"{settings.BASE_DIR}/app/utils/Room Allotment.pdf", "wb") as file:
        file.write(response.content)

    return True
    
def check_course_update(last_course_update):
    course_list_url = "http://internal.devclub.in/ldap/courses/"
    response = requests.get(course_list_url, verify=False, headers={'secret-key': settings.LDAP_KEY})
    if response.status_code != 200:
        print("VPN not connected.")
        return False, last_course_update
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("tr")
    for l in links:
        if '2501-' in str(l):
            course_update = l
            break
    course_update = course_update.find_all("td", attrs={'align' : 'right'})[0].text
    if course_update == last_course_update:
        return False, course_update
    else:
        return True, course_update

def run():

    last_course_update = ""

    while True:

        course_update_needed, last_course_update = check_course_update(last_course_update)
        lh_update_needed = check_room_allotment()

        if course_update_needed:
            print("Course update is needed.")
            print("Refreshing user data.")
            fetchUserData()
            print("Refreshing course data.")
            fetchCourseList("2501")
        
        if lh_update_needed:
            print("LH update is needed.")
            fix_course_lh("2501")

        print("Update complete.")

        time.sleep(60*10) # Check every 10 minutes

