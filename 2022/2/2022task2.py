import unittest


strategy_chart = {
    ('A', 'X'): 'C',
    ('A', 'Y'): 'A',
    ('A', 'Z'): 'B',
    ('B', 'X'): 'A',
    ('B', 'Y'): 'B',
    ('B', 'Z'): 'C',
    ('C', 'X'): 'B',
    ('C', 'Y'): 'C',
    ('C', 'Z'): 'A',
}


chart = {
    ('A', 'A'): 3,
    ('A', 'B'): 6,
    ('A', 'C'): 0,
    ('B', 'A'): 0,
    ('B', 'B'): 3,
    ('B', 'C'): 6,
    ('C', 'A'): 6,
    ('C', 'B'): 0,
    ('C', 'C'): 3,
}


def read_data(filename):
    with open(filename) as f:
        return [tuple(map(lambda x: x.strip(), l.split(' '))) for l in f.readlines()]


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        op, you = zip(*read_data('input2.txt'))
        yours = sum(list(map(lambda x: ord(x) - ord('X') + 1, you)))
        print("yours", yours)

        shift = ord('X') - ord('A')
        you_shifted = list(map(lambda x: chr(ord(x) - shift), you))
        win_score = sum(map(lambda v: chart[v], zip(op, you_shifted)))
        print("winscore", win_score)
        print("total", win_score + yours)

    def test_part2(self):
        op, you = zip(*read_data('input2.txt'))
        planned_you = list(map(lambda v: strategy_chart[v], zip(op, you)))
        win_score = sum(map(lambda v: chart[v], zip(op, planned_you)))

        yours = sum(list(map(lambda x: ord(x) - ord('A') + 1, planned_you)))
        print("yours", yours)
        print("winscore", win_score)
        print("total", win_score + yours)


if __name__ == '__main__':
    unittest.main()
