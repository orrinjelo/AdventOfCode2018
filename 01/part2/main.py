#!/usr/bin/env python3
import os, sys

if __name__ == '__main__':
    # Parse args, parse number list
    if len(sys.argv) <= 1:
        sys.exit('No entries given.  Answer: unknown')

    if len(sys.argv) == 2:
        print('Loading file: {}'.format(sys.argv[1]))
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    else:
        lines = sys.argv[1:]

    lines = list(map(lambda x: int(str(x).strip(',')), lines))

    def number_generator():
        '''Will loop through list of numbers circularly'''
        position = 0
        while True:
            if position == len(lines):
                position = 0
            yield lines[position]
            position += 1

    numbers = number_generator()

    # Iterate through the calculations until we have a duplicate
    entries = set({0})
    last = 0
    while True:
        n = last + next(numbers)
        if n in entries:
            print('Answer: {}'.format(n))
            break
        else:
            entries.add(n)
            last = n
