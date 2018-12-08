#!/usr/bin/env python3
import os, sys
import networkx as nx 

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

from utils.timeit import timeit


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
        
    @timeit
    def construct_graph():
        g = nx.DiGraph()
        for line in lines:
            head, tail = line[5], line[36]
            g.add_edge(head, tail)
        return g

    g = construct_graph()
    
    print(f'Answer: {"".join(nx.lexicographical_topological_sort(g))}')

# BFGKNRTWXIHPUMLVQZOYJACDSE # bad
# BFGKNRTWXIHPUMLQVZOYJACDSE # good