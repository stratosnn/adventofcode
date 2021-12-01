import unittest
import functools


def tobin(v):
    if v in ['F', 'L']:
        return '0'
    elif v in ['B', 'R']:
        return '1'
    else:
        raise Exception(f'Unexpected input {v}')


def read_data_as_bin(filename):
    result = []
    with open(filename) as f:
        return [int(''.join(map(tobin, l.strip())), 2) for l in f.readlines()]


def read_data(filename):
    result = []
    with open(filename) as f:
        for l in f:
            row, seat = int(''.join(map(tobin, l[:7])), 2), int(''.join(map(tobin, l[7:])), 2)
            result.append((row, seat))
    return result


class MyTestCase(unittest.TestCase):
    def test_something(self):
        data = read_data_as_bin('inpu5.txt')
        print(max(data))
        print(set(data).symmetric_difference(set(range(1023))))


if __name__ == '__main__':
    unittest.main()
