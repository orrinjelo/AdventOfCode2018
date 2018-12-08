#!/usr/bin/env python3
import os, sys
from collections import defaultdict

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

from utils.timeit import timeit

class Graph:
    def __init__(self):
        self.__graph = defaultdict(list)
        self.__visited = {}
        
    def add_edge(self, u, v):
        self.__graph[u].append(v)
        self.__graph[u].sort(reverse=True)
        self.__visited[u] = False
        self.__visited[v] = False
        
    def _topological_sort_util(self, v, stack):
        self.__visited[v] = True
        for i in sorted(self.__graph[v], reverse=True):
            if not self.__visited[i]:
                self._topological_sort_util(i, stack)
        stack.insert(0, v)
        return stack
        
    @timeit    
    def topological_sort(self):
        stack = []
        for i in sorted(list(self.__visited.keys()), reverse=True):
            if not self.__visited[i]:
                stack = self._topological_sort_util(i, stack)
        
        return stack

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
        g = Graph()
        for line in lines:
            head, tail = line[5], line[36]
            g.add_edge(head, tail)
        return g

    g = construct_graph()
    
    print(f'Answer: {"".join(g.topological_sort())}')