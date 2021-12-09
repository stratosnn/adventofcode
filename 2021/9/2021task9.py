import unittest
from pprint import pprint
import itertools
import math
import functools


def read_data(filename):
    with open(filename) as f:
        return [[int(c) for c in l.strip()] for l in f.readlines()]


def prepare_data(raw_data):
    data = [[9]*(len(raw_data[0]) + 2)]
    for line in raw_data:
        data.append([9] + line + [9])
    data.append([9]*(len(raw_data[0]) + 2))
    return data


def find_lows(data):
    mins = dict()
    for y in range(1, len(data)-1):
        for x in range(1, len(data[0])-1):
            if data[y][x] < data[y][x-1] and data[y][x] < data[y][x+1] and \
                    data[y][x] < data[y-1][x] and data[y][x] < data[y+1][x]:
                mins[(y, x)] = data[y][x] + 1
    return mins


def basin_bfs(mins, data):
    basins = []
    for pos in mins:
        processed = []
        bfs = [pos]
        while bfs:
            p = bfs.pop(0)
            processed.append(p)
            y, x = p
            neighbours = [(y, x - 1), (y, x + 1), (y - 1, x), (y + 1, x)]
            for n in neighbours:
                ny, nx = n
                if (n not in processed) and (n not in bfs) and (9 > data[ny][nx] > data[y][x]):
                    bfs.append(n)
        basins.append(processed)
    return basins


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        raw_data = read_data('input1.txt')
        data = prepare_data(raw_data)
        mins = find_lows(data)
        print(sum(mins.values()))

    def test_part2(self):
        raw_data = read_data('input1.txt')
        data = prepare_data(raw_data)
        mins = find_lows(data)
        basins = basin_bfs(mins, data)

        top3 = [x for x in reversed(sorted([len(b) for b in basins]))][0:3]
        print(top3)
        print(functools.reduce(lambda a, b: a*b, top3))




if __name__ == '__main__':
    unittest.main()
