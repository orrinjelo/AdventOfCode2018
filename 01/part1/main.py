#!/usr/bin/env python3
import os, sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

from utils.timeit import timeit

@timeit
def day1_part1(input):
    return sum([int(x) for x in input])
    

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        sys.exit('No entries given.  Answer: 0')

    if len(sys.argv) == 2:
        print('Loading file: {}'.format(sys.argv[1]))
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    else:
        lines = sys.argv

    print(f'Answer: {day1_part1(lines)}')