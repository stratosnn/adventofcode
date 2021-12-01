import unittest
from pprint import pprint
import itertools
import math
import functools


def read_data(filename):
    with open(filename) as f:
        return [int(c) for c in f.readline().strip()]


PATTERN = [0, 1, 0, -1]


def single_pattern(ix, length):
    lst = []
    for p in PATTERN:
        lst += [p] * (ix + 1)
    result = lst * (math.ceil(length / len(lst)) + 1)
    return result[1:length+1]


def pattern_list(length):
    return [single_pattern(i, length) for i in range(length)]


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        reps = 100
        data = read_data('input16.txt')
        pattern = pattern_list(len(data))
        #print(pattern)
        #print(data)
        assert len(pattern) == len(data)
        assert len(pattern[0]) == len(data)

        for r in range(reps):
            data = [abs(sum(map(lambda x, y: x*y, data, pattern[i]))) % 10 for i in range(len(data))]
            #print(data)

        print(''.join(map(str,data[:8])))


    def test_part2(self):
        pass


if __name__ == '__main__':
    unittest.main()
