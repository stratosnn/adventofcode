import unittest
from pprint import pprint
import itertools
import math
from operator import add


def read_data(filename):
    positions = dict()
    with open(filename) as f:
        for iy, l in enumerate(f.readlines()):
            for ix, c in enumerate(l.strip()):
                positions[(ix, iy, 0)] = 1 if c == '#' else 0
        return positions


def read_data4d(filename):
    positions = dict()
    with open(filename) as f:
        for iy, l in enumerate(f.readlines()):
            for ix, c in enumerate(l.strip()):
                positions[(ix, iy, 0, 0)] = 1 if c == '#' else 0
        return positions

def get_neighbours_gen(point):
    d = len(point)
    skip = tuple(0 for i in range(d))
    for offset in itertools.product([-1, 0, 1], repeat=d):
        if offset == skip:
            continue
        yield tuple(map(add, offset, point))


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        pos = read_data('input17.txt')
        #print(pos)
        #print(len(tuple(get_neighbours_gen((5, 5, 5)))))
        for i in range(6):
            new_pos = {}
            for p in pos:
                for n in get_neighbours_gen(p):
                    if n in new_pos:
                        continue
                    s = sum([pos.get(x, 0) for x in get_neighbours_gen(n)])
                    if pos.get(n, 0) == 1 and 2 <= s <= 3:
                        new_pos[n] = 1
                    elif pos.get(n, 0) == 0 and s == 3:
                        new_pos[n] = 1
                    else:
                        new_pos[n] = 0
            pos = new_pos

        print(sum(pos.values()))

    def test_part2(self):
        pos = read_data4d('input17.txt')
        for i in range(6):
            new_pos = {}
            for p in pos:
                for n in get_neighbours_gen(p):
                    if n in new_pos:
                        continue
                    s = sum([pos.get(x, 0) for x in get_neighbours_gen(n)])
                    if pos.get(n, 0) == 1 and 2 <= s <= 3:
                        new_pos[n] = 1
                    elif pos.get(n, 0) == 0 and s == 3:
                        new_pos[n] = 1
                    else:
                        new_pos[n] = 0
            pos = new_pos
        print(sum(pos.values()))

if __name__ == '__main__':
    unittest.main()
