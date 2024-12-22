#! Winter Semester, 2024-25

import datetime

semester_start_date = datetime.date(2025, 1, 2)
last_teaching_day = datetime.date(2025, 4, 28)

net_working_days = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": []}

### Generate all days in the semester excluding weekends

all_days = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": []}

for i in range((last_teaching_day - semester_start_date).days + 1):
    day = semester_start_date + datetime.timedelta(days=i)
    if day.weekday() > 4: continue
    all_days[day.strftime("%A")].append(day.strftime("%d%m"))

# print(all_days)

holidays = ["1401", "2601", "2602", "1403", "3103", "1004", "1804", "1205"]
no_class_days = ["0703", "2709"]
semester_break = ["1003", "1103", "1203", "1303", "1403", "1503", "1603"]
mid_sem = ["2102", "2202", "2302", "2402", "2502", "2602", "2702"]

substitutions = {
    "1601": "Tuesday",
    "1204": "Thursday",
    "2604": "Friday",
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

working_days = {'Monday': ['0601', '1301', '2001', '2701', '0302', '1002', '1702', '0303', '1703', '2403', '0704', '1404', '2104', '2804'], 'Tuesday': ['0701', '2101', '2801', '0402', '1102', '1802', '0403', '1803', '2503', '0104', '0804', '1504', '2204', '1601'], 'Wednesday': ['0801', '1501', '2201', '2901', '0502', '1202', '1902', '0503', '1903', '2603', '0204', '0904', '1604', '2304'], 'Thursday': ['0201', '0901', '2301', '3001', '0602', '1302', '2002', '0603', '2003', '2703', '0304', '1704', '2404', '1204'], 'Friday': ['0301', '1001', '1701', '2401', '3101', '0702', '1402', '2802', '2103', '2803', '0404', '1104', '2504', '2604']}