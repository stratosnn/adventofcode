import unittest
from pprint import pprint
import itertools
import functools
import math
import copy
import collections
from functools import cache


def read_data(filename):
    with open(filename) as f:
        template = f.readline().strip()
        mapping = {}
        for line in f:
            if '->' in line:
                sp = line.strip().split(' ')
                mapping[(sp[0][0], sp[0][1])] = sp[2]
        return template, mapping


def transform(template, mapping):
    result = []
    for t in itertools.pairwise(template):
        result.append(t[0])
        result.append(mapping[t])
    result.append(template[-1])
    return result


@cache
def grow(pair, count=0):
    if count >= 40:
        return collections.Counter(pair[0])
    else:
        insert = MAPPING[pair]
        return grow((pair[0], insert), count + 1) + grow((insert, pair[1]), count + 1)


# bit of a cheat to make cache happy
TEMPLATE, MAPPING = read_data('input1.txt')


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        template, mapping = read_data('input1.txt')
        for i in range(10):
            print(template)
            template = transform(template, mapping)
        print(template)
        counter = collections.Counter(template)
        print(max(counter.values()) - min(counter.values()))

    def test_part2(self):
        counter = collections.Counter()
        for t in itertools.pairwise(TEMPLATE):
            counter += grow(t)
        print(max(counter.values()) - min(counter.values()) + 1)


if __name__ == '__main__':
    unittest.main()
