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

    # Ugly implementation, runs about 2 secs.
    import difflib as dl
    for x in range(len(lines)):
        for y in range(x, len(lines)):
            line = lines[x]
            otherline = lines[y]
            if line == otherline:
                continue
            diff = dl.ndiff(line, otherline)
            combo = ''.join(diff)
            count = len(combo[0::3].strip(' -'))
            if count == 1:
                print(''.join([combo[x*3+2] for x in range(len(combo)//3) if combo[x*3] == ' ']))