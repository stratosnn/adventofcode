import unittest
from pprint import pprint
import itertools
import math
from functools import reduce


def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda x, y: x*y, n)

    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    m = b
    x, y = 0, 1
    if b == 1:
        return 0

    while a > 1:
        q = a // b
        a, b = b, a % b
        x, y = y - q * x, x
    if y < 0:
        y += m
    return y


def read_data(filename):
    with open(filename) as f:
        first, second = f.readlines()
        return int(first), [x for x in map(int, filter(lambda x: x != 'x', second.split(',')))]


def read_data2(filename):
    with open(filename) as f:
        _, second = f.readlines()
        return [int(x) if x != 'x' else 'x' for x in second.strip().split(',')]


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        timestamp, schedule = read_data('input13.txt')
        print(schedule)
        rems = [timestamp % s for s in schedule]
        print(rems)
        diff = [a - b for (a, b) in zip(schedule, rems)]
        print(f'min {min(diff)} bus {schedule[diff.index(min(diff))]} mult {min(diff) * schedule[diff.index(min(diff))]}')

    def test_part2(self):
        schedule = enumerate(read_data2('input13.txt'))
        step = 1
        timestamp = 0

        n = []
        a = []
        for ix, bus in schedule:
            if bus == 'x':
                continue
            n.append(bus)
            a.append(bus - ix)

        print(chinese_remainder(n, a))

        # for ix, bus in schedule:
        #     done = False
        #     if bus == 'x':
        #         continue
        #     print(f'ix {ix}, {bus}, {timestamp}, {step}')
        #     while not done:
        #         timestamp += step
        #         if (timestamp + ix) % bus == 0:
        #             done = True
        #             step = timestamp
        #             print(f'DONE ix {ix}, {bus}, {timestamp}, {step}')

        print(timestamp)

        # 402251700208293 is not!



if __name__ == '__main__':
    unittest.main()
