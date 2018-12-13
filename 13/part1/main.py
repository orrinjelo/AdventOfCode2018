#!/usr/bin/env python3
import os, sys
import numpy as np 
from pprint import pprint
import time
import re
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

from utils.timeit import timeit

class Minecart:
    def __init__(self, x, y, direction):
        self.direction_choice = 'ccw'
        self.x = x
        self.y = y
        self.direction = direction
        self.history_x = [x]
        self.history_y = [y]

    def progress(self, sym):
        if sym == '|':
            if self.direction != 'up' and self.direction != 'down':
                raise Exception(f'Minecart is derailed at {self.x},{self.y}!')
            elif self.direction == 'up':
                self.y -= 1
            elif self.direction == 'down':
                self.y += 1
            else:
                raise Exception('Logic error.')
        elif sym == '-':
            if self.direction != 'left' and self.direction != 'right':
                raise Exception(f'Minecart is derailed at {self.x},{self.y}!')
            elif self.direction == 'left':
                self.x -= 1
            elif self.direction == 'right':
                self.x += 1
            else:
                raise Exception('Logic error.')
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
                raise Exception('Invalid direction?')
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
                raise Exception('Invalid direction?')
        elif sym == '+':
            rotate = ['left', 'up', 'right', 'down', 'left', 'up', 'right', 'down']
            idx = rotate.index(self.direction)
            if self.direction_choice == 'ccw':
                self.direction = rotate[idx-1]
                self.direction_choice = 'straight'
            elif self.direction_choice == 'straight':
                self.direction_choice = 'cw'
            elif self.direction_choice == 'cw':
                self.direction = rotate[idx+1]
                self.direction_choice = 'ccw'
            else:
                raise Exception(f'Invalid direction choice? {self.direction_choice}')

            if self.direction == 'left':
                self.x -= 1
            elif self.direction == 'right':
                self.x += 1
            elif self.direction == 'up':
                self.y -= 1
            elif self.direction == 'down':
                self.y += 1
        else:
            raise Exception(f'Given strange symbol: {sym}')

        self.history_x.append(self.x)
        self.history_y.append(self.y)
        if len(self.history_x) > 2000:
            del self.history_x[0]
            del self.history_y[0]

    def __str__(self):
        return f'({self.x},{self.y}) [{self.direction}]'

class Map:
    def __init__(self, lines):
        self.minecarts = []
        self.yourcarts = []
        self.collisions = [[],[]]
        self.parse(lines)
        self.ticks = 0

    def has_collision(self):
        for a in range(len(self.minecarts)):
            for b in range(a):
                if self.minecarts[a].x == self.minecarts[b].x and self.minecarts[a].y == self.minecarts[b].y:
                    print(f'Collision @ {self.minecarts[a].x},{self.minecarts[a].y}!')
                    deada, deadb = self.minecarts[a], self.minecarts[b]
                    self.collisions[0].append(self.minecarts[a].x)
                    self.collisions[1].append(self.minecarts[a].y)
                    self.yourcarts.append(deada)
                    self.yourcarts.append(deadb)
                    self.minecarts.remove(deada)
                    self.minecarts.remove(deadb)
                    print(f'{len(self.minecarts)} minecarts are left. Tick: {self.ticks}')
                    return True
        return False

    def tick(self):
        self.ticks += 1
        def cartorder(cart):
            return (cart.x, cart.y)

        for cart in sorted(self.minecarts, key=lambda cart:(cart.x, cart.y)):
            cart.progress(self.npmap[cart.x, cart.y])
            if self.has_collision():
                # self.npmap[cart.x, cart.y] = 'X'
                return True
            # print(str(cart))
        return False

    def parse(self, lines):
        width = len(lines[0])
        height = len(lines)
        self.npmap = np.zeros((width, height), dtype='U1')
        for y in range(height):
            for x in range(width):
                try:
                    char = lines[y][x]
                except:
                    continue
                if char in '/\\|-+':
                    self.npmap[x,y] = char
                elif char in '^v':
                    self.npmap[x,y] = '|'
                    self.minecarts.append(Minecart(x,y,'up' if char == '^' else 'down'))
                elif char in '<>':
                    self.npmap[x,y] = '-'
                    self.minecarts.append(Minecart(x,y,'right' if char == '>' else 'left'))
                elif char == ' ':
                    self.npmap[x,y] = ' '
                elif char == '\n':
                    continue
                else:
                    raise Exception(f'Invalid character encountered? {char}@{x,y}')

    def __str__(self):
        newmap = np.copy(self.npmap)
        for cart in self.minecarts:
            newmap[cart.x,cart.y] = '*'
        for cart in self.yourcarts:
            newmap[cart.x,cart.y] = 'X'
        return '\n'.join([''.join(newmap[:,row]) for row in range(newmap.shape[1])])
            


if __name__ == '__main__':
    # Parse args, parse number list
    if len(sys.argv) <= 1:
        sys.exit('No entries given.  Answer: unknown')

    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    else:
        sys.exit('Too many args.')

    @timeit
    def parseMap():
        return Map(lines)

    m = parseMap()
    
    @timeit
    def runMap(m):
        while len(m.minecarts) > 1:
            m.tick()
            if m.ticks % 10000 == 0:
                print(f'Ticks = {m.ticks}')
            # time.sleep(1)
            
            # print([str(c) for c in m.minecarts])


    runMap(m)

    if m.minecarts:
        print(str(m))
        print(''.join([str(c) for c in m.minecarts]))
    else:
        print('No minecarts left!')

    plt.figure(1)
    for cart in m.minecarts:
        plt.plot(cart.history_x, cart.history_y)
    for cart in m.yourcarts:
        plt.plot(cart.history_x, cart.history_y)
    plt.plot(m.collisions[0],m.collisions[1],'ro')
    plt.show()