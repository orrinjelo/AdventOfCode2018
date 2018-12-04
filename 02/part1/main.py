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

    # Create histogram
    outer_dict = {}

    for label in lines:
        inner_dict = {}
        # Inner histogram for label
        for char in label:
            if char in inner_dict.keys():
                inner_dict[char] += 1
            else:
                inner_dict[char] = 1
        # Update outer histogram; filter out singular occuranaces
        updated = set()
        for k, v in inner_dict.items():
            if v >= 2:
                if v in updated:    # Ensure there aren't repeats. :)
                    continue
                updated.add(v)
                if v in outer_dict.keys():
                    outer_dict[v] += 1
                else:
                    outer_dict[v] = 1

    # Reduce the outer histogram into checksum
    from functools import reduce
    print('Answer: {}'.format(reduce(lambda x, y: x * y, outer_dict.values())))
