import unittest
import itertools
import functools


def chunk(l: list, size: int):
    for i in range(0, len(l), size):
        yield l[i:i + size]


def read_data(filename):
    with open(filename) as f:
        return list(map(eval, filter(lambda x: x, [l.strip() for l in f.readlines()])))


def compare(l, r):
    l = [l] if type(l) is not list else l
    r = [r] if type(r) is not list else r

    for i in range(min(len(l), len(r))):
        el, er = l[i], r[i]

        if type(el) is int and type(er) is int:
            if el < er:
                return 1
            elif el > er:
                return -1
        else:
            sub = compare(el, er)
            if sub != 0:
                return sub

    if len(l) < len(r):
        return 1
    elif len(l) > len(r):
        return -1
    return 0


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        pairs = chunk(read_data('input13.txt'), 2)
        result = [compare(*p) for p in pairs]
        print(sum(map(lambda x: x[0]+1 if x[1] == 1 else 0, enumerate(result))))

    def test_part2(self):
        data = list(itertools.chain(read_data('input13.txt'), [[[2]], [[6]]]))
        sdata = list(sorted(data, key=functools.cmp_to_key(compare), reverse=True))
        print((sdata.index([[2]]) + 1) * (sdata.index([[6]]) + 1))


if __name__ == '__main__':
    unittest.main()
