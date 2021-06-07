#! /usr/bin/env python3
from typing import Dict, List

import statistics

yeardata: Dict[int, List[float]] = dict()

century_prefix = 19
last_yy = 0

BASE_YEAR = 1880
END_YEAR = 2020
# starting 1880
sequencedata = []

with open('sea-level.txt', encoding='cp1252') as sl:
    next(sl) # skip first line
    for line in sl:
        line = line.strip()
        try:
            date_s, level_s = line.split()
        except ValueError:
            # assert False, line
            try:
                date_s, _, level_s = line.split()
            except ValueError:
                assert False, line
        if len(date_s) == 10:
            assert date_s[4] == '-', date_s
            assert date_s[7] == '-', date_s
            year = int(date_s[0:4])
            # month = int(date_s[5:7])
        else:
            mm, dd, yys = date_s.split('/')
            yy = int(yys)
            if yy < last_yy:
                century_prefix += 1
            year = century_prefix * 100 + yy
            last_yy = yy
        if year not in yeardata:
            yeardata[year] = []
        yeardata[year].append(float(level_s))

# print(yeardata[1880])
# print(yeardata[1890])
# print(yeardata[1909])
# # expect:
# # 1/15/09	-152.3140625				
# # 4/15/09	-146.3140625				
# # 7/15/09	-152.7807292				
# # 10/15/09	-148.6473958				
# print(yeardata[1900])
# print(yeardata[1999])
# print(yeardata[2000])
# print(yeardata[2001])

yearsequence = list(range(BASE_YEAR, END_YEAR + 1))

for i in range(BASE_YEAR, END_YEAR + 1):
    sequencedata.append(statistics.mean(yeardata[i]))

print(yearsequence)
print(sequencedata)
