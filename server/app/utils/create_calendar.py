from ics import Calendar, Event
from datetime import timedelta
from ics.alarm import DisplayAlarm

working_days = {
    'Monday': ['0601', '1301', '2001', '2701', '0302', '1002', '1702', '0303', '1703', '2403', '0704', '1404', '2104', '2804'], 
    'Tuesday': ['0701', '2101', '2801', '0402', '1102', '1802', '0403', '1803', '2503', '0104', '0804', '1504', '2204', '1601'], 
    'Wednesday': ['0801', '1501', '2201', '2901', '1202', '1902', '0503', '1903', '2603', '0204', '0904', '1604', '2304'], 
    'Thursday': ['0201', '0901', '2301', '3001', '0602', '1302', '2002', '0603', '2003', '2703', '0304', '1704', '2404', '1204'], 
    'Friday': ['0301', '1001', '1701', '2401', '3101', '0702', '1402', '2802', '2103', '2803', '0404', '1104', '2504', '2604']
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
                        e.begin = f"2025-{date[2:]}-{date[:2]} {day['start'][:2]}:{day['start'][2:]}:00+05:30"
                        e.end = f"2025-{date[2:]}-{date[:2]} {day['end'][:2]}:{day['end'][2:]}:00+05:30"
                        e.alarms = [DisplayAlarm(trigger=timedelta(minutes=-10))]
                        e.description = "Powered by ClassGrid - DevClub IIT Delhi"
                        cal.events.add(e)

    return cal