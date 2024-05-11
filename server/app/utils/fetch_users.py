from app.models import UserData
from .. import logs

import requests
from bs4 import BeautifulSoup

def fetchUserGroups():

    url = "https://ldapweb.iitd.ac.in/LDAP/dcs.html"
    response = requests.get(url, verify=False)

    if response.status_code != 200:
        return "Cannot connect to LDAP server!"

    soup = BeautifulSoup(response.text, "html.parser")
    departments = soup.find_all("a")

    user_groups = {}

    for dept in departments:

        dept_name = dept["href"].split("/")[0]

        url = f"https://ldapweb.iitd.ac.in/LDAP/{dept['href']}"
        response = requests.get(url, verify=False)

        if response.status_code != 200:
            return "Connection Lost!"

        soup = BeautifulSoup(response.text, "html.parser")
        groups = soup.find_all("a")

        for group in groups:
            group_name = group["href"].split(".")[0]
            if (len(group_name) == 5 and group_name[:2].isalpha() and group_name[3:].isdigit()) or group_name == "visiting_students":
                if dept_name not in user_groups:
                    user_groups[dept_name] = []
                if group_name not in user_groups[dept_name]:
                    user_groups[dept_name].append(group_name)

    return user_groups

def fetchUserData():

    log_file = logs.create_new_log_file()

    url = "https://ldapweb.iitd.ac.in/LDAP/%s/%s.shtml"
    
    user_groups = fetchUserGroups()
    if type(user_groups) == str:
        return user_groups
    
    all_users = UserData.objects.all()
    current_users = [user.kerberos for user in all_users]
    users_stack = current_users.copy()

    created = 0 ; deleted = 0

    for dept in user_groups:

        for group in user_groups[dept]:

            response = requests.get(url % (dept, group), verify=False)
            if response.status_code != 200:
                logs.write_log(log_file, f"ERROR: Connection Lost!")
                return "Connection Lost!"

            soup = BeautifulSoup(response.text, "html.parser")
            users = soup.find_all("tr")[1:]

            for user in users:
                kerberos = user.find_all("td")[0].text
                name = user.find_all("td")[1].text
                if kerberos not in current_users:
                    new_user = UserData(department=dept, group=group, kerberos=kerberos, name=name)
                    new_user.save() ; created += 1
                    logs.write_log(log_file, f"ACTION: {kerberos} - {name} created. ({dept}/{group})")
                else:
                    users_stack.remove(kerberos)

    for kerberos in users_stack:
        UserData.objects.filter(kerberos=kerberos).delete()
        deleted += 1
        logs.write_log(log_file, f"ACTION: {kerberos} deleted.")

    logs.write_log(log_file, f"Created: {created}, Deleted: {deleted}")

    return {'status': 200, 'message': "Users fetched successfully!", 'log_file': log_file}