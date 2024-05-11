from ics import Calendar, Event
from datetime import timedelta
from ics.alarm import DisplayAlarm

working_days = {
    'Monday': ['0101', '0801', '1501', '2901', '0502', '1202', '1103', '1803', '0104', '0804', '1504', '2204', '0604', '2604'], 
    'Tuesday': ['0201', '0901', '1601', '2301', '3001', '0602', '1302', '0503', '1903', '0204', '0904', '1604', '2304', '2704'], 
    'Wednesday': ['0301', '1001', '1701', '2401', '3101', '0702', '1402', '0603', '1303', '2003', '0304', '1004', '2404', '2004'], 
    'Thursday': ['0401', '1101', '1801', '2501', '0102', '0802', '1502', '0703', '1403', '2103', '0404', '1804', '2504', '1304'], 
    'Friday': ['0501', '1201', '1901', '0202', '0902', '1602', '1503', '2203', '0504', '1204', '1904', '2001', '0403', '1203']
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
                        e.begin = f"2024-{date[2:]}-{date[:2]} {day['start'][:2]}:{day['start'][2:]}:00+05:30"
                        e.end = f"2024-{date[2:]}-{date[:2]} {day['end'][:2]}:{day['end'][2:]}:00+05:30"
                        e.alarms = [DisplayAlarm(trigger=timedelta(minutes=-10))]
                        e.description = "Powered by ClassGrid - DevClub IIT Delhi"
                        cal.events.add(e)

    return cal