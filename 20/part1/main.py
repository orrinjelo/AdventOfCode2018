#!/usr/bin/env python3
import os, sys
import numpy as np 
from pprint import pprint
import time
# from operator import itemgetter
import matplotlib.pyplot as plt
import re
import networkx


def traverse(msg):
    maze = networkx.Graph()
    stack_major = []
    s, e = set({(0,0)}), set()
    pos = set({(0,0)})

    for c in msg:
        if c in 'NEWS':
            if c == 'N':
                dx,dy = 0,-1
            elif c == 'S':
                dx,dy = 0,1
            elif c == 'E':
                dx,dy = 1,0
            elif c == 'W':
                dx,dy = -1,0

            maze.add_edges_from((p,(p[0]+dx,p[1]+dy)) for p in pos)
            pos = {(p[0]+dx,p[1]+dy) for p in pos}
        elif c == '(':
            stack_major.append((s,e))
            s,e = pos, set()
        elif c == ')':
            pos.update(e)
            s,e = stack_major.pop()
        elif c == '|':
            e.update(pos)
            pos = s

        # networkx.draw(maze)
    return maze, networkx.algorithms.shortest_path_length(maze, (0,0))

def plot_course(s,g):
    N = 400
    m = 2
    graf = np.zeros((N,N), dtype=int)

    for k in s.keys():
        x, y = k
        graf[m*x+N//2,m*y+N//2] = s[k] + 4000

    for e in g.edges():
        a, b = e
        c = graf[m*a[0]+N//2, m*a[1]+N//2]
        x, y = (m*a[0]+N//2+m*b[0]+N//2)//2, (m*a[1]+N//2+m*b[1]+N//2)//2
        graf[x,y] = c

    plt.imshow(graf, cmap='gist_earth')
    plt.colorbar()
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

    maze, res = traverse(cutstr)
    # res = run('N|ES|WES|SENE')
    plot_course(res, maze)
    print(max(res.values()))
    print(sum(1 for x in res.values() if x >= 1000))
    # plot_course(res)