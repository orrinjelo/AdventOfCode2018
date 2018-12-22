#!/usr/bin/env python3
import os, sys
import numpy as np 
from pprint import pprint
import time
# from operator import itemgetter
import matplotlib.pyplot as plt
import re
import networkx

maze = networkx.Graph()

s = ''

def cleanup(x):
    xl = len(x)
    x = x.replace('EW','')
    x = x.replace('WE','')
    x = x.replace('NS','')
    x = x.replace('SN','')
    x = x.replace('NESW','')
    x = x.replace('ESWN','')
    x = x.replace('SWNE','')
    x = x.replace('WNES','')
    x = x.replace('NWSE','')
    x = x.replace('WSEN','')
    x = x.replace('SENW','')
    x = x.replace('ENWS','')
    if len(x) < xl:
        return cleanup(x)
    else:
        return x

def run(x):
    '''This is the regex-parsing approach'''
    stack_major = [['']]

    stack_ptr = stack_major[-1]
    meta = cleanup(x)

    for c in meta:
        if c in 'NEWS':
            stack_ptr[-1] += c
        elif c == '(':
            stack_major.append([''])
            stack_ptr = stack_major[-1]
        elif c == ')':
            best = max(stack_ptr, key=lambda x: len(cleanup(x)))
            del stack_major[-1]
            stack_ptr = stack_major[-1]
            stack_ptr[-1] += best
        elif c == '|':
            stack_ptr.append('')
    meta = max(stack_major[0], key=lambda x: len(cleanup(x)))

    return meta

class ElfMap:
    def __init__(self, sizex=400, sizey=400):
        self.elfmap = np.zeros(sizex,sizey)
        self.visitmap = np.zeros(sizex,sizey)
        self.sizex, self.sizey = sizex, sizey
        self.path = [[0],[0]]
        self.x, self.y = 0, 0
        self.set(0,0,1)
        self.step = 1

    def get(self, x, y):
        return self.elfmap[x+sizex//2, y+sizey//2]

    def getvisit(self, x, y):
        return self.visitmap[x+sizex//2, y+sizey//2]

    def set(self,x,y,v):
        self.elfmap[x+sizex//2, y+sizey//2] = v

    def setvisit(self,x,y,v):
        self.visitmap[x+sizex//2, y+sizey//2] = v

    def is_visited(self,x,y):
        if get(x,y) != 0:
            return True
        return False

    def traverse(self,s):
        stack_major = [['']]

        stack_ptr = stack_major[-1]

        for c in s:
            if c in 'NEWS':
                stack_ptr[-1] += c
            elif c == '(':
                stack_major.append([''])
                stack_ptr = stack_major[-1]
            elif c == ')':
                stack_ptr = stack_major[-1]
                stack_ptr[-1] += best
            elif c == '|':
                stack_ptr.append('')

            if c == 'N':
                dx,dy = 0,-1
            elif c == 'S':
                dx,dy = 0,1
            elif c == 'E':
                dx,dy = 1,0
            elif c == 'W':
                dx,dy = -1,0
            v = self.getvisit(self.x, self.y)
            self.x += dx
            self.y += dy
            nv = self.getvisit(self.x, self.y)
            if nv != 0:
                if nv > v+1:
                    pass
            self.path[0].append(self.x)
            self.path[1].append(self.y)
            self.set(x,y,i)
            i += 1


def plot_course(s):
    graf = np.zeros((len(s)+1, 2), dtype=int)
    x,y = 0,0
    graf[0,:] = x,y

    for i in range(1,len(s)+1):
        if s[i-1] == 'N':
            dx,dy = 0,-1
        elif s[i-1] == 'S':
            dx,dy = 0,1
        elif s[i-1] == 'E':
            dx,dy = 1,0
        elif s[i-1] == 'W':
            dx,dy = -1,0
        x += dx
        y += dy
        graf[i,:] = x,y

    plt.plot(graf[:,0], graf[:,1])
    plt.show()

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

    res = run(cutstr)
    # res = run('N|ES|WES|SENE')
    print(res)
    print(len(res))
    plot_course(res)