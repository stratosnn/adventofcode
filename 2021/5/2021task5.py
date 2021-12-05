import unittest
from pprint import pprint
import itertools
import math


def read_data(filename):
    with open(filename) as f:
        pipes = []
        for line in f:
            raw = line.split()
            start = raw[0].split(',')
            end = raw[2].split(',')
            pipes.append(((int(start[0]), int(start[1])), (int(end[0]), int(end[1]))))
        return pipes


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        pipes = read_data('input1.txt')
        strait = filter(lambda p: p[0][0] == p[1][0] or p[0][1] == p[1][1], pipes)
        fmap = dict()
        for p1, p2 in strait:
            (x1, y1), (x2, y2) = p1, p2

            if x1 == x2:
                offset = 1 if y1 < y2 else -1
                for y in range(y1, y2 + offset, offset):
                    fmap[(x1, y)] = fmap.setdefault((x1, y), 0) + 1
            elif y1 == y2:
                offset = 1 if x1 < x2 else -1
                for x in range(x1, x2 + offset, offset):
                    fmap[(x, y1)] = fmap.setdefault((x, y1), 0) + 1
            else:
                assert 0, "something went wrong"

        danger_points = [x for x in filter(lambda p: p > 1, fmap.values())]
        print(len(danger_points))

    def test_part2(self):
        pipes = read_data('input1.txt')
        fmap = dict()
        for p1, p2 in pipes:
            (x1, y1), (x2, y2) = p1, p2

            # normalize offset
            offset = tuple([x for x in map(lambda v: int(v / abs(v)) if v != 0 else 0, (x2 - x1, y2 - y1))])
            cp = p1
            while cp != p2:
                fmap[cp] = fmap.setdefault(cp, 0) + 1
                cp = (cp[0] + offset[0], cp[1] + offset[1])
            fmap[cp] = fmap.setdefault(cp, 0) + 1  # last point

        danger_points = [x for x in filter(lambda p: p > 1, fmap.values())]
        print(len(danger_points))


if __name__ == '__main__':
    unittest.main()
