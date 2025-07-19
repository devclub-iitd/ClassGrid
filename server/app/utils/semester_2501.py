#! Winter Semester, 2024-25

import datetime

semester_start_date = datetime.date(2025, 7, 24)
last_teaching_day = datetime.date(2025, 11, 14)

net_working_days = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": []}

### Generate all days in the semester excluding weekends

all_days = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": []}

for i in range((last_teaching_day - semester_start_date).days + 1):
    day = semester_start_date + datetime.timedelta(days=i)
    if day.weekday() > 4: continue
    all_days[day.strftime("%A")].append(day.strftime("%d%m"))

# print(all_days)

holidays = ["1508", "1608", "0509", "0210", "2010", "0511", "2411", "2512"]
no_class_days = ["2609", "2709"]
semester_break = ["2809", "2909", "3009", "0110", "0210", "0310", "0410", "0510"]
mid_sem = ["1209", "1309", "1409", "1509", "1609", "1709"]

substitutions = {
    "1408": "Friday",
    "3008": "Friday",
    "2510": "Monday",
    "0611": "Wednesday",
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

{'Monday': ['2807', '0408', '1108', '1808', '2508', '0109', '0809', '2209', '0610', '1310', '2710', '0311', '1011', '2510'], 'Tuesday': ['2907', '0508', '1208', '1908', '2608', '0209', '0909', '2309', '0710', '1410', '2110', '2810', '0411', '1111'], 'Wednesday': ['3007', '0608', '1308', '2008', '2708', '0309', '1009', '2409', '0810', '1510', '2210', '2910', '1211', '0611'], 'Thursday': ['2407', '3107', '0708', '2108', '2808', '0409', '1109', '1809', '2509', '0910', '1610', '2310', '3010', '1311'], 'Friday': ['2507', '0108', '0808', '2208', '2908', '1909', '1010', '1710', '2410', '3110', '0711', '1411', '1408', '3008']}