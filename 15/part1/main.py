#!/usr/bin/env python3
import os, sys
import numpy as np 
from pprint import pprint
import time
import curses

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

from utils.timeit import timeit

class Entity:
    def __init__(self, x, y, hp=200, attack=3):
        self.x = x
        self.y = y
        self.hp = hp
        self.attack = attack

    def step(self, cmap):
        in_range = []
        cmap_copy = cmap.cave_map

        # In range
        for goblin in cmap.goblins:
            for dx in range(-1,2):
                for dy in range(-1,2):
                    if abs(dx) == abs(dy):
                        continue
                    if cmap.cave_map[goblin.x + dx, goblin.y + dy] == 0:
                        cmap_copy[goblin.x + dx, goblin.y + dy] = 5 # '?'
        self.print_map(cmap, cmap_copy)
        in_range = np.where(cmap_copy == 5)

        # Reachable
        for i in range(len(in_range[0])):
            if self.is_reachable(in_range[0][i], in_range[1][i]):
                cmap_copy[in_range[0][i], in_range[1][i]] = '@'
            else:
                cmap_copy[in_range[0][i], in_range[1][i]] = '.'
        self.print_map(cmap, cmap_copy)

    def is_reachable(x,y):
        pass

    def print_map(self, cmap, m):
        s = ''
        for y in range(m.shape[1]):
            for x in range(m.shape[0]):
                s += cmap.map_key[m[x,y]]
        print(s)


class Map:
    def __init__(self, lines, pad):

        self.pad = pad
        self.elves = []
        self.goblins = []
        self.map_key = {
            0: '.',  # Open
            1: '#',  # Wall
            2: 'E',  # Elf
            3: 'G',  # Goblin
            4: '\n',
            5: '?',
            6: '@',
            7: '!',
            8: '+',
        }
        self.color_key = {
            0: curses.COLOR_BLACK,  # Open
            1: curses.COLOR_YELLOW, # Wall
            2: curses.COLOR_GREEN,  # Elf
            3: curses.COLOR_RED,    # Goblin
        }
        self.reverse_key = {
            '.': 0,
            '#': 1,
            'E': 2,
            'G': 3,
            '\n': 4
        }

        self.parseMap(lines)

    @timeit
    def parseMap(self, lines):
        shape = len(lines[0]), len(lines)
        self.cave_map = np.zeros(shape, dtype=int)
        for x in range(shape[0]):
            for y in range(shape[1]):
                try:
                    self.cave_map[x,y] = self.reverse_key[lines[y][x]]
                    if lines[y][x] == 'E':
                        self.elves.append(Entity(x,y))
                    elif lines[y][x] == 'G':
                        self.goblins.append(Entity(x,y))
                except:
                    pass

    def __str__(self):
        s = ''
        for y in range(self.cave_map.shape[1]):
            for x in range(self.cave_map.shape[0]):
                s += self.map_key[self.cave_map[x,y]]
        return s

    # def print(self):
    #     for y in range(self.cave_map.shape[1]):
    #         for x in range(self.cave_map.shape[0]):
    #             try:
    #                 self.pad.addch(y,x, ord(self.map_key[self.cave_map[x,y]]), self.color_key[self.cave_map[x,y]])
    #             except:
    #                 pass
    #     self.pad.refresh(0, 0, 0, 0, self.cave_map.shape[1], self.cave_map.shape[0])


if __name__ == '__main__':
    # Parse args, parse number list
    if len(sys.argv) <= 1:
        sys.exit('No entries given.  Answer: unknown')

    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    else:
        sys.exit('Too many args.')

    # # Curses setup
    # stdscr = curses.initscr()
    # curses.start_color()
    # curses.noecho()
    # pad = curses.newpad(len(lines), len(lines[0]))

    m = Map(lines, None)
    print(str(m))
    m.elves[0].step(m)