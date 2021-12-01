import unittest
from pprint import pprint
from functools import reduce
import itertools
import math
from copy import deepcopy
from collections import deque


def read_data(filename):
    with open(filename) as f:
        data = []
        for l in f:
            data.append(l.strip())
        ix = data.index('')
        first = list(map(int, data[1:ix]))
        second = list(map(int, data[ix+2:]))
        return first, second


def game(first, second):
    f = deque(first)
    s = deque(second)
    while len(f) > 0 and len(s) > 0:
        fc = f.popleft()
        sc = s.popleft()
        if fc > sc:
            f.append(fc)
            f.append(sc)
        else:
            s.append(sc)
            s.append(fc)
    return f, s


def game2(first, second):
    f = deque(first)
    s = deque(second)
    rounds = dict()
    while len(f) > 0 and len(s) > 0:

        fc = f.popleft()
        sc = s.popleft()

        if fc <= len(f) and sc <= len(s):
            if subgame(list(f)[:fc], list(s)[:sc]):
                f.append(fc)
                f.append(sc)
            else:
                s.append(sc)
                s.append(fc)
        else:
            if fc > sc:
                f.append(fc)
                f.append(sc)
            else:
                s.append(sc)
                s.append(fc)
        if (','.join(map(str, f)), ','.join(map(str, s))) in rounds:
            print(f'FOUND, {f} {s}')
            return [1], []
        rounds[(','.join(map(str, f)), ','.join(map(str, s)))] = 1
    return f, s


def subgame(first, second):
    #print(f'Starting subgame {first} {second}')
    f, s = game2(first, second)
    return True if len(f) > 0 else False


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        f, s = read_data('input22.txt')
        wf, ws = game(f, s)
        print(wf, ws)

        deck = list(wf if len(wf) > 0 else ws)

        sm = sum(map(lambda v: (v[0]+1)*v[1], enumerate(reversed(deck))))
        print(sm)

    def test_part2(self):
        f, s = read_data('input22.txt')
        wf, ws = game2(f, s)
        print(wf, ws)

        deck = list(wf if len(wf) > 0 else ws)

        sm = sum(map(lambda v: (v[0]+1)*v[1], enumerate(reversed(deck))))
        print(sm) # 33134 to high


if __name__ == '__main__':
    unittest.main()
