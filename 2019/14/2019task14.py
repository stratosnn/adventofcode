import unittest
import re
from pprint import pprint
import math
from copy import deepcopy


def read_data(filename):
    data = dict()
    with open(filename) as f:
        for line in f:
            m = re.search(r'(.*) => (\d+ \w+)', line)
            dst_quanity, dst_name = m.group(2).split(' ')

            for pair in m.group(1).split(','):
                src_quanity, src_name = pair.strip().split(' ')
                data.setdefault(dst_name, (int(dst_quanity), []))[1].append((int(src_quanity), src_name))
    return data


def walk_reactions(required_cnt, name, reactions, workbench={}):
    if name == 'ORE':
        return required_cnt
    cnt, sources = reactions[name]
    needed_to_produce = max(0, required_cnt - workbench.setdefault(name, 0))
    workbench[name] -= (required_cnt - needed_to_produce)
    batches = math.ceil(needed_to_produce / cnt)
    ores = sum(walk_reactions(q * batches, src, reactions, workbench) for (q, src) in sources)
    workbench[name] = workbench.get(name, 0) + (batches*cnt - needed_to_produce)
    return ores


def binary_search(min_val, max_val, reactions):
    current = min_val + (max_val - min_val) // 2
    ore = walk_reactions(current, 'FUEL', reactions, dict())

    rng = (current, max_val) if ore < 1000000000000 else (min_val, current)
    if rng == (min_val, max_val):
        return current
    else:
        return binary_search(*rng, reactions)


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        reactions = read_data('input14.txt')
        cnt = walk_reactions(1, 'FUEL', reactions, dict())
        print(cnt)

    def test_part2(self):
        reactions = read_data('input14.txt')
        approx = 1000000000000 // walk_reactions(1, 'FUEL', reactions, dict())
        print(binary_search(approx, 2*approx, reactions))


if __name__ == '__main__':
    unittest.main()
