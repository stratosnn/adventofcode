import unittest
from pprint import pprint
import itertools
import math


def read_data(filename):
    with open(filename) as f:
        return [(l[0], int(l.strip()[1:])) for l in f.readlines()]


# Generalised vector rotation using 2D rotational matrix
def rotation(v, action):
    (x, y), (d, a) = action
    a = math.radians(a if d == 'L' else -a)
    return round(math.cos(a) * x - math.sin(a) * y), round(math.sin(a) * x + math.cos(a) * y)


# Neat trick to do 90° right rotation (x, y) -> (y, -x)
def rotation2(v, action):
    (x, y), (r, a) = v, action
    ix = (-1 if r == 'L' else 1) * a % 360 // 90
    return [(x, y), (y, -x), (-x, -y), (-y, x)][ix]


def navigate(p, direction, action):
    d, s = action
    m = {
        'N': (0, s),
        'S': (0, -s),
        'E': (s, 0),
        'W': (-s, 0),
        'F': (direction[0] * s, direction[1] * s)
    }
    if d in m:
        v = m[d]
        return (p[0] + v[0], p[1] + v[1]), direction
    elif d in 'LR':
        direction = rotation2(direction, action)
        return p, direction
    else:
        raise Exception(f'Unknown action {action}')


def navigate2(p, w, action):
    d, s = action
    m = {
        'N': (0, s),
        'S': (0, -s),
        'E': (s, 0),
        'W': (-s, 0),
    }
    if d in m:
        v = m[d]
        return p, (w[0] + v[0], w[1] + v[1])
    elif d == 'F':
        return (p[0] + w[0] * s, p[1] + w[1] * s), w
    elif d in 'LR':
        w = rotation2(w, action)
        return p, w
    else:
        raise Exception(f'Unknown action {action}')


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        pos = (0, 0)
        direction = (1, 0)
        for action in read_data('input12.txt'):
            pos, direction = navigate(pos, direction, action)
        print(pos, sum(map(abs, pos)))

    def test_part2(self):
        pos = (0, 0)
        waypoint = (10, 1)
        for action in read_data('input12.txt'):
            pos, waypoint = navigate2(pos, waypoint, action)
        print(pos, sum(map(abs, pos)))


if __name__ == '__main__':
    unittest.main()
