import unittest
from math import sqrt, atan2
from operator import mul
from pprint import pprint
from functools import cmp_to_key
from collections import OrderedDict


def read_data(filename):
    result = []
    with open(filename) as f:
        for y, line in enumerate(f.readlines()):
            for x, c in enumerate(line):
                if c == '#':
                    result.append((x, y))
        return result


def distance(v):
    return sqrt(v[0] ** 2 + v[1] ** 2)


def angle(v1, v2):
    dot = sum(map(mul, v1, v2))
    return dot / (1 * sqrt(v2[0] ** 2 + v2[1] ** 2))


def angle2(v1, v2):
    dot = sum(map(mul, v1, v2))
    det = v1[0]*v2[1] - v2[0]*v1[1]
    return atan2(det, dot)


def cmp(v1, v2):
    if v1[0] == v2[0]:
        return v1[3] < v2[3]
    else:
        return v1[0] < v2[0]


class MyTestCase(unittest.TestCase):
    def test_something(self):
        cords = read_data('input10.txt')
        max_len = 0
        pos = None
        for cx, cy in cords:
            uniq = set()
            for x, y in cords:
                if (x, y) == (cx, cy):
                    continue
                rx, ry = x - cx, y - cy
                uniq.add(angle2((1.0, 0.0), (rx, ry)))
            if len(uniq) > max_len:
                max_len = len(uniq)
                pos = cx, cy
                #print(uniq)
            #print(f'Center ({cx, cy}) Rel ({rx, ry}) uniq {len(uniq)} {uniq}  ')
        print(f'({pos[0]},{pos[1]}) {max_len}')  # (23,19)

    def test_task2(self):
        cords = read_data('input10.txt')
        lst = []
        coord_map = dict()
        cx, cy = 23, 19  #11, 13 # 23, 19  # result of previous task # 11, 13  #
        for x, y in cords:
            if (cx, cy) == (x, y):
                continue
            rx, ry = x - cx, y - cy
            a = angle2((0.0, 1.0), (rx, ry))
            ln = coord_map.setdefault(a, [])
            ln.append((x, y, distance((rx, ry))))

        # presort each cell
        for k, v in coord_map.items():
            coord_map[k].sort(key=lambda e: e[2])

        # Now flat the structure
        max_entry_len = max([len(e) for e in coord_map.values()])
        coord_map = OrderedDict(sorted(coord_map.items()))
        ordered = []
        for i in range(max_entry_len):
            for e in coord_map.values():
                if i < len(e):
                    ordered.append(e[i])

        #pprint(coord_map)
        #pprint(ordered)
        print(ordered[198])
        print(ordered[199])
        print(ordered[200])
        print(ordered[298])
        #print(ordered[200 - 1][0] * 100 + ordered[200 - 1][1])


if __name__ == '__main__':
    unittest.main()
