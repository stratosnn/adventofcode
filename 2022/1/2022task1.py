import unittest


def read_data(filename):
    with open(filename) as f:
        provision = [0]
        for l in [l.strip() for l in f.readlines()]:
            if not l:
                provision.append(0)
            else:
                provision[-1] += int(l)
        return provision


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        provisions = read_data('input1.txt')
        print(max(provisions))

    def test_part2(self):
        provisions = sorted(read_data('input1.txt'), reverse=True)
        print(sum(provisions[0:3]))
        pass


if __name__ == '__main__':
    unittest.main()
