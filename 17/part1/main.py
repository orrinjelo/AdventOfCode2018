#!/usr/bin/env python3
import os, sys
import numpy as np 
from pprint import pprint
import time
from operator import itemgetter
import matplotlib.pyplot as plt
import re

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

from utils.timeit import timeit

class Board:
    def __init__(self, size, lines):
        self.shape = size
        self.board = np.zeros(self.shape, dtype=int)

        self.key = {
            ' ': 0, # Sand
            '#': 1, # Clay
            '+': 2, # Source
            '|': 3, # Falling water
            '~': 4  # Standing water
        }

        # x=474, y=1887..1892        
        inp = re.compile(r'(x|y)=(\d+),\s(y|x)=(\d+)\.\.(\d+)')
        for line in lines:
            m = inp.match(line)
            g = m.group(1)
            if g == 'x':
                xlbl, x1, ylbl, y1, y2 = m.group(1), int(m.group(2)), m.group(3), int(m.group(4)), int(m.group(5))+1
                x2 = x1+1
            elif g == 'y':
                ylbl, y1, xlbl, x1, x2 = m.group(1), int(m.group(2)), m.group(3), int(m.group(4)), int(m.group(5))+1
                y2 = y1+1

            print(xlbl, x1, x2, ylbl, y1, y2)
            assert(xlbl == 'x')
            assert(ylbl == 'y')
            self.board[x1:x2, y1:y2] = 1

        self.board[500,0] = 2
        self.start = 500,1
        self.board[self.start] = 3

    def plot(self, x1=None, x2=None, y1=None, y2=None):
        if x1 is None:
            x1 = 0
        if x2 is None:
            x2 = self.shape[0]
        if y1 is None:
            y1 = 0
        if y2 is None:
            y2 = self.shape[1]

        plt.figure()
        plt.imshow(np.transpose(self.board[x1:x2,y1:y2]), aspect='auto')
        plt.show()

    def flow(self, x, y):
        if y == self.shape[1]:
            return False, x, y
        if self.board[x,y+1] == 0:
            self.board[x,y+1] = 3
            if self.flow(x,y+1) and self.board[x,y+1] != 3:
                return self.flow(x,y)
        else:
            left_bound, lx, ly = self.flow_left(x-1,y)
            right_bound, rx, ry = self.flow_right(x+1,y)
            if left_bound and right_bound:
                self.board[lx:rx+1,ly:ry+1] = 4
                return True, x, y
            else:
                return False, x, y

    def flow_left(self, x, y):
        if self.board[x,y+1] == 0:
            return False, x-1, y #self.flow(x,y+1)
        if x == 0:
            return False, x, y
        if self.board[x,y] == 0:
            self.board[x,y] = 3
            return self.flow_left(x-1,y)
        elif self.board[x,y] == 1:
            return True, x+1, y
        else:
            return False, x, y

    def flow_right(self, x, y):
        if self.board[x,y] == 0:
            self.board[x,y] = 3
        if self.board[x,y+1] == 0:
            return False, x+1, y#self.flow(x,y+1)
        if x == self.shape[0]-1:
            return False, x, y
        if self.board[x,y] == 0:
            # self.board[x,y] = 3
            return self.flow_right(x+1,y)
        elif self.board[x,y] == 1:
            return True, x-1, y
        else:
            return False, x, y    



def main(lines):
    board = Board((1000,2000), lines)
    board.flow(board.start[0],board.start[1])
    board.plot(494,508,0,14)

if __name__ == '__main__':
    # Parse args, parse number list
    if len(sys.argv) <= 1:
        sys.exit('No entries given.  Answer: unknown')

    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    else:
        sys.exit('Too many args.')

    main(lines)