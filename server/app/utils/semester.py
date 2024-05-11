import datetime

start_date = datetime.date(2024, 2, 26)
end_date = datetime.date(2024, 2, 29)

current_date = start_date
l = []
while current_date <= end_date:
    # if current_date.weekday() == 4:  # Monday is represented by 0
    d = str(current_date).split("-")
    l.append(d[2] + d[1])
    current_date += datetime.timedelta(days=1)

# print(l)

all_days = {
    "Monday": [
        "0101",
        "0801",
        "1501",
        "2201",
        "2901",
        "0502",
        "1202",
        "1902",
        "2602",
        "0403",
        "1103",
        "1803",
        "2503",
        "0104",
        "0804",
        "1504",
        "2204",
    ],
    "Tuesday": [
        "0201",
        "0901",
        "1601",
        "2301",
        "3001",
        "0602",
        "1302",
        "2002",
        "2702",
        "0503",
        "1203",
        "1903",
        "2603",
        "0204",
        "0904",
        "1604",
        "2304",
    ],
    "Wednesday": [
        "0301",
        "1001",
        "1701",
        "2401",
        "3101",
        "0702",
        "1402",
        "2102",
        "2802",
        "0603",
        "1303",
        "2003",
        "2703",
        "0304",
        "1004",
        "1704",
        "2404",
    ],
    "Thursday": [
        "0401",
        "1101",
        "1801",
        "2501",
        "0102",
        "0802",
        "1502",
        "2202",
        "2902",
        "0703",
        "1403",
        "2103",
        "2803",
        "0404",
        "1104",
        "1804",
        "2504",
    ],
    "Friday": [
        "0501",
        "1201",
        "1901",
        "2601",
        "0202",
        "0902",
        "1602",
        "2302",
        "0103",
        "0803",
        "1503",
        "2203",
        "2903",
        "0504",
        "1204",
        "1904",
        "2604",
    ],
}

holidays = ["2601", "0803", "2503", "2903", "1104", "1704", "2104", "2305", "1706"]
no_class_days = ["2201", "2102", "2202", "2302", "0103"]
semester_break = [
    "2303",
    "2403",
    "2503",
    "2603",
    "2703",
    "2803",
    "2903",
    "3003",
    "3103",
]
mid_sem = ["1902", "2002", "2602", "2702", "2802", "2902"]

substituitions = {
    "2001": "Friday",
    "0403": "Friday",
    "1203": "Friday",
    "0604": "Monday",
    "1304": "Thursday",
    "2004": "Wednesday",
    "2604": "Monday",
    "2704": "Tuesday",
}

net_working_days = {
    "Monday": [],
    "Tuesday": [],
    "Wednesday": [],
    "Thursday": [],
    "Friday": [],
}
for day, dates in all_days.items():
    for date in dates:
        if (
            date not in holidays
            and date not in no_class_days
            and date not in semester_break
            and date not in mid_sem
            and date not in substituitions
        ):
            net_working_days[day].append(date)

for date, day in substituitions.items():
    net_working_days[day].append(date)

# print(net_working_days)
# print(len(net_working_days["Monday"]))
# print(len(net_working_days["Tuesday"]))
# print(len(net_working_days["Wednesday"]))
# print(len(net_working_days["Thursday"]))
# print(len(net_working_days["Friday"]))

working_days = {'Monday': ['0101', '0801', '1501', '2901', '0502', '1202', '1103', '1803', '0104', '0804', '1504', '2204', '0604', '2604'], 'Tuesday': ['0201', '0901', '1601', '2301', '3001', '0602', '1302', '0503', '1903', '0204', '0904', '1604', '2304', '2704'], 'Wednesday': ['0301', '1001', '1701', '2401', '3101', '0702', '1402', '0603', '1303', '2003', '0304', '1004', '2404', '2004'], 'Thursday': ['0401', '1101', '1801', '2501', '0102', '0802', '1502', '0703', '1403', '2103', '0404', '1804', '2504', '1304'], 'Friday': ['0501', '1201', '1901', '0202', '0902', '1602', '1503', '2203', '0504', '1204', '1904', '2001', '0403', '1203']}