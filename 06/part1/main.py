#!/usr/bin/env python3
import os, sys
import numpy as np
from operator import itemgetter
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

from utils.timeit import timeit

def print_field(f):
    X,Y = f.shape
    for y in range(Y):
        for x in range(X):
            print(f[x,y] if f[x,y] > 0 else '.', end='')
        print('')

@timeit
def parse_lines(lines):
    return [tuple(map(lambda x: int(x), line.split(','))) for line in lines]

@timeit
def make_field(points):
    min_x = min(min(points)[0], 0)
    max_x = max(points)[0]
    min_y = min(min(points, key=itemgetter(1))[1], 0)
    max_y = max(points, key=itemgetter(1))[1]
    field = np.zeros((max_x + 1, max_y + 1), dtype=int)

    for i in range(len(points)):
        point = points[i]
        field[point[0],point[1]] = i+1

    return field

@timeit
def infect_full(field, points):
    X,Y = field.shape
    def calc_distance(x,y,p):  # Try L2, P-norm, or Max!
        return abs(p[0]-x) + abs(p[1]-y)
    for x in range(X):
        for y in range(Y):
            best = (0, X+Y) 
            if field[x,y] != 0:
                continue
            for p in range(len(points)):
                dist = calc_distance(x,y,points[p])
                if dist == best[1]:
                    best = (-1, dist)
                elif dist < best[1]:
                    best = (p+1, dist)
            field[x, y] = best[0]
    return field

@timeit
def count_territories(field, max_points):
    X,Y = field.shape
    rulers = [_+1 for _ in range(max_points)]
    # Inspect the borders
    north = field[:,0]
    south = field[:,Y-1]
    west  = field[0,:]
    east  = field[X-1,:]

    ns_join = np.concatenate((np.intersect1d(rulers, north), np.intersect1d(rulers, south)))
    we_join = np.concatenate((np.intersect1d(rulers, west), np.intersect1d(rulers, east)))
    all_join = np.concatenate((ns_join, we_join))
    disqualified = np.unique(all_join)
    qualified = np.setxor1d(rulers, disqualified)
    
    # Count cells in territory
    kingdoms = {}
    for king in qualified:
        kingdoms[king] = np.sum(field == king)

    return kingdoms

@timeit
def day6_part1(input, do_plot=False):
    points = parse_lines(input)
    field = make_field(points)
    infect_full(field, points)
    k = count_territories(field, len(points))

    if do_plot:
        import matplotlib.pyplot as plt 
        from matplotlib import cm
        plt.figure(1)
        plt.imshow(field, interpolation='none', cmap='gist_ncar')
        plt.show()

    return max(k.items(), key=itemgetter(1))[1]
    

if __name__ == '__main__':
    # Argument parsing
    if len(sys.argv) <= 1:
        sys.exit('No entries given.  Answer: 0')

    if len(sys.argv) > 2:
        sys.exit('Too many arguments.')

    # Load file
    print('Loading file: {}'.format(sys.argv[1]))
    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()

        print(f'Answer: {day6_part1(lines, False)}')