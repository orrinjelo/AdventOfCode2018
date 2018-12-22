#!/usr/bin/env python3
import os, sys
import numpy as np 
from pprint import pprint
import time
from operator import itemgetter
import matplotlib.pyplot as plt
import re

class Node:
    def __init__(self, parent=None, contents=None, pref=''):
        if contents == None:
            self.contents = ['']
        else:
            self.contents = contents
        self.pref = pref
        self.parent = parent
        self.str = ''

    def __repr__(self):
        s = ''
        if self.pref:
            s += '"' + repr(self.pref) + '"+'
        s += '[' + ','.join([repr(x) for x in self.contents]) + ']'
        if self.str:
             s += '+"' + repr(self.str) + '"'
        return s

    def __iadd__(self, i):
        self.str += i
        return self

class Tree:
    def __init__(self):
        self.head = Node()
        self.ptr = self.head

    def parse(self, s):
        try:
            for c in s:
                if c in 'NEWS':
                    self.ptr.contents[-1] += c

                elif c == '|':
                    self.ptr.contents.append('')
                elif c == '(':
                    pref = self.ptr.contents[-1]
                    n = Node(self.ptr, pref=pref)
                    del self.ptr.contents[-1]
                    self.ptr.contents.append(n)
                    self.ptr = n
                elif c == ')':
                    self.ptr = self.ptr.parent

        except Exception as e:
            print(e)
            print(self.ptr.contents)
        print(self.head)

class Maze:
    def __init__(self, sizex=400, sizey=400):
        self.sizex = sizex
        self.sizey = sizey
        self.map = np.zeros((sizex, sizey), dtype=int)

    def run(self,node,x=0,y=0,i=1):
        # N = 100000
        for branch in node.contents:
            if type(branch) == str:
                j = i
                for c in branch:
                    if c == 'N':
                        dx,dy = 0,-1
                    elif c == 'S':
                        dx,dy = 0,1
                    elif c == 'E':
                        dx,dy = 1,0
                    elif c == 'W':
                        dx,dy = -1,0
                    x += dx
                    y += dy
                    if self.map[x*2+self.sizex//2,y*2+self.sizey//2] < j and self.map[x*2+self.sizex//2,y*2+self.sizey//2] != 0:
                        break
                    else:
                        self.map[x*2+self.sizex//2,y*2+self.sizey//2] = j #% N + 100
                        self.map[x*2-dx+self.sizex//2,y*2-dy+self.sizey//2] = j #% N + 100
                    j += 1
            elif type(branch) == Node:
                j = i
                if type(branch.pref) == Node:
                    self.run(branch.pref,x, y, i=j)
                else:
                    for c in branch.pref:
                        if c == 'N':
                            dx,dy = 0,-1
                        elif c == 'S':
                            dx,dy = 0,1
                        elif c == 'E':
                            dx,dy = 1,0
                        elif c == 'W':
                            dx,dy = -1,0
                        x += dx
                        y += dy
                        if self.map[x*2+self.sizex//2,y*2+self.sizey//2] < j and self.map[x*2+self.sizex//2,y*2+self.sizey//2] != 0:
                            break
                        else:
                            self.map[x*2+self.sizex//2,y*2+self.sizey//2] = j #% N + 100
                            self.map[x*2-dx+self.sizex//2,y*2-dy+self.sizey//2] = j #% N + 100
                        j += 1
                self.run(branch,x,y,j)
                if type(branch.str) == Node:
                    self.run(branch.pref, x, y, i=j)
                else:
                    for c in branch.str:
                        if c == 'N':
                            dx,dy = 0,-1
                        elif c == 'S':
                            dx,dy = 0,1
                        elif c == 'E':
                            dx,dy = 1,0
                        elif c == 'W':
                            dx,dy = -1,0
                        x += dx
                        y += dy
                        if self.map[x*2+self.sizex//2,y*2+self.sizey//2] < j and self.map[x*2+self.sizex//2,y*2+self.sizey//2] != 0:
                            break
                        else:
                            self.map[x*2+self.sizex//2,y*2+self.sizey//2] = j #% N + 100
                            self.map[x*2-dx+self.sizex//2,y*2-dy+self.sizey//2] = j #% N + 100
                        j += 1

    def plot(self):        
        plt.figure()
        plt.imshow(self.map,cmap='rainbow')
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

    tree = Tree()
    tree.parse(cutstr)
    # tree.parse('N|ES|WES|SEN(E|WE)SSE(SS|EEW)')
    maze = Maze()
    maze.run(tree.head)

    print(np.max(maze.map))

    maze.plot()


    # print(tree.head.contents)

    # res = run(cutstr)
    # # res = run('N|ES|WES|SENE')
    # print(res)
    # print(len(res))
    # plot_course(res)