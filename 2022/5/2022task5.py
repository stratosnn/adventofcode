import unittest
import re


WIDTH = 9


def parse_move(l: str):
    t = l.split(" ")
    return int(t[1]), int(t[3]) - 1, int(t[5]) - 1


def chunk(l: list, size: int):
    for i in range(0, len(l), size):
        yield l[i:i + size]


def parse_crate_input(crate_input):
    chunked = list(map(lambda l: [re.sub(r'[\[\] \n]', '', c) for c in chunk(l, 4)], crate_input))
    for c in chunked:
        if len(c) < WIDTH:
            c += [''] * (WIDTH - len(c))
    transposed = list(map(lambda x: list(reversed(x)), zip(*chunked)))
    return list(map(lambda e: list(filter(lambda x: x, e)), transposed))


def read_data(filename):
    with open(filename) as f:
        crate_consumed = False
        crate_input = []
        move_input = []
        for l in f.readlines():
            if not l.strip():
                crate_consumed = True
                continue
            if not crate_consumed:
                crate_input.append(l)
            else:
                move_input.append(l)
        crate_input.pop()
        return parse_crate_input(crate_input), list(map(parse_move, move_input))


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        crates, moves = read_data('input5.txt')
        for n, fr, to in moves:
            stack = reversed(crates[fr][-n:])
            crates[fr] = crates[fr][0:-n]
            crates[to] += list(stack)

        print(''.join([c[-1] for c in crates]))

    def test_part2(self):
        crates, moves = read_data('input5.txt')
        for n, fr, to in moves:
            stack = crates[fr][-n:]
            crates[fr] = crates[fr][0:-n]
            crates[to] += stack

        print(''.join([c[-1] for c in crates]))


if __name__ == '__main__':
    unittest.main()
