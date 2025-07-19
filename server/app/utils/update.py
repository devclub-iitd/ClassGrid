from django.conf import settings
import requests
from bs4 import BeautifulSoup
from .fetch_users import fetchUserData
from .fetch_course_list import fetchCourseList, fix_course_lh

import boto3

requests.packages.urllib3.disable_warnings()

def check_room_allotment():

    return False

    # Room Allotment Chart not published for semester 2501

    response = requests.get("https://web.iitd.ac.in/~tti/timetable/Room_Allotment_Chart_2024_2025_2.pdf", verify=False)
    if response.status_code != 200:
        return False
    
    s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    
    try:
        if s3_client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key="Room Allotment.pdf")['Body'].read() == response.content:
            return False
    except s3_client.exceptions.NoSuchKey:
        pass

    s3_client.put_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key="Room Allotment.pdf", Body=response.content)

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

    try:
        last_course_update = open(f"{settings.BASE_DIR}/app/utils/last_update.txt", "r").read()
    except:
        last_course_update = "0"

    course_update_needed, last_course_update = check_course_update(last_course_update)
    lh_update_needed = check_room_allotment()

    if course_update_needed:
        print("Course update is needed.")
        print("Refreshing user data.")
        fetchUserData()
        print("Refreshing course data.")
        fetchCourseList("2402")
        with open(f"{settings.BASE_DIR}/app/utils/last_update.txt", "w") as file:
            file.write(last_course_update)
    
    if lh_update_needed:
        print("LH update is needed.")
        fix_course_lh("2402")

    print("Update complete.")

