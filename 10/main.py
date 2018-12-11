#!/usr/bin/env python3
import os, sys
import numpy as np 
from scipy import optimize
from pprint import pprint
import re
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from utils.timeit import timeit

class Star:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def step(self, speed=1):
        self.x += self.vx * speed
        self.y += self.vy * speed

    def project(self, t):
        x = self.x + self.vx*t
        y = self.y + self.vy*t
        return x,y

    def __gt__(self, x):
        return self.x > x.x

    def __lt__(self, x):
        return self.x < x.x

def calc_chi_sq(stars, t):
    s = 0
    xx, yy = stars[-1].project(t)
    for i in range(0, len(stars)-1):
        x, y = stars[i].project(t)
        s += (x - xx)**2 + (y - yy)**2
    return s**0.5

if __name__ == '__main__':
    # Parse args, parse number list
    if len(sys.argv) <= 1:
        sys.exit('No entries given.  Answer: unknown')

    if len(sys.argv) == 2:
        print('Loading file: {}'.format(sys.argv[1]))
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    else:
        sys.exit('Too many args.')
        
    r = re.compile(r'position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>')

    stars = []

    for line in lines:
        entry = r.match(line)
        x, y, vx, vy = entry.group(1),entry.group(2),entry.group(3),entry.group(4)
        stars.append(Star(int(x), int(y), int(vx), int(vy)))

    result = optimize.minimize_scalar(lambda t: calc_chi_sq(stars, int(t)))
    print(result.success)
    print(result.x)

    c = 4
    for n in range(-c, c):
        adjusted = int(result.x - n)

        xx = np.array([star.project(adjusted)[0] for star in stars])
        yy = np.array([star.project(adjusted)[1] for star in stars])

        plt.figure(n + c + 1)
        plt.title(f'Time = {adjusted}')
        plt.scatter(xx, yy, 50, marker='s')
    plt.show()
