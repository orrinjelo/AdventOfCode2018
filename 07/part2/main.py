#!/usr/bin/env python3
import os, sys
import networkx as nx
import numpy as np 
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

from utils.timeit import timeit

class Scheduler:
    class Worker:
        def __init__(self, idno=0, scheduler=None):
            self.task = None
            self.task_time = 0
            self.__scheduler = scheduler
            self.idno = idno
            self.history = []
        def doWork(self):
            if self.task:
                for dependency in self.__scheduler.dependency(self.task):
                    if not dependency in self.__scheduler.finished:
                        self.history.append('.')
                        return
                self.task_time += 1
            else:
                self.history.append('.')
                return
            # if self.isFinished():
            self.history.append(self.task)
        def isFinished(self):
            return ord(self.task) - 64 + self.__scheduler.base_time == self.task_time

        def assignWork(self, job):
            self.task = job
            self.task_time = 0

    def __init__(self, graph, task_list, base_time=60, n_workers=5):
        self.__graph = graph
        self.__time = 0
        self.__base_time = base_time
        self.__workers = []
        self.__task_list = list(task_list)
        self.__n_tasks = len(self.__task_list)
        self.__task_pointer = 0
        self.__finished = []
        self.__dependencies = {}

        self._timecard = {}

        for n in range(n_workers):
            self.__workers.append(self.Worker(n, self))
            self._timecard[n] = 0
            if n == 0:
                assignment = self.__task_list[0]
                self.__workers[0].assignWork(assignment)
                self.__task_list.remove(assignment)


    @property
    def base_time(self):
        return self.__base_time

    @property
    def dependencies(self):
        return self.__dependencies

    @property
    def finished(self):
        return self.__finished
    
    def _run_step(self):
        # Assign tasks
        for worker in self.__workers:
            if not worker.task:
                if not self.__task_list:
                    worker.task = None
                else:
                    priority = 'z'
                    for task in self.__task_list:
                        # print(task, self.is_dependent(task), self.dependency(task))
                        if not self.is_dependent(task):
                            # print('x', task, priority)
                            if ord(priority) > ord(task):
                                priority = task
                    
                    if priority != 'z' and not self.is_dependent(priority):
                        self.__task_list.remove(priority)
                        worker.assignWork(priority)

            worker.doWork()

            # print(self.__finished)

        for worker in self.__workers:
            if worker.task and worker.isFinished():
                self._timecard[worker.idno] += worker.task_time
                self.__finished.append(worker.task)
                worker.task = None

        self.__time += 1

    @timeit
    def run(self):
        while self.__n_tasks != len(self.__finished):
            self._run_step()
        print(self.__time)
        # print(self._timecard)
        # print(self.__finished)

        # for w in self.__workers:
        #     print(w.history)

    def dependency(self,n):
        if not n in self.__dependencies:
            self.__dependencies[n] = [x[0] for x in self.__graph.edges() if x[1] == n]
        
        return self.__dependencies[n]

    def is_dependent(self, n):
        for x in self.dependency(n):
            if not x in self.finished:
                return True
        return False




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

    steps = list(nx.lexicographical_topological_sort(g))

    print(''.join(steps))

    s = Scheduler(g, steps, 60, 5)
    s.run()


