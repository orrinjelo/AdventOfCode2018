#!/usr/bin/env python3
import os, sys
import datetime as dt
from pprint import pprint

# Pardon the ugliness

if __name__ == '__main__':
    # Parse args, parse list
    if len(sys.argv) <= 1:
        sys.exit('No filename given.  Answer: unknown')

    if len(sys.argv) > 2:
        sys.exit('Too many arguments.')

    print('Loading file: {}'.format(sys.argv[1]))
    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()

    lines = list(map(lambda x: str(x).strip(','), lines))

    # Parse data
    import re
    p = re.compile(r'\[(\d+)-(\d+)-(\d+)\s(\d+):(\d+)\]\s(.*)')

    def date_compare(s, t):
        if s[0] != t[0]:
            return int(s[0]) - int(t[0])
        if s[1] != t[1]:
            return int(s[1]) - int(t[1])
        return 0

    db = set()

    time_hack = dt.timedelta(hours=12) # Hacking time because I'm lazy

    # Parse each claim
    for line in lines:
        x = p.search(line)
        year, month, day, hour, minute, message = x.groups()
        entry = (dt.datetime(int(year), int(month), int(day),
            int(hour), int(minute)) + time_hack, message)
        db.add(entry)

    # And sort
    from operator import itemgetter
    sorted_db = sorted(db, key=itemgetter(0))

    # Parsing the messages - use a state machine
    import numpy as np

    # Guard schedules will be 
    guards = {}
    timesheet = {}

    # First field is the guard id
    # Second field can be 'unguarded', 'alert', or 'sleeping'
    pattern = re.compile(r'Guard #(\d+) begins shift')
    current_guard = None
    for entry in sorted_db:
        match = re.findall(pattern, entry[1])
        if match:
            current_guard = match[0]
            if not current_guard in guards:
                guards[current_guard] = 0
                timesheet[current_guard] = np.zeros((24, 60)).flatten()
        elif entry[1] == 'wakes up':
            wakey_time = entry[0]
            guards[current_guard] += (wakey_time - sleepy_time).seconds // 60
            timesheet[current_guard][(sleepy_time.hour * 60 + sleepy_time.minute):(wakey_time.hour * 60 + wakey_time.minute)] += 1
        elif entry[1] == 'falls asleep':
            sleepy_time = entry[0]

    sleepiest_minute = (0, None, 0)
    for guard in timesheet.keys():
        highest = int(np.max(timesheet[guard]))
        if sleepiest_minute[2] < highest:
            sleepiest_minute = (guard, np.where(timesheet[guard]==highest)[0][0], highest)

    print('Sleepiest guard: {}'.format(sleepiest_minute[0]))
    print('Sleepiest time: {}:{}'.format(sleepiest_minute[1]//60, sleepiest_minute[1]%60))
    print('Sleepiest frequency: {}'.format(sleepiest_minute[2]))
    print('Sleepy calculation: {}'.format(int(sleepiest_minute[0]) * (sleepiest_minute[1]%60)))