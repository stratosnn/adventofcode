import unittest
from pprint import pprint
import itertools
import math


def read_data(filename):
    with open(filename) as f:
        return [[int(x) for x in l.strip()] for l in f.readlines()]


def octostep(data):
    # increase by one all
    for y in range(len(data)):
        for x in range(len(data[0])):
            data[y][x] = data[y][x] + 1

    # initial flash
    bfs, processed = set(), set()
    flashes = 0
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] > 9:
                bfs.add((y, x))
    # chain reaction
    while bfs:
        y, x = bfs.pop()
        if (y, x) not in processed and data[y][x] > 9:
            processed.add((y, x))
            neighbours = [(y + 1, x - 1), (y + 1, x), (y + 1, x + 1),
                          (y, x - 1), (y, x), (y, x + 1),
                          (y - 1, x - 1), (y - 1, x), (y - 1, x + 1)]
            for ny, nx in neighbours:
                if (0 <= ny < len(data)) and (0 <= nx < len(data[0])):
                    data[ny][nx] = data[ny][nx] + 1
                    bfs.add((ny, nx))
            flashes += 1

    # mark 0
    for y, x in processed:
        data[y][x] = 0

    return flashes


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        data = read_data('input1.txt')
        flashes = [octostep(data) for i in range(100)]
        print(flashes)
        print(sum(flashes))
        pass

    def test_part2(self):
        data = read_data('input1.txt')
        for i in range(999999):
            if octostep(data) == len(data) * len(data[0]):
                print(f'Sync step {i+1}')
                break


if __name__ == '__main__':
    unittest.main()
