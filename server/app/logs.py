import os
import time
from django.conf import settings

def create_new_log_file():

    curr_time_in_unix = int(time.time())
    unix_to_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(curr_time_in_unix))

    with open(f"{settings.BASE_DIR}/logs/{curr_time_in_unix}.log", "w") as file:
        file.write(f"Log file created at {unix_to_date}\n")

    return curr_time_in_unix

def write_log(filename, message):

    if not os.path.exists(f"{settings.BASE_DIR}/logs/{filename}.log"):
        return False

    with open(f"{settings.BASE_DIR}/logs/{filename}.log", "a") as file:
        file.write(f"{message}\n")

    return True