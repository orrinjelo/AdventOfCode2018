#!/usr/bin/env python3
import os, sys
import numpy as np 
from pprint import pprint
import time
from operator import itemgetter

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

from utils.timeit import timeit

class Elf:
    def __init__(self, x, y, hp=200, attack=3):
        self.x = x
        self.y = y
        self.hp = hp
        self.attack = attack

    def step(self, cmap):
        in_range = []
        cmap_copy = cmap.cave_map

        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if abs(dy) == abs(dx):
                    continue
                if cmap_copy[self.x + dx, self.y + dy] == 3: #'G'
                    self.attackDude(cmap, self.x + dx, self.y + dy)
                    return cmap_copy
        # In range
        for goblin in cmap.goblins:
            for dx in range(-1,2):
                for dy in range(-1,2):
                    if abs(dx) == abs(dy):
                        continue
                    if cmap.cave_map[goblin.x + dx, goblin.y + dy] == 0:
                        cmap_copy[goblin.x + dx, goblin.y + dy] = 5 # '?'
        print('In range:')
        self.print_map(cmap, cmap_copy)
        in_range = np.where(cmap_copy == 5)

        # Reachable
        reachable_paths = []
        for i in range(len(in_range[0])):
            is_reachable, visited = self.is_reachable(in_range[0][i], in_range[1][i], cmap_copy)
            if is_reachable:
                reachable_paths.append(visited)
                cmap_copy[in_range[0][i], in_range[1][i]] = 6 #'@'
            else:
                cmap_copy[in_range[0][i], in_range[1][i]] = 0 #'.'
        print('Reachable:')
        self.print_map(cmap, cmap_copy)
        reachable = np.where(cmap_copy == 6)

        # Nearest
        nearest_list = self.nearest(cmap_copy, reachable)
        nearest_paths = []
        for i in range(len(reachable[0])):
            if (reachable[0][i],reachable[1][i]) not in nearest_list:
                cmap_copy[reachable[0][i], reachable[1][i]] = 0 #'.'
            else:
                nearest_paths.append(reachable_paths[i])
                cmap_copy[reachable[0][i], reachable[1][i]] = 7 #'!'
        print('Nearest:')
        self.print_map(cmap, cmap_copy)

        # Choose
        choice = self.choosiest(nearest_list)
        choice_path = nearest_paths[nearest_list.index(choice)]
        cmap_copy[reachable] = 0 #'.'
        cmap_copy[choice[0],choice[1]] = 8 #'+'
        print('Choice:')
        self.print_map(cmap, cmap_copy)
        print(choice_path)
        del choice_path[-1]

        if len(choice_path) == 0:
            cmap_copy[self.x, self.y] = 0#'.'
            self.x = choice[0]
            self.y = choice[1]
            cmap_copy[self.x, self.y] = 2#'E'
        else:
            cmap_copy[self.x, self.y] = 0#'.'
            self.x = choice_path[-1][0]
            self.y = choice_path[-1][1]
            cmap_copy[self.x, self.y] = 2#'E'
            cmap_copy[choice[0],choice[1]] = 0 #'.'

        print('New:')
        self.print_map(cmap, cmap_copy)
        return cmap_copy


    def is_reachable(self, x,y, cmap, visited=None):
        if visited == None:
            visited = []
        if cmap[x,y] not in [0, 5, 6]:
            return False, None
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if abs(dy) == abs(dx):
                    continue
                if (x+dx,y+dy) in visited:
                    continue
                visited.append((x+dx, y+dy))
                if x+dx == self.x and y+dy == self.y:
                    return True, visited
                elif cmap[x+dx, y+dy] in [0, 5, 6]:
                    if self.is_reachable(x+dx, y+dy, cmap, visited):
                        return True, visited
        return False, None

    def nearest(self, cmap, reachable):
        best = (100000,None)
        nearest = []
        for i in range(len(reachable[0])):
            dist = abs(self.x - reachable[0][i]) + abs(self.y - reachable[1][i])
            if dist < best[0]:
                best = (dist, i)
                nearest = [(reachable[0][i],reachable[1][i])]
            elif dist == best[0]:
                nearest.append((reachable[0][i],reachable[1][i]))
        return nearest

    def choosiest(self, nearest):
        return min(nearest, key=itemgetter(1))

    def attackDude(self, cmap, x, y):
        for i in range(len(cmap.goblins)):
            goblin = cmap.goblins[i]
            if (goblin.x,goblin.y) == (x,y):
                cmap.goblins[i].hp -= self.attack
                if cmap.goblins[i].hp <= 0:
                    del cmap.goblins[i]
                    cmap.cave_map[x,y] = 0
                    print(f'Goblin at {x},{y} has died.')
                return


    def print_map(self, cmap, m):
        s = ''
        for y in range(m.shape[1]):
            for x in range(m.shape[0]):
                s += cmap.map_key[m[x,y]]
        print(s[:-1])

class Goblin(Elf):
    def __init__(self, x, y, hp=200, attack=3):
        self.x = x
        self.y = y
        self.hp = hp
        self.attack = attack

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
            5: '?',  # In range
            6: '@',  # Reachable
            7: '!',  # Nearest
            8: '+',  # Chosen
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
                        self.elves.append(Elf(x,y))
                    elif lines[y][x] == 'G':
                        self.goblins.append(Goblin(x,y))
                except:
                    pass

    def step(self):
        self.cave_map = self.elves[0].step(m)

    def __str__(self):
        s = ''
        for y in range(self.cave_map.shape[1]):
            for x in range(self.cave_map.shape[0]):
                s += self.map_key[self.cave_map[x,y]]
        return s


if __name__ == '__main__':
    # Parse args, parse number list
    if len(sys.argv) <= 1:
        sys.exit('No entries given.  Answer: unknown')

    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    else:
        sys.exit('Too many args.')

    m = Map(lines, None)
    print(str(m))
    m.step()
    m.step()
    m.step()
    m.step()
    for x in range(100):
        m.step()
    print([x.hp for x in m.goblins])
    print(str(m))
