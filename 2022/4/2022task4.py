import unittest


def range_to_set(rng: str):
    l, r = map(int, rng.split("-"))
    return set([l for l in range(l, r+1)])


def read_data(filename):
    with open(filename) as f:
        return [tuple(l.split(",")) for l in f.readlines()]


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        left, right = zip(*read_data("input4.txt"))
        left_set, right_set = map(range_to_set, left), map(range_to_set, right)
        print(sum(map(lambda p: p[0] <= p[1] or p[1] <= p[0], zip(left_set, right_set))))

        pass

    def test_part2(self):
        left, right = zip(*read_data("input4.txt"))
        left_set, right_set = map(range_to_set, left), map(range_to_set, right)
        print(sum(map(lambda p: len(p[0] & p[1]) > 0, zip(left_set, right_set))))
        pass


if __name__ == '__main__':
    unittest.main()
