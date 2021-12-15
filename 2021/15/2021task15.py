import unittest
from pprint import pprint
import itertools
import functools
import math
import copy
import collections
import heapq


def read_data(filename):
    with open(filename) as f:
        return [[int(x) for x in l.strip()] for l in f.readlines()]


def weight(data: list, y, x):
    my, mx = len(data), len(data[0])
    oy, ox = y // my, x // mx
    ry, rx = y % my, x % mx
    w = data[ry][rx] + oy + ox
    return w if w < 10 else (w % 10) + (w // 10)  # wrap around to 1 magic


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        data = read_data('input1.txt')
        end = (len(data) - 1, len(data[0]) - 1)
        dtra, used = [], set()
        heapq.heappush(dtra, (0, (0, 0)))
        p = None
        while dtra and p != end:
            l, (py, px) = heapq.heappop(dtra)
            neighbours = [(py, px - 1), (py, px + 1), (py + 1, px), (py - 1, px)]
            for ny, nx in filter(lambda p: p not in used and 0 <= p[0] <= end[0] and 0 <= p[1] <= end[1], neighbours):
                heapq.heappush(dtra, (l + data[ny][nx], (ny, nx)))
                used.add((ny, nx))
        print(l)

    def test_part2(self):
        data = read_data('input1.txt')
        end = (5*len(data) - 1, 5*len(data[0]) - 1)
        dtra, used = [], set()
        heapq.heappush(dtra, (0, (0, 0)))
        p = None
        while dtra and p != end:
            l, (py, px) = heapq.heappop(dtra)
            neighbours = [(py, px - 1), (py, px + 1), (py + 1, px), (py - 1, px)]
            for ny, nx in filter(lambda p: p not in used and 0 <= p[0] <= end[0] and 0 <= p[1] <= end[1], neighbours):
                heapq.heappush(dtra, (l + weight(data, ny, nx), (ny, nx)))
                used.add((ny, nx))
        print(l)


if __name__ == '__main__':
    unittest.main()
