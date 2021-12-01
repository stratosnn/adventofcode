import unittest
from pprint import pprint
import itertools
import math
import re


def read_data(filename):
    inter = dict()
    all_ingr = set()
    all_alle = set()
    recepies = []
    with open(filename) as f:
        for l in f:
            m = re.match(r'(.*) \(contains (.*)\)', l)
            ingr = set(m.group(1).strip().split(' '))
            all_ingr.update(ingr)
            recepies.append(ingr)
            alle = m.group(2).split(',')
            for a in [x.strip() for x in alle]:
                all_alle.add(a)
                if a in inter:
                    inter[a] = inter[a].intersection(ingr)
                else:
                    inter[a] = ingr
        return inter, all_ingr, all_alle, recepies



class MyTestCase(unittest.TestCase):
    def test_part1(self):
        data, ingr, alle, recepies = read_data('input21.txt')
        pprint(data)
        pprint(ingr)
        pprint(alle)

        present = set()
        for v in data.values():
            present.update(v)

        non_present = ingr.symmetric_difference(present)

        print(sum([sum([i in non_present for i in r]) for r in recepies]))

    def test_part2(self):
        data, ingr, alle, recepies = read_data('input21.txt')
        pprint(data)

        present = set()
        for v in data.values():
            present.update(v)

        mapping = dict()
        for i in range(len(data)):
            singles = list(filter(lambda x: len(x[1]) == 1, data.items()))
            for k, v in singles:
                mapping[k] = v.pop()
                for ing in data.values():
                    if mapping[k] in ing:
                        ing.remove(mapping[k])

        result = []
        for k in sorted(mapping):
            result.append(mapping[k])
        print(','.join(result))
        #  not xzb,khqsk,dskjpq,srmsh,ksdgk,pgnpx,nvbrx,zbkbgp

if __name__ == '__main__':
    unittest.main()
