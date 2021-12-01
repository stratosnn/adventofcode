import unittest
import functools
import operator

def read_input(filename):
    lst = []
    with open(filename) as f:
        for line in f:
            lst.append(line.strip())
        return lst, len(lst[0]), len(lst)


def calculate(dx, dy):
    lst, szx, szy = read_input('input3.txt')
    print(szx, szy)
    px, py = 0, 0
    tree_counter = 0
    while py < szy:
        if lst[py][px] == '#':
            tree_counter += 1
        px, py = (px + dx) % szx, py + dy
    return tree_counter


class MyTestCase(unittest.TestCase):
    def test_something(self):
        lst, szx, szy = read_input('input3.txt')
        res = []
        for pair in [(1,1), (3,1), (5,1), (7,1), (1,2)]:
            cnt = calculate(*pair)
            print(cnt)
            res.append(cnt)

        print(functools.reduce(operator.mul, res, 1))


if __name__ == '__main__':
    unittest.main()
