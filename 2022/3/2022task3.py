import unittest


def split_input(s: str):
    return s[:(len(s) // 2)], s[len(s) // 2:]


def score(s: chr):
    if 'A' <= s <= 'Z':
        return ord(s) - ord('A') + 27
    elif 'a' <= s <= 'z':
        return ord(s) - ord('a') + 1
    else:
        assert f"wrong input {s}"


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def read_data_split(filename):
    with open(filename) as f:
        return [split_input(l.strip()) for l in f.readlines()]


def read_data(filename):
    with open(filename) as f:
        return [set(l.strip()) for l in f.readlines()]


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        pairs = map(lambda x: (set(x[0]), set(x[1])), read_data_split('input3.txt'))
        print(sum(map(lambda v: score((v[0] & v[1]).pop()), pairs)))

    def test_part2(self):
        groups = chunks(read_data('input3.txt'), 3)
        badges = map(lambda x: score((x[0] & x[1] & x[2]).pop()), groups)
        print(sum(badges))


if __name__ == '__main__':
    unittest.main()
