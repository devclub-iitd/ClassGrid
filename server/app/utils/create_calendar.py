from ics import Calendar, Event
from datetime import timedelta
from ics.alarm import DisplayAlarm

working_days = {
    'Monday': ['2807', '0408', '1108', '1808', '2508', '0109', '0809', '2209', '0610', '1310', '2710', '0311', '1011', '2510'], 
    'Tuesday': ['2907', '0508', '1208', '1908', '2608', '0209', '0909', '2309', '0710', '1410', '2110', '2810', '0411', '1111'], 
    'Wednesday': ['3007', '0608', '1308', '2008', '2708', '0309', '1009', '2409', '0810', '1510', '2210', '2910', '1211', '0611'], 
    'Thursday': ['2407', '3107', '0708', '2108', '2808', '0409', '1109', '1809', '2509', '0910', '1610', '2310', '3010', '1311'], 
    'Friday': ['2507', '0108', '0808', '2208', '2908', '1909', '1010', '1710', '2410', '3110', '0711', '1411', '1408', '3008']
}

def generate_calendar(data):

    cal = Calendar()
    cal.creator = "ClassGrid - DevClub IIT Delhi"

    for course, content in data.items():
        for ltp, schedule in content.items():
            if schedule:
                for day in schedule:
                    dates = working_days[day['day']]
                    for date in dates:
                        e = Event()
                        e.name = f"{course.upper()} - {ltp.title()}"
                        try: e.location = day['room']
                        except: pass
                        # Change the years below as per current year. (2501) Labelled for identification. 
                        e.begin = f"2025-{date[2:]}-{date[:2]} {day['start'][:2]}:{day['start'][2:]}:00+05:30"
                        e.end = f"2025-{date[2:]}-{date[:2]} {day['end'][:2]}:{day['end'][2:]}:00+05:30"
                        e.alarms = [DisplayAlarm(trigger=timedelta(minutes=-10))]
                        e.description = "Powered by ClassGrid - DevClub IIT Delhi"
                        cal.events.add(e)

    return cal