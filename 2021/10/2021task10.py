import unittest
from pprint import pprint
import itertools
import math


def read_data(filename):
    with open(filename) as f:
        return [l.strip() for l in f.readlines()]


BMAP = {'<': '>',
        '[': ']',
        '(': ')',
        '{': '}'
        }

RMAP = {v: k for k, v in BMAP.items()}

SCORING = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

SCORING2 = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


def is_line_valid(line):
    stack = []
    for c in line:
        if c in BMAP:
            stack.append(c)
        elif c in RMAP:
            if RMAP[c] != stack.pop():
                return False
        else:
            assert "Unexpected character"
    return True


def calculate_scoring2(line):
    score = 0
    for c in line:
        score = score * 5 + SCORING2[c]
    return score


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        data = read_data('input1.txt')
        errors = []
        for ln, line in enumerate(data):
            stack = []
            for c in line:
                if c in BMAP:
                    stack.append(c)
                elif c in RMAP:
                    if RMAP[c] != stack.pop():
                        errors.append(c)
                        break
                else:
                    assert "Unexpected character"
        print(errors)
        print(sum(map(lambda x: SCORING[x], errors)))
        pass

    def test_part2(self):
        data = read_data('input1.txt')
        fdata = [x for x in filter(is_line_valid, data)]

        fixes = []
        for line in fdata:
            stack = []
            for c in line:
                if c in BMAP:
                    stack.append(c)
                elif c in RMAP:
                    stack.pop()
            fixes.append([x for x in map(lambda b: BMAP[b], reversed(stack))])
        pprint(fixes)

        scores = [x for x in sorted(map(calculate_scoring2, fixes))]
        print(scores)
        print(f'len scores {len(scores)} mid {scores[len(scores)//2]}')



if __name__ == '__main__':
    unittest.main()
