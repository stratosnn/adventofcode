import unittest
import itertools


def read_data(filename):
    with open(filename) as f:
        return [int(x.strip()) for x in f.readlines()]


def check_matching(xnum, data):
    for ix, _ in enumerate(data):
        current_sum = 0
        for jx in range(ix, len(data)):
            current_sum += data[jx]
            if current_sum == xnum:
                mn = min(data[ix:jx+1])
                mx = max(data[ix:jx+1])
                print(f'Matching for {xnum} min:{mn} max:{mx} sum of 2 : {mn + mx}')
                return ix, data[ix:jx+1]
            if current_sum > xnum:
                break


def get_invalid_position(preamble, raw_data):
    p = raw_data[:preamble]
    data = raw_data[preamble:]
    for ix, e in enumerate(data):
        index = len(p) + ix
        valid = any(map(lambda v: sum(v) == e, itertools.combinations(p, 2)))
        if valid:
            p.pop(0)
            p.append(e)
        else:
            print(f'Found {e} at {index} preamble [{preamble}]{p}')
            return index, e
    return None


class MyTestCase(unittest.TestCase):
    def test_something(self):
        raw_data = read_data('input9.txt')
        preamble = 25
        print(get_invalid_position(preamble, raw_data))

    def test_something2(self):
        data = read_data('input9.txt')
        xnum = 1721308972  # 127
        print(check_matching(xnum, data))



if __name__ == '__main__':
    unittest.main()
