#!/usr/bin/env python3
import os, sys

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        sys.exit('No entries given.  Answer: unknown')

    if len(sys.argv) == 2:
        print('Loading file: {}'.format(sys.argv[1]))
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    else:
        lines = sys.argv

    frequency_list = [0]
    current_frequency = 0
    for l in lines:
        current_frequency += int(l)
        if current_frequency in frequency_list:
            print('Answer: {}'.format(current_frequency))
            sys.exit(None)
        frequency_list.append(current_frequency)
    
    # We probably won't get here...but if so...make sure
    print('Frequencies: {}'.format(frequency_list))
    print(len(frequency_list) == len(set(frequency_list)))
