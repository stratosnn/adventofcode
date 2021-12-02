import unittest
from pprint import pprint
import itertools
import math


def read_data(filename):
    with open(filename) as f:
        return [tuple(l.strip().split()) for l in f.readlines()]


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        cf, cd = 0, 0
        for action, step in read_data('input1.txt'):
            si = int(step)
            if action == 'forward':
                cf = cf + si
            elif action == 'down':
                cd = cd + si
            elif action == 'up':
                cd = cd - si
        print(cf*cd)


    def test_part2(self):
        cf, cd, ca = 0, 0, 0
        for action, step in read_data('input1.txt'):
            si = int(step)
            if action == 'forward':
                cf = cf + si
                cd = cd + ca * si
            elif action == 'down':
                ca = ca + si
            elif action == 'up':
                ca = ca - si
        print(cf*cd)


if __name__ == '__main__':
    unittest.main()
