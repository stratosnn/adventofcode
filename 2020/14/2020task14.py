import unittest
from pprint import pprint
import itertools
import math
import functools


def read_data(filename):
    mem = dict()
    bitmask0, bitmask1 = 0, 0  # bm0 for setting 0s and bm1 for 1s
    with open(filename) as f:
        for line in f:
            instr, _, data = line.strip().split(' ')
            if instr == 'mask':
                bitmap = {'0': 0, '1': 0, 'X': 0}
                for ix in range(len(data)):
                    offset = len(data) - ix - 1
                    bitmap[data[ix]] += 1 << offset
                bitmask0, bitmask1 = ~bitmap['0'], bitmap['1']
            else:
                addr = int(instr[4:-1])
                mem[addr] = int(data) & bitmask0 | bitmask1
    return mem


def read_data2(filename):
    mem = dict()
    mask = 0
    floating = []
    with open(filename) as f:
        for line in f:
            instr, _, data = line.strip().split(' ')
            if instr == 'mask':
                bitmap = {'0': [], '1': [], 'X': []}
                for ix in range(len(data)):
                    offset = len(data) - ix - 1
                    bitmap[data[ix]].append(offset)
                mask = functools.reduce(lambda s, o: s + (1 << o), bitmap['1'], 0)
                floating = bitmap['X']
            else:
                addr = int(instr[4:-1])
                for p in itertools.product([0, 1], repeat=len(floating)):
                    bitmap = {0: 0, 1: 0}
                    for ix in range(len(floating)):
                        bitmap[p[ix]] += (1 << floating[ix])
                    bm0, bm1 = ~bitmap[0], bitmap[1]
                    newaddr = (addr | mask) & bm0 | bm1
                    mem[newaddr] = int(data)
    return mem


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        mem = read_data('input14.txt')
        print(sum(mem.values()))

    def test_part2(self):
        mem = read_data2('input14.txt')
        print(sum(mem.values()))


if __name__ == '__main__':
    unittest.main()
