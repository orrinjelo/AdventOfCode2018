#!/usr/bin/env python3
import os, sys
import numpy as np 
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

from utils.timeit import timeit

class Elf:
    def __init__(self, start):
        self.pos = start

    def advance(self, recepe_list, max_idx):
        self.pos += recepe_list[self.pos] + 1
        self.pos = self.pos % max_idx

    def score(self, recepe_list):
        return recepe_list[self.pos]

@timeit
def search_sequence_numpy(arr,seq):
    # Store sizes of input array and sequence
    Na, Nseq = arr.size, seq.size

    # Range of sequence
    r_seq = np.arange(Nseq)

    # Create 2D array of sliding indices across entire length of input array.
    # Match up with the input sequence & get the matching starting indices.
    M = (arr[np.arange(Na-Nseq+1)[:,None] + r_seq] == seq).all(1)

    # Get the range of those indices as final output
    if M.any()>0:
        return np.where(np.convolve(M,np.ones((Nseq),dtype=int))>0)[0]
    else:
        return []         # No match found        

if __name__ == '__main__':
    # Parse args, parse number list
    if len(sys.argv) <= 1:
        sys.exit('No entries given.  Answer: unknown')

    if len(sys.argv) == 2:
        input_val = int(sys.argv[1])
    else:
        sys.exit('Too many args.')
    
    scores = np.zeros(input_val*2, dtype=int)
    scores[0:2] = [3,7]
    score_ptr = 2

    buddy = Elf(0)
    legolas = Elf(1)

    def step():
        global scores, score_ptr, buddy, legolas
        new_score = buddy.score(scores) + legolas.score(scores)
        new_scores = [int(x) for x in list(str(new_score))]

        if score_ptr+len(new_scores) > len(scores):
            resized_scores = np.zeros(len(scores)*2, dtype=int)
            resized_scores[:len(scores)] = scores
            scores = resized_scores

        # print(score_ptr,len(new_scores))
        scores[score_ptr:score_ptr+len(new_scores)] = new_scores
        score_ptr += len(new_scores)

        buddy.advance(scores, score_ptr)
        legolas.advance(scores, score_ptr)

    @timeit
    def part1():
        global input_val
        for _ in range(input_val+10):
            step()


    part1()

    if input_val > len(scores) - 10:
        forward_slice = np.concatenate(scores[input_val:score_ptr], scores[:10-(len(scores) - input_val)])
    else:
        forward_slice = scores[input_val:input_val+10]

    # if input_val < 10:
    #     # backward_slice = np.concatenate(scores[len(scores)-(11-input_val):len(scores)], scores[:input_val])
    #     backward_slice = np.concatenate((scores[score_ptr-(10-input_val):score_ptr], scores[:input_val]))
    # else:
    #     backward_slice = scores[input_val-10:input_val]

    print('Part 1:',''.join([str(_) for _ in forward_slice]))

    # print(''.join([str(_) for _ in backward_slice]))

    @timeit
    def part2():
        ans = []
        while len(ans) == 0:
            for _ in range(100000):
                step()

            arrayd = np.array([int(_) for _ in list(str(input_val))])
            ans = search_sequence_numpy(scores,arrayd)
        return ans

    ans = part2()
    # print(arrayd)

    print('Part 2:', ans[0])
