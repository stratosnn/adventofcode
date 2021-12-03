import unittest
from pprint import pprint
import itertools
import math
import ctypes
import copy


def read_data(filename):
    with open(filename) as f:
        return [int(l.strip(), 2) for l in f.readlines()]


def get_gamma_and_epsilon(data):
    max_len = int(math.log2(max(data))) + 1
    gamma = 0
    for offset in range(max_len):
        count = sum(map(lambda x: (x >> offset) & 1, data))
        gamma = gamma + ((1 if count > len(data)/2 else 0) << offset)
    epsilon = ~gamma & ((2 ** max_len)-1)
    print(gamma, epsilon, gamma * epsilon)
    return gamma, epsilon


def split_filter(func, data):
    yes, no = [], []
    for x in data:
        if func(x):
            yes.append(x)
        else:
            no.append(x)
    return yes, no


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        data = read_data('input1.txt')
        get_gamma_and_epsilon(data)

    def test_part2(self):
        data = read_data('input1.txt')
        max_len = int(math.log2(max(data))) + 1
        # oxygen
        oxygen = copy.deepcopy(data)
        for offset in reversed(range(max_len)):
            #print(f' len oxygen {len(oxygen)}')
            yes, no = split_filter(lambda x: (x >> offset) & 1 == 1, oxygen)
            if len(yes) == len(no):
                oxygen = yes
            else:
                oxygen = yes if len(yes) > len(no) else no

            if len(oxygen) == 1:
                print(f'oxygen {oxygen[0]}')
                break

        # co2
        co2 = copy.deepcopy(data)
        for offset in reversed(range(max_len)):
            #print(f' len co2 {len(co2)}')
            yes, no = split_filter(lambda x: (x >> offset) & 1 == 1, co2)
            if len(yes) == len(no):
                co2 = no
            else:
                co2 = no if len(no) < len(yes) else yes

            if len(co2) == 1:
                print(f'co2 {co2[0]}')
                break
        print(f'result {oxygen[0] * co2[0]}')



if __name__ == '__main__':
    unittest.main()
