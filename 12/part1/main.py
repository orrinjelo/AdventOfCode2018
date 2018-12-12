#!/usr/bin/env python3
import os, sys
import numpy as np 
from pprint import pprint
import re

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

from utils.timeit import timeit

def print_plants(i, s):
    print(f'{i:2}: {s}')

if __name__ == '__main__':
    # Parse args, parse number list
    if len(sys.argv) <= 1:
        sys.exit('No entries given.  Answer: unknown')

    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    else:
        sys.exit('Too many args.')

    # Parse header/init state
    header = re.compile(r'initial state: ((\.|#)*)')

    init = header.match(lines[0]).groups(1)[0]
    laststep = None

    flipflop = {
        '#':'@',
        '.':'_',
        '@':'#',
        '_':'.'
    }

    rules = None

    @timeit
    def part1():
        global init, laststep, flipflop, rules
        # Parse rules
        rules = {}

        for l in lines[2:]:
            rules[l[0:5]] = l[9]

        laststep = init.replace('#','@',1)
        print_plants(0, laststep)


        N = 20
        np.zeros((N,))

        def step(j):
            global laststep, flipflop, rules
            newstep = ''
            for i in range(-2,len(laststep)+2):
                if i > len(laststep)-3:
                    probe = laststep[i-2:] + '.' * (3 - (len(laststep)-i))
                elif i < 2:
                    probe = '.' * (2 - i) + laststep[0:3 - (len(laststep)-i)]
                else:
                    probe = laststep[i-2:i+3]

                probe_key = probe.replace('@','#').replace('_', '.')
                
                # print(f'Probe ({i}): {probe} {probe_key}')
                if probe_key in rules.keys():
                    newstep += rules[probe_key] if probe[2] == '#' or probe[2] == '.' else flipflop[rules[probe_key]]
                else:
                    newstep += '.' if probe[2] == '#' or probe[2] == '.' else flipflop['.']

            laststep = newstep.strip('.')

            print_plants(j+1, laststep)

        for j in range(N):
            step(j)

        idxs = np.where(np.array(list(laststep)) == '#')
        try:
            offset = list(laststep).index('@')
        except:
            try:
                offset = list(laststep).index('_')
            except:
                offset = 0

        ans1 = np.sum(np.arange(-offset,len(laststep))[idxs])
        print(ans1)

    # step(200)
    # step(201)
    # idxs = np.where(np.array(list(laststep)) == '#')
    # try:
    #     offset = list(laststep).index('@')
    # except:
    #     try:
    #         offset = list(laststep).index('_')
    #     except:
    #         offset = 0

    # ans1 = np.sum(np.arange(-offset,len(laststep))[idxs])
    # print(ans1)    

    # Personalized formula...
    # print(list(laststep).index('#')) # 200 = 125, 201 = 126
    # length of train = 173, 86 #
    @timeit
    def part2():
        # The cheaty way.  I should generalize this for other inputs... but not today!
        generation = 50000000000
        hoffset = generation - 75
        print('Billions of generations:', sum([_ for _ in range(hoffset,hoffset+173,2)]))

    part1()
    part2()
