import unittest
from pprint import pprint
import itertools
import math
import collections


def read_data(filename):
    with open(filename) as f:
        return [int(x) for x in f.readline().split(',')]


def preprocess_input(i: list):
    population = collections.defaultdict(int)
    for e in i:
        population[e] = population[e] + 1
    return population


def simulation(pop: dict, days: int):
    new_pop = None
    for r in range(days):
        new_pop = collections.defaultdict(int)
        new_gen = pop.pop(0, 0)
        new_pop[8] = new_gen
        for k, v in pop.items():
            new_pop[k-1] = v
        new_pop[6] = new_pop[6] + new_gen
        pop = new_pop

    return sum(new_pop.values())


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        pop = preprocess_input(read_data('input1.txt'))
        print(simulation(pop, 80))

    def test_part2(self):
        pop = preprocess_input(read_data('input1.txt'))
        print(simulation(pop, 256))


if __name__ == '__main__':
    unittest.main()
