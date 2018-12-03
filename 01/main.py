#!/usr/bin/env python3
import os, sys

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        sys.exit('No entries given.  Answer: 0')

    if len(sys.argv) == 2:
        print('Loading file: {}'.format(sys.argv[1]))
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    else:
        lines = sys.argv

    print('Answer: {}'.format(sum([int(x) for x in lines])))