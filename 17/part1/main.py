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

        self.reverse_key = {
            0: '.', # Sand
            1: '#', # Clay
            2: '+', # Source
            3: '|', # Falling water
            4: '~'  # Standing water
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
            try:
                res = self.flow(x,y+1)
                if self.board[x,y+1] != 3:
                    return self.flow(x,y)
            except Exception as e:
                print(e)
                return False, x, y
        elif self.board[x,y+1] == 3:
            # Running water?
            return False, x, y
        else:
            left_bound, lx, ly = self.flow_left(x-1,y)
            right_bound, rx, ry = self.flow_right(x+1,y)
            if left_bound and right_bound:
                self.board[lx:rx+1,ly:ry+1] = 4
                return True, x, y
            else:
                return False, x, y

    def flow_left(self, x, y):
        if self.board[x,y] == 0:
            self.board[x,y] = 3
        if self.board[x,y+1] == 0:
            self.flow(x,y)
            return False, x-1, y
        if x == 0:
            return False, x, y
        if self.board[x,y] == 3 and self.board[x,y+1] != 3:
            # self.board[x,y] = 3
            return self.flow_left(x-1,y)
        elif self.board[x,y] == 1:
            return True, x+1, y
        else:
            return False, x, y

    def flow_right(self, x, y):
        if self.board[x,y] == 0:
            self.board[x,y] = 3
        if self.board[x,y+1] == 0:
            self.flow(x,y)
            return False, x+1, y
        if x == self.shape[0]-1:
            return False, x, y
        if self.board[x,y] == 3 and self.board[x,y+1] != 3:
            # self.board[x,y] = 3
            return self.flow_right(x+1,y)
        elif self.board[x,y] == 1:
            return True, x-1, y
        else:
            return False, x, y    



def main(lines):
    board = Board((1000,2000), lines)
    try:
        board.flow(board.start[0],board.start[1])
    except Exception as e:
        print(e)
        
    maxy = np.max(np.where(board.board == 1)[1])
    minx = np.min(np.where(board.board == 1)[0])
    maxx = np.max(np.where(board.board == 1)[0])
    reduced_map = board.board[minx-2:maxx+3,:maxy+1]
    # for x in range(board.board.shape[0]-1):
    #     for y in range(board.board.shape[1]-1):
    #         if np.sum(board.board[x:x+2,y:y+2] == np.array([[3,3],[3,3]], dtype=int)) == 4:
    #             print('Error?:',x,y)
    print(np.sum(reduced_map >= 3))
    board.plot(y2=maxy+1)

    with open('res4-2.txt','w') as f:
        for y in range(maxy+1):
            f.write('\n')
            for x in range(minx-2, maxx+3):
                f.write(board.reverse_key[board.board[x,y]])

    # plt.figure(2)
    # plt.imshow(reduced_map >= 3)
    # plt.show()

if __name__ == '__main__':
    # Parse args, parse number list
    if len(sys.argv) <= 1:
        sys.exit('No entries given.  Answer: unknown')

    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    else:
        sys.exit('Too many args.')

    sys.setrecursionlimit(20000)

    main(lines)