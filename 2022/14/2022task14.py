import unittest
from pprint import pprint
import itertools
import functools
import math
import copy
import collections


def clamp(offset: tuple, max_val: int = 1):
    return offset[0] // max(1, abs(offset[0] // max_val)), offset[1] // max(1, abs(offset[1] // max_val))


def shift(p: tuple, offset: tuple):
    return p[0] + offset[0], p[1] + offset[1]


def read_data(filename):
    with open(filename) as f:
        return [[tuple(map(int, p.split(','))) for p in l.strip().split(' -> ')] for l in f.readlines()]


def build_grid(data: list):
    grid = {}
    for l in data:
        for s, e in itertools.pairwise(l):
            offset = clamp((e[0] - s[0], e[1] - s[1]))
            while s != e:
                grid[s] = '#'
                s = shift(s, offset)
            grid[e] = '#'
    return grid


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        data = read_data('input14.txt')
        grid = build_grid(data)
        lowest = max(map(lambda x: x[1], grid.keys()))
        h, p = (500, 0), (500, 0)
        while p[1] < lowest:
            if shift(p, (0, 1)) not in grid:
                p = shift(p, (0, 1))
            elif shift(p, (-1, 1)) not in grid:
                p = shift(p, (-1, 1))
            elif shift(p, (1, 1)) not in grid:
                p = shift(p, (1, 1))
            else:
                grid[p] = 's'
                p = h
        print(len(list(filter(lambda x: x == 's', grid.values()))))

    def test_part2(self):
        data = read_data('input14.txt')
        grid = build_grid(data)
        lowest = max(map(lambda x: x[1], grid.keys()))

        for x in range(-(500**2), (500**2)):
            s = (x, lowest + 2)
            grid[s] = '#'

        h, p = (500, 0), (500, 0)
        while True:
            if shift(p, (0, 1)) not in grid:
                p = shift(p, (0, 1))
            elif shift(p, (-1, 1)) not in grid:
                p = shift(p, (-1, 1))
            elif shift(p, (1, 1)) not in grid:
                p = shift(p, (1, 1))
            else:
                grid[p] = 's'
                if p == h:
                    break
                p = h
        print(len(list(filter(lambda x: x == 's', grid.values()))))


if __name__ == '__main__':
    unittest.main()
