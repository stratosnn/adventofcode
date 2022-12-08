import unittest
import itertools
import functools


def read_data(filename):
    with open(filename) as f:
        return [[int(c) for c in l.strip()] for l in f.readlines()]


def visibility(e: int, line: list):
    l = list(itertools.takewhile(lambda x: x < e, line))
    return len(l) + 1 if len(l) < len(line) else len(l)


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        data = read_data('input8.txt')
        transposed = list(zip(*data))
        visible = 4 * (len(data) - 1)
        for i in range(1, len(data) - 1):
            for j in range(1, len(data[0]) - 1):
                r, t = data[i], transposed[j]
                m = map(max, [r[:j], r[j+1:], t[:i], t[i+1:]])
                visible += any(map(lambda x: data[i][j] > x, m))
        print(visible)

    def test_part2(self):
        data = read_data('input8.txt')
        transposed = list(zip(*data))
        top_score = 0
        for i in range(1, len(data) - 1):
            for j in range(1, len(data[0]) - 1):
                r, t = data[i], transposed[j]
                vis = list(map(lambda y: visibility(data[i][j], y), map(list, [reversed(r[:j]), r[j+1:], reversed(t[:i]), t[i+1:]])))
                top_score = max(functools.reduce(lambda x, y: x * y, vis), top_score)
        print(top_score)
        pass


if __name__ == '__main__':
    unittest.main()
