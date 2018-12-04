#!/usr/bin/env python3
import os, sys

if __name__ == '__main__':
    # Parse args, parse list
    if len(sys.argv) <= 1:
        sys.exit('No entries given.  Answer: unknown')

    if len(sys.argv) == 2:
        print('Loading file: {}'.format(sys.argv[1]))
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    else:
        lines = sys.argv[1:]

    lines = list(map(lambda x: str(x).strip(','), lines))

    # Parse data
    import re
    p = re.compile(r'#(\d+)\s@\s(\d+),(\d+):\s(\d+)x(\d+)')

    db = set()
    # Parse each claim
    for line in lines:
        x = p.search(line)
        db.add(x.groups())

    max_x_tuple = max(db, key=lambda x: int(x[1]) + int(x[3]))
    max_x = int(max_x_tuple[1]) + int(max_x_tuple[3])
    max_y_tuple = max(db, key=lambda x: int(x[2]) + int(x[4]))
    max_y = int(max_y_tuple[2]) + int(max_y_tuple[4])

    # Construct the fabric space
    import numpy as np 
    fabric = np.zeros((max_x, max_y))

    # Partition the fabric space
    for entry in db:
        x = int(entry[1])
        x_max = x + int(entry[3])
        y = int(entry[2])
        y_max = y + int(entry[4])
        fabric[x:x_max, y:y_max] += 1

    # Count the inches doubled up
    print(np.sum(fabric >= 2))
