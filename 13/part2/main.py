#!/usr/bin/env python3
import os, sys
import numpy as np 
from pprint import pprint
import re

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

from utils.timeit import timeit

class Minecart:
    def __init__(self, x, y, direction):
        self.direction_choice = 'ccw'
        self.x = x
        self.y = y
        self.direction = direction

    def progress(self, sym):
        if sym == '|':
            if self.direction != 'up' and self.direction != 'down':
                throw Exception(f'Minecart is derailed at {self.x},{self.y}!')
            elif self.direction == 'up':
                self.y -= 1
            elif self.direction == 'down':
                self.y += 1
            else:
                throw Exception('Logic error.')
        elif sym == '-':
            if self.direction != 'left' and self.direction != 'right':
                throw Exception(f'Minecart is derailed at {self.x},{self.y}!')
            elif self.direction == 'left':
                self.x -= 1
            elif self.direction == 'right':
                self.x += 1
            else:
                throw Exception('Logic error.')
        elif sym == '/':
            if self.direction == 'left':
                self.direction = 'down'
                self.y += 1
            elif self.direction == 'down':
                self.direction = 'left'
                self.x -= 1
            elif self.direction == 'up':
                self.direction = 'right'
                self.x += 1
            elif self.direction == 'right':
                self.direction = 'up'
                self.y -= 1
            else:
                throw Exception('Invalid direction?')
        elif sym == '\\':
            if self.direction == 'left':
                self.direction = 'up'
                self.y -= 1
            elif self.direction == 'up':
                self.direction = 'left'
                self.x -= 1
            elif self.direction == 'down':
                self.direction = 'right'
                self.x += 1
            elif self.direction == 'right':
                self.direction = 'down'
                self.y += 1
            else:
                throw Exception('Invalid direction?')
        elif sym == '+':
            rotate = ['left', 'up', 'right', 'down', 'left', 'up', 'right', 'down']
            idx = rotate.index(self.direction)
            if self.direction_choice == 'ccw':
                self.direction = rotate[idx-1]
                self.direction_choice = 'straight'
            elif self.direction_choice == 'straight':
                self.direction_choice = 'right'
            elif self.direction_choice == 'cw':
                self.direction = rotate[idx+1]
                self.direction_choice = 'ccw'
            else:
                throw Exception('Invalid direction choice?')

class Map:
    def __init__(self, lines):
        self.parse(lines)

    def has_collision(self):
        pass

    def parse(self, lines):
        width = len(lines[0])
        height = len(lines)
        self.npmap = np.zeros((width, height), dtype=str)
        for y in range(height):
            for x in range(width):
                char = lines[y][x]
                if char in '/\\|-+':
                    self.npmap[x,y] = char
                elif char in '^v':
                    self.npmap[x,y] = '|'
                    # Create cart
                elif char in '<>':
                    self.npmap[x,y] = '-'
                    # Create cart
                else:
                    throw Exception(f'Invalid character encountered? {char}@{x,y}')

if __name__ == '__main__':
    # Parse args, parse number list
    if len(sys.argv) <= 1:
        sys.exit('No entries given.  Answer: unknown')

    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    else:
        sys.exit('Too many args.')