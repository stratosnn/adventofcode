import unittest


def transform_until(base, target):
    cnt, value = 1, base
    while value != target:
        value, cnt = (value * base) % 20201227, cnt + 1
    return cnt


def read_data(filename):
    with open(filename) as f:
        return [int(l.strip()) for l in f.readlines()]


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        pub = read_data('input25.txt')
        loops = [transform_until(7, v) for v in pub]
        print(pub, loops)
        print(list(map(pow, reversed(pub), loops, [20201227]*2)))


if __name__ == '__main__':
    unittest.main()
