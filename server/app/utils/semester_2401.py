#! Fall Semester, 2024-25

import datetime

semester_start_date = datetime.date(2024, 7, 22)
last_teaching_day = datetime.date(2024, 11, 14)

net_working_days = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": []}

### Generate all days in the semester excluding weekends

all_days = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": []}

for i in range((last_teaching_day - semester_start_date).days + 1):
    day = semester_start_date + datetime.timedelta(days=i)
    if day.weekday() > 4: continue
    all_days[day.strftime("%A")].append(day.strftime("%d%m"))

# print(all_days)

holidays = ["1707", "1508", "1908", "2608", "1609", "0210", "1210", "3110", "1511", "2512"]
no_class_days = ["1608", "2709"]
semester_break = ["0510", "0610", "0710", "0810", "0910", "1010", "1110", "1210", "1310"]
mid_sem = ["1209", "1309", "1409", "1509", "1609", "1709", "1809"]

substitutions = {
    "1308": "Thursday",
    "3108": "Monday",
    "1109": "Friday",
    "1910": "Wednesday",
    "2610": "Friday",
}

for day, dates in all_days.items():
    for date in dates:
        if (
            date not in holidays
            and date not in no_class_days
            and date not in semester_break
            and date not in mid_sem
            and date not in substitutions
        ):
            net_working_days[day].append(date)

for date, day in substitutions.items():
    net_working_days[day].append(date)

# print(net_working_days)
# print(len(net_working_days["Monday"]))
# print(len(net_working_days["Tuesday"]))
# print(len(net_working_days["Wednesday"]))
# print(len(net_working_days["Thursday"]))
# print(len(net_working_days["Friday"]))

woking_days = {'Monday': ['2207', '2907', '0508', '1208', '0209', '0909', '2309', '3009', '1410', '2110', '2810', '0411', '1111', '3108'], 'Tuesday': ['2307', '3007', '0608', '2008', '2708', '0309', '1009', '2409', '0110', '1510', '2210', '2910', '0511', '1211'], 'Wednesday': ['2407', '3107', '0708', '1408', '2108', '2808', '0409', '2509', '1610', '2310', '3010', '0611', '1311', '1910'], 'Thursday': ['2507', '0108', '0808', '2208', '2908', '0509', '1909', '2609', '0310', '1710', '2410', '0711', '1411', '1308'], 'Friday': ['2607', '0208', '0908', '2308', '3008', '0609', '2009', '0410', '1810', '2510', '0111', '0811', '1109', '2610']}