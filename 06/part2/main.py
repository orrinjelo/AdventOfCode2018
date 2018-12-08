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
            print(f"{f[x,y] if f[x,y] > 0 else '..':2} ", end='')
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

    return field

@timeit
def infect_full(field, points):
    X,Y = field.shape
    def calc_distance(x,y,p):
        return abs(p[0]-x) * abs(p[1]-y)
    for x in range(X):
        for y in range(Y):
            best = (0, X+Y) 
            if field[x,y] != 0:
                continue
            for p in range(len(points)):
                dist = calc_distance(x,y,points[p])
                field[x, y] += dist            
    return field


@timeit
def day6_part2(input):
    points = parse_lines(input)
    field = make_field(points)
    infect_full(field, points)
    res = len(np.where(field < 10000)[0])

    return res 
    

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

        print(f'Answer: {day6_part2(lines)}')