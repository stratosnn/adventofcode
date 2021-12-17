import unittest
from pprint import pprint
import itertools
import functools
import math
import copy
import collections
import re


def read_data(filename):
    with open(filename) as f:
        line = f.readline().strip()
        spl = re.split('[ =.,]', line)
        xrange = (int(spl[3]), int(spl[5]))
        yrange = (int(spl[8]), int(spl[10]))
        return xrange, yrange


def in_range(p, cavern: tuple):
    xr, yr = cavern
    return xr[0] <= p[0] <= xr[1] and yr[0] <= p[1] <= yr[1]


def simulate(velocity: list, cavern: tuple):
    xr, yr = cavern
    p = [0, 0]
    mxy = 0
    while p[0] <= xr[1] and p[1] >= min(yr):
        mxy = max(mxy, p[1])
        if in_range(p, cavern):
            return mxy
        p = [p[0] + velocity[0], p[1] + velocity[1]]
        velocity = [velocity[0] - 1 if velocity[0] > 0 else 0, velocity[1] - 1]
    return None


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        rng = read_data('input1.txt')
        heights = []
        for vx in range(rng[0][1] + 1):
            for vy in range(max(map(abs, rng[1])) + 1):
                heights.append(simulate([vx, vy], rng))
        print(max(filter(lambda x: x is not None, heights)))

    def test_part2(self):
        rng = read_data('input1.txt')
        cnt = 0
        for vx in range(rng[0][1] + 1):
            for vy in range(min(rng[1]), max(map(abs, rng[1])) + 1):
                if simulate([vx, vy], rng) is not None:
                    cnt += 1
        print(cnt)


if __name__ == '__main__':
    unittest.main()
