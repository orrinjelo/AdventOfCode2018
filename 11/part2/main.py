#!/usr/bin/env python3
import os, sys
import numpy as np 
from scipy import optimize
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

from utils.timeit import timeit

class FuelCells:
    def __init__(self, serial_number):
        self.serial_no = serial_number
        self.grid = np.zeros((301, 301), dtype=int)
        self.grid[1:,1:] = self.powerLevel(np.arange(1,301), np.arange(1,301))

    def rackId(self, x, y=None):
            return x + 10

    def powerLevel(self, x, y):
        getHundreds = lambda x: ((x - (x % 100)) // 100) - ((x // 1000)*10)
        if type(x) == int:
            xx, yy = x, y
            power = self.rackId(xx) * yy
        else:
            xx, yy = np.meshgrid(x, y, sparse=True)
            power = np.transpose(np.multiply(self.rackId(np.arange(1,301)), 1) * yy)
        power += self.serial_no
        power = np.multiply(power, np.transpose(self.rackId(xx, yy)))
        power = getHundreds(power)
        power -= 5
        return power

    def collection(self, x, y, size):
        xx = x #+ 1
        yy = y #+ 1

        # if xx < size//2 or xx > 300-size//2 or yy < size//2 or yy > 300-size//2:
        #     print(f'Invalid index: {xx},{yy}')
        #     return 0

        return np.sum(self.grid[xx:xx+size,yy:yy+size])

    def maxCollection(self):
        best = (0, (0, 0, 0))
        for s in range(1,300):
            print(f'Size: {s}')
            for x in range(1,300-s+1):
                for y in range(1,300-s+1):
                    try:
                        z = self.collection(x,y,s)
                    except:
                        continue
                    if z > best[0]:
                        best = (z, (x, y, s))

        return best


if __name__ == '__main__':
    # Parse args, parse number list
    if len(sys.argv) <= 1:
        sys.exit('No entries given.  Answer: unknown')

    if len(sys.argv) == 2:
        x = int(sys.argv[1])
    else:
        sys.exit('Too many args.')
        
    fc = FuelCells(x)

    import matplotlib.pyplot as plt 
    plt.imshow(fc.grid)
    plt.show()
    # print(fc.collection(90,269,16))
    print(fc.maxCollection())