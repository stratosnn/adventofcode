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


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        data = read_data('input1.txt')
        used = set()
        end = (len(data) - 1, len(data[0]) - 1)
        dtra = []
        heapq.heappush(dtra, (0, (0, 0)))
        while dtra:
            l, p = heapq.heappop(dtra)
            if p == end:
                print(l)
                break
            # used.add(p)

            py, px = p
            neighbours = [(py, px - 1), (py, px + 1), (py + 1, px), (py - 1, px)]
            for ny, nx in filter(lambda ps: ps not in used and 0 <= ps[0] < len(data) and 0 <= ps[1] < len(data[0]), neighbours):
                heapq.heappush(dtra, (l + data[ny][nx], (ny, nx)))
                used.add((ny, nx))

        print('done')



def test_part2(self):
        pass


if __name__ == '__main__':
    unittest.main()
