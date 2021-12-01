import unittest
from pprint import pprint
import itertools
import math
import functools


def read_data(filename):
    with open(filename) as f:
        return [int(l.strip()) for l in f.readlines()]


def add_if_increasing(x, y):
    depth1, count1 = x
    depth2, _ = y
    return depth2, count1 + 1 if depth2 > depth1 else count1


def pre_process_part2(data):
    windows = [data[i:i+3] for i in range(len(data)-2)]
    assert all([len(item) == 3 for item in windows])
    return [sum(w) for w in windows]


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        depths = read_data('input1.txt')
        incs = functools.reduce(add_if_increasing, zip(depths, [0]*len(depths)))
        print(incs[1])

    def test_part2(self):
        depths = read_data('input1.txt')
        sliding_depths = zip(pre_process_part2(depths), [0]*len(depths))
        incs = functools.reduce(add_if_increasing, sliding_depths)
        print(incs[1])


if __name__ == '__main__':
    unittest.main()
