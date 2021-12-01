import unittest
from operator import add
from functools import reduce


def splitstr(s):
    return s.replace('w', 'w ').replace('e', 'e ').split()


def read_data(filename):
    with open(filename) as f:
        return [splitstr(l) for l in f]


DIRECTIONS = {
    'e':  (1, 0),
    'se': (0.5, -1),
    'sw': (-0.5, -1),
    'ne': (0.5, 1),
    'nw': (-0.5, 1),
    'w':  (-1, 0),
}


def flip(path):
    return tuple(reduce(lambda p, v: map(add, p, v), path))


def needs_flip(pos, db={}):
    neighbours = map(lambda v: tuple(map(add, pos, v)), DIRECTIONS.values())
    v = sum([db.setdefault(x, 0) for x in neighbours])
    return (db[pos] and (v == 0 or v > 2)) or (not db[pos] and v == 2)


def loop(count, db={}):
    # prepare initial neighbours
    for v in list(db):
        needs_flip(v, db)

    for i in range(count):
        flips = []
        for k in list(db):
            flips += [k] if needs_flip(k, db) else []
        for f in flips:
            db[f] = (db[f] + 1) % 2
        print(i, sum(db.values()))


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        flips = [flip(map(DIRECTIONS.get, p)) for p in read_data('input24.txt')]
        db = {pos: flips.count(pos) % 2 for pos in flips}
        print(sum(db.values()))

    def test_part2(self):
        flips = [flip(map(DIRECTIONS.get, p)) for p in read_data('input24.txt')]
        db = {pos: flips.count(pos) % 2 for pos in flips}
        loop(100, db)


if __name__ == '__main__':
    unittest.main()
