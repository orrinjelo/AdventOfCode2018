#!/usr/bin/env python3
import os, sys
import numpy as np 
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

from utils.timeit import timeit

if __name__ == '__main__':
    # Parse args, parse number list
    if len(sys.argv) <= 1:
        sys.exit('No entries given.  Answer: unknown')

    if len(sys.argv) == 2:
        input_val = str(int(sys.argv[1]))
    else:
        sys.exit('Too many args.')
    
    scores = '37'

    @timeit
    def part2(scores, input_val):
        buddy,legolas = 0, 1
        local_scores = scores
        min_idx = -len(input_val)-1
        while input_val not in local_scores[min_idx:]:
            local_scores += str(int(local_scores[buddy]) + int(local_scores[legolas]))
            buddy   = (buddy   + int(local_scores[buddy])   + 1) % len(local_scores)
            legolas = (legolas + int(local_scores[legolas]) + 1) % len(local_scores)
        return local_scores.index(input_val)

    ans = part2(scores, input_val)

    print('Part 2:', ans)
