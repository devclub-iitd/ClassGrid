from ics import Calendar, Event
from datetime import timedelta
from ics.alarm import DisplayAlarm

working_days = {
    'Monday': ['2207', '2907', '0508', '1208', '0209', '0909', '2309', '3009', '1410', '2110', '2810', '0411', '1111', '3108'], 
    'Tuesday': ['2307', '3007', '0608', '2008', '2708', '0309', '1009', '2409', '0110', '1510', '2210', '2910', '0511', '1211'], 
    'Wednesday': ['2407', '3107', '0708', '1408', '2108', '2808', '0409', '2509', '1610', '2310', '3010', '0611', '1311', '1910'], 
    'Thursday': ['2507', '0108', '0808', '2208', '2908', '0509', '1909', '2609', '0310', '1710', '2410', '0711', '1411', '1308'], 
    'Friday': ['2607', '0208', '0908', '2308', '3008', '0609', '2009', '0410', '1810', '2510', '0111', '0811', '1109', '2610']
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
                        e.begin = f"2024-{date[2:]}-{date[:2]} {day['start'][:2]}:{day['start'][2:]}:00+05:30"
                        e.end = f"2024-{date[2:]}-{date[:2]} {day['end'][:2]}:{day['end'][2:]}:00+05:30"
                        e.alarms = [DisplayAlarm(trigger=timedelta(minutes=-10))]
                        e.description = "Powered by ClassGrid - DevClub IIT Delhi"
                        cal.events.add(e)

    return cal