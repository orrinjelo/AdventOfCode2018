#!/usr/bin/env python3
import os, sys
import numpy as np 
from pprint import pprint
import time
from operator import itemgetter
import matplotlib.pyplot as plt
import re

s = ''

def run(x):
    stack_major = ['']

    stack_ptr = stack_major

    for c in x:
        print(c, ord(c))
        if c in 'NEWS':
            stack_ptr[-1] += c
        elif c == '(':
            stack_ptr.append([''])
            stack_ptr = stack_ptr[-1]
        elif c == ')':
            stack_ptr = stack_major
            while type(stack_ptr[-1]) == list:
                stack_ptr = stack_ptr[-1]
            best = max(stack_ptr, key=len)
            print(stack_ptr)
            del stack_ptr
            stack_ptr[-1] += best
            print(stack_major)
        elif c == '|':
            stack_ptr.append('')
    # return stack_major
    return max(stack_major, key=len)


if __name__ == '__main__':
    # Parse args, parse number list
    if len(sys.argv) <= 1:
        sys.exit('No entries given.  Answer: unknown')

    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    else:
        sys.exit('Too many args.')

    restr = lines[0]
    cutstr = restr[1:-1]

    print(run(cutstr))

    # def getLongest(x, i=0):
    #     s = ['']
    #     c = 0

    #     while True:
    #         try:
    #             if x[i] == '|':
    #                 c += 1
    #                 s.append('')
    #                 i += 1
    #             elif x[i] == '(':
    #                 res, i = getLongest(x, i+1)
    #                 s[c] += max(res, key=len)
    #             elif x[i] == ')':
    #                 print(s)
    #                 return max(s, key=len), i+1
    #             s[c] += x[i]
    #             i += 1
    #         except IndexError as e:
    #             break
    #         except Exception as e:
    #             print(type(e), e)
    #             break
    #     print(s, max(s, key=len))
    #     return max(s, key=len), i

    # s, l = getLongest('WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))')
    # print(len(s), s)



