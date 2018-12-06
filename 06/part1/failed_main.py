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

history = None

@timeit
def make_field(points):
    global history
    min_x = min(min(points)[0], 0)
    max_x = max(points)[0]
    min_y = min(min(points, key=itemgetter(1))[1], 0)
    max_y = max(points, key=itemgetter(1))[1]
    field = np.zeros((max_x + 1, max_y + 1), dtype=int)
    history = np.zeros((max_x + 1, max_y + 1), dtype=bool)

    for i in range(len(points)):
        point = points[i]
        field[point[0],point[1]] = i+1

    return field

@timeit
def infect_full(field, points):
    global history
    def infect_single_step(field):
        def check_cell(field, x, y, p):
            global history
            if field[x,y] == p + 1 or field[x,y] == -1: # No touch!
                return 
            elif field[x,y] == 0: # claim it!
                field[x,y] = p + 1
            elif field[x,y] > 0 and not history[x,y]: # clash!
                field[x,y] = -1
        max_point = np.max(field) # Number of viruses
        X,Y = field.shape
        for p in range(max_point):
            claimed = np.where(field == p+1)
            for s in range(len(claimed[0])):
                spot = claimed[0][s], claimed[1][s]
                if spot[0] > 0: # Check West
                    check_cell(field, spot[0]-1, spot[1], p)
                if spot[0] < X-1: # Check East
                    check_cell(field, spot[0]+1, spot[1], p)
                if spot[1] > 0: # Check North
                    check_cell(field, spot[0], spot[1]-1, p)
                if spot[1] < Y-1: # Check South
                    check_cell(field, spot[0], spot[1]+1, p)
    while len(np.where(field == 0)[0]) != 0:
        infect_single_step(field)
        history[field != 0] = True
        # print_field(field)
        # print()


    return field

@timeit
def day6_part6(input):
    points = parse_lines(input)
    field = make_field(points)
    infect_full(field, points)
    print_field(field)
    return None
    

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

        print(f'Answer: {day6_part6(lines)}')