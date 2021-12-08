import unittest
from pprint import pprint
import itertools
import math


def read_data(filename):
    with open(filename) as f:
        seq, display = [], []
        for line in f:
            s, d = line.split('|')
            seq.append([x for x in s.split()])
            display.append([x for x in d.split()])

        return seq, display


# 0 - 6 p done
# 1 - 2 done
# 2 - 5 p done
# 3 - 5 p done
# 4 - 4 done
# 5 - 5 p done
# 6 - 6 p done
# 7 - 3 done
# 8 - 7 done
# 9 - 6 p done

# unique patters 9, 6, 4
# 9 = bottom right
# 6 = top left
# 4 = bottom left

def crack_the_code(seq: list):
    mapping = {}
    for s in seq:
        if len(s) == 2:
            mapping[1] = frozenset([c for c in s])
        elif len(s) == 3:
            mapping[7] = frozenset([c for c in s])
        elif len(s) == 4:
            mapping[4] = frozenset([c for c in s])
        elif len(s) == 7:
            mapping[8] = frozenset([c for c in s])

    len6 = [frozenset([c for c in x]) for x in seq if len(x) == 6]
    inter6 = len6[0] & len6[1] & len6[2]

    bottom = inter6 - mapping[4] - mapping[7]
    bottom_left = mapping[8] - mapping[7] - mapping[4] - bottom
    bottom_right = mapping[1] & inter6
    top = mapping[7] - mapping[1]
    top_left = inter6 - mapping[7] - bottom
    top_right = mapping[1] - inter6
    middle = mapping[4] - inter6 - mapping[1]

    mapping[9] = mapping[8] - bottom_left
    mapping[5] = top | top_left | middle | bottom_right | bottom
    mapping[6] = mapping[8] - top_right
    mapping[3] = mapping[8] - top_left - bottom_left
    mapping[2] = mapping[8] - top_left - bottom_right
    mapping[0] = mapping[8] - middle
    return {v: k for k, v in mapping.items()}


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        seq, display = read_data('input1.txt')

        s = 0
        for r in display:
            s += sum([1 for e in filter(lambda x: len(x) in [2, 3, 4, 7], r)])
        print(s)

    def test_part2(self):
        seq, display = read_data('input1.txt')

        value = 0
        for s, dis in zip(seq, display):
            mapping = crack_the_code(s)
            d = [frozenset([c for c in x]) for x in dis]
            value += int(f'{mapping[d[0]]}{mapping[d[1]]}{mapping[d[2]]}{mapping[d[3]]}')
        print(value)


if __name__ == '__main__':
    unittest.main()
