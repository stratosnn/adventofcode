import unittest
import math


OFFSET = {
    'U': (0,  1),
    'D': (0, -1),
    'R': ( 1, 0),
    'L': (-1, 0),
}


def read_data(filename):
    with open(filename) as f:
        for l in f.readlines():
            move = l.strip().split(' ')
            yield move[0], int(move[1])


def sign_offset(val):
    return int(math.copysign(1, val)) if val != 0 else 0


def distance(p1: tuple, p2: tuple):
    return int(math.sqrt(sum(map(lambda x: pow(x[0] - x[1], 2), zip(p1, p2)))))


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        pos, prev = (0, 0), (0, 0)
        tail = (0, 0)
        visited = {tail}
        for d, shifts in read_data('input9.txt'):
            for shift in range(shifts):
                off = OFFSET[d]
                prev = pos
                pos = (pos[0] + off[0], pos[1] + off[1])
                if distance(pos, tail) > 1:
                    visited.add(prev)
                    tail = prev
        print(len(visited))

    def test_part2(self):
        rope = [(0, 0)] * 10
        visited = {rope[-1]}
        for d, shifts in read_data('input9.txt'):
            for shift in range(shifts):
                off = OFFSET[d]
                rope[0] = (rope[0][0] + off[0], rope[0][1] + off[1])
                for ix in range(1, len(rope)):
                    if distance(rope[ix], rope[ix-1]) >= 2:
                        cshift = sign_offset(rope[ix-1][0] - rope[ix][0]), sign_offset(rope[ix-1][1] - rope[ix][1])
                        rope[ix] = (rope[ix][0] + cshift[0], rope[ix][1] + cshift[1])
                visited.add(rope[-1])
        print(len(visited))


if __name__ == '__main__':
    unittest.main()
