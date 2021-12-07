import unittest
from pprint import pprint
import itertools
import math


def read_data(filename):
    with open(filename) as f:
        return [int(l) for l in f.readline().split(',')]


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        data = read_data('input1.txt')
        mn, mx = min(data), max(data)
        print(f'min {mn} max {mx}')

        results = {}
        for p in range(mn, mx + 1):
            total = sum([abs(x - p) for x in data])
            results[total] = p

        winner = min(results.keys())
        print(f'position: {results[winner]} fuel {winner}')

    def test_part2(self):
        data = read_data('input1.txt')
        mn, mx = min(data), max(data)
        print(f'min {mn} max {mx}')

        results = {}
        for p in range(mn, mx + 1):
            total = sum([int((abs(x - p) + abs(x - p) ** 2) / 2) for x in data])
            results[total] = p

        winner = min(results.keys())
        print(f'position: {results[winner]} fuel {winner}')


if __name__ == '__main__':
    unittest.main()
