#!/usr/bin/env python3
import os, sys
import numpy as np 
from pprint import pprint
import time
from operator import itemgetter
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

from utils.timeit import timeit

convert_map = {
    '.': 0, # Open ground
    '|': 1, # Trees
    '#': 2, # Lumberyard
}
reverse_map = {
    0: '.', # Open ground
    1: '|', # Trees
    2: '#', # Lumberyard
}

def tick(m):
    mm = np.copy(m)
    for y in range(m.shape[0]):
        for x in range(m.shape[1]):
            mm = tick_point(mm,m,x,y)
    m = mm[:]
    return mm

def tick_point(mm, m, x, y):
    min_x = x-1 if x > 0 else 0
    min_y = y-1 if y > 0 else 0
    max_x = x+2 if x < m.shape[1]-1 else m.shape[1]
    max_y = y+2 if y < m.shape[0]-1 else m.shape[0]

    local = m[min_y:max_y,min_x:max_x]
    t = m[y,x]
    if t == 0 and len(np.where(local==1)[0]) >= 3:
        mm[y,x] = 1
    elif t == 1 and len(np.where(local==2)[0]) >= 3:
        mm[y,x] = 2
    elif t == 2:
        if len(np.where(local==1)[0]) >= 1 and len(np.where(local==2)[0]) >= 2:
            pass
        else:
            mm[y,x] = 0
    return mm

def print_map(m):
    s = ''
    for y in range(m.shape[0]):
        for x in range(m.shape[1]):
            s += reverse_map[m[y,x]]
        s += '\n'
    print(s)

if __name__ == '__main__':
    # Parse args, parse number list
    if len(sys.argv) <= 1:
        sys.exit('No entries given.  Answer: unknown')

    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    else:
        sys.exit('Too many args.')

    nframes = 200
    m = np.zeros((len(lines), len(lines[0])-1), dtype=int)
    for i in range(len(lines)):
        for j in range(len(lines[0])-1):
            m[i,j] = convert_map[lines[i][j]]

    fig = plt.figure()

    ims = [] #[[plt.imshow(m, animated=True)]]

    for t in range(nframes):
        m = tick(m)
        ims.append([plt.imshow(m, animated=True, cmap='viridis')])

    from matplotlib.animation import FFMpegWriter
    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=1000)
    ani.save('wildforest2.gif', writer='imagemagick')