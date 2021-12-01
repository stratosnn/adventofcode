import unittest
import itertools
from copy import deepcopy
from pprint import pprint


def read_data(filename):
    with open(filename) as f:
        return [[c for c in x.strip()] for x in f.readlines()]


def occupied(x, y, data):
    mxx = len(data[0])
    mxy = len(data)
    coords = []
    for ix in [x-1, x, x+1]:
        for iy in [y-1, y, y+1]:
            if 0 <= ix < mxx and 0 <= iy < mxy and (ix, iy) != (x, y):
                coords.append((ix, iy))
    return sum(map(lambda p: data[p[1]][p[0]] == '#', coords))


def occupied2(x, y, data):
    mxx = len(data[0])
    mxy = len(data)
    vectors = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
    coords = []
    occ = 0

    for v in vectors:
        (ix, iy) = deepcopy((x, y))
        ix, iy = ix + v[0], iy + v[1]
        while 0 <= ix < mxx and 0 <= iy < mxy and data[iy][ix] != 'L':
            if data[iy][ix] == '#':
                occ += 1
                break
            ix, iy = ix + v[0], iy + v[1]

    return occ


def round1(data):
    cnt = 0
    nd = deepcopy(data)
    for iy in range(len(data)):
        for ix in range(len(data[0])):
            if data[iy][ix] == 'L' and occupied(ix, iy, data) == 0:
                nd[iy][ix] = '#'
                cnt += 1
    return nd, cnt


def round2(data):
    cnt = 0
    nd = deepcopy(data)
    for iy in range(len(data)):
        for ix in range(len(data[0])):
            if data[iy][ix] == '#' and occupied(ix, iy, data) >= 4:
                nd[iy][ix] = 'L'
                cnt += 1
    return nd, cnt


def round21(data):
    cnt = 0
    nd = deepcopy(data)
    for iy in range(len(data)):
        for ix in range(len(data[0])):
            if data[iy][ix] == 'L' and occupied2(ix, iy, data) == 0:
                nd[iy][ix] = '#'
                cnt += 1
    return nd, cnt


def round22(data):
    cnt = 0
    nd = deepcopy(data)
    for iy in range(len(data)):
        for ix in range(len(data[0])):
            if data[iy][ix] == '#' and occupied2(ix, iy, data) >= 5:
                nd[iy][ix] = 'L'
                cnt += 1
    return nd, cnt


class MyTestCase(unittest.TestCase):
    def test_something(self):
        data = read_data('input11.txt')
        cnt = 1
        while cnt > 0:
            #pprint(data)
            #print()
            data, cnt = round1(data)
            #pprint(data)
            #print()
            if cnt == 0:
                break
            data, cnt = round2(data)

        print(sum([x.count('#') for x in data]))

    def test_something2(self):
        data = read_data('input11.txt')
        cnt = 1
        while cnt > 0:
            #pprint(data)
            #print()
            data, cnt = round21(data)
            #pprint(data)
            #print()
            if cnt == 0:
                break
            data, cnt = round22(data)

        print(sum([x.count('#') for x in data]))


if __name__ == '__main__':
    unittest.main()
