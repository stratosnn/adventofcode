import unittest
from itertools import combinations, permutations
from pprint import pprint
from operator import add
from functools import reduce
from copy import deepcopy
import math

def read_data(filename):
    trunc = ['<', '>', '=', 'x', 'y', 'z']
    coords = []
    with open(filename) as f:
        for l in f:
            for t in trunc:
                l = l.replace(t, '')
            coords.append([int(x) for x in l.strip().split(',')])
        return coords


def calc_velocity(pos, vel):
    for (lx, lp), (rx, rp) in permutations(enumerate(pos), 2):
        for axis in range(3):
            if lp[axis] < rp[axis]:
                vel[lx][axis] += 1
            if lp[axis] > rp[axis]:
                vel[lx][axis] += -1
            if lp[axis] == rp[axis]:
                vel[lx][axis] += 0
    return vel


def calc_velocity_axis(pos, vel, axis):
    for (lx, lp), (rx, rp) in permutations(enumerate(pos), 2):
        if lp[axis] < rp[axis]:
            vel[lx][axis] += 1
        if lp[axis] > rp[axis]:
            vel[lx][axis] += -1
        if lp[axis] == rp[axis]:
            vel[lx][axis] += 0
    return vel


# def gcd(a, b, c):
#     return math.gcd(a, math.gcd(b, c))


# def lcm(a, b, c):
#     return abs(a*b*c) // gcd(a, b, c)


def lcm(denominators):
    return reduce(lambda a, b: a*b // math.gcd(a, b), denominators)

class MyTestCase(unittest.TestCase):
    def test_something(self):
        pos = read_data('input12.txt')
        vel = [[0] * 3 for l in pos]
        #print(f'pos {pos}\n  vel {vel}')
        for i in range(1000):
            vel = calc_velocity(pos, vel)
            for ix, v in enumerate(vel):
                pos[ix] = [x for x in map(add, pos[ix], v)]
            #print(f'pos {pos}\n  vel {vel}')

        # calculate energy
        print(sum([reduce(lambda pr, e: pr + abs(e), p, 0)*reduce(lambda pr, e: pr + abs(e), v, 0) for p, v in zip(pos, vel)]))

    def test_something2(self):
        pos = read_data('input12.txt')
        vel = [[0] * 3 for l in pos]

        orig_pos, orig_vel = deepcopy(pos), deepcopy(vel)
        acnt = []
        for axis in range(3):
            done = False
            cnt = 0
            while not done:
                vel = calc_velocity_axis(pos, vel, axis)
                v = [vl[axis] for vl in vel]
                for ix, po in enumerate(v):
                    pos[ix][axis] = pos[ix][axis] + po

                if vel == orig_vel and pos == orig_pos:
                    done = True
                cnt += 1
            print(f'cnt {cnt}')
            acnt.append(cnt)
        print(lcm(acnt))


if __name__ == '__main__':
    unittest.main()
