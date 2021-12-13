import unittest
from pprint import pprint
import itertools
import functools
import math
import copy
import collections


def read_data(filename):
    with open(filename) as f:
        coords, folds = set(), list()
        for line in f:
            if ',' in line:
                x, y = line.strip().split(',')
                coords.add((int(x), int(y)))
            elif 'y=' in line:
                folds.append((0, int(line.strip().split('=')[-1])))
            elif 'x=' in line:
                folds.append((int(line.strip().split('=')[-1]), 0))
        return coords, folds


def fold(coords, axis):
    fx, fy = axis
    foldable = {e for e in filter(lambda v: v[0] >= fx and v[1] >= fy, coords)}
    transformed = {(x, 2*fy - y) if fy > 0 else (2*fx - x, y) for (x, y) in foldable}
    return coords - foldable | transformed


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        coords, folds = read_data('input1.txt')
        print(len(fold(coords, folds[0])))
        pass

    def test_part2(self):
        coords, folds = read_data('input1.txt')
        for axis in folds:
            coords = fold(coords, axis)
        # visualize
        cols, rows = functools.reduce(lambda mx, e: (max(mx[0], e[0]), max(mx[1], e[1])), coords)
        display = [['.' for i in range(cols + 1)] for j in range(rows + 1)]
        for x, y in coords:
            display[y][x] = '#'
        for line in display:
            print(''.join(line))


if __name__ == '__main__':
    unittest.main()
