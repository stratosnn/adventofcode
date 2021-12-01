# import unittest
# import functools
# import operator
#
#
# def read_input(filename):
#     with open(filename) as f:
#         return [l.strip() for l in f.readlines()]
#
#
# def roll(x, y, dx, dy, n):
#     coords = [(x + (i+1)*dx, y + (i+1)*dy) for i in range(n)]
#     x, y = coords[-1]
#     return coords, x, y
#
#
# def create_coordinates(movement):
#     x, y = 0, 0
#     coords = []
#     c = []
#     print(movement)
#     for m in movement:
#         #print(x, y)
#         direction, offset = m[0], int(m[1:])
#         if direction.upper() == 'U':
#             c, x, y = roll(x, y, 0, 1, offset)
#             coords += c
#         elif direction.upper() == 'R':
#             c, x, y = roll(x, y, 1, 0, offset)
#             coords += c
#         elif direction.upper() == 'D':
#             c, x, y = roll(x, y, 0, -1, offset)
#             coords += c
#         elif direction.upper() == 'L':
#             c, x, y = roll(x, y, -1, 0, offset)
#             coords += c
#         else:
#             raise Exception(f'Alarm direct {direction} ')
#     return coords
#
#
#
#
# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         first, second = read_input('input3.txt')
#         first_set = set(create_coordinates(first.split(',')))
#         second_set = set(create_coordinates(second.split(',')))
#
#         intersections = first_set.intersection(second_set)
#         print(intersections)
#         m = 9999999999999
#         for i in intersections:
#             el = sum([abs(x) for x in i])
#             if el < m:
#                 print(f'Candidate {i} dist {el}, prev {m}')
#                 m = el


import unittest
import functools
import operator


def read_input(filename):
    with open(filename) as f:
        return [l.strip() for l in f.readlines()]


def roll(x, y, dx, dy, n):
    coords = [(x + (i+1)*dx, y + (i+1)*dy) for i in range(n)]
    x, y = coords[-1]
    return coords, x, y


def create_coordinates(movement):
    x, y = 0, 0
    coords = []
    c = []
    print(movement)
    for m in movement:
        direction, offset = m[0], int(m[1:])
        if direction.upper() == 'U':
            c, x, y = roll(x, y, 0, 1, offset)
            coords += c
        elif direction.upper() == 'R':
            c, x, y = roll(x, y, 1, 0, offset)
            coords += c
        elif direction.upper() == 'D':
            c, x, y = roll(x, y, 0, -1, offset)
            coords += c
        elif direction.upper() == 'L':
            c, x, y = roll(x, y, -1, 0, offset)
            coords += c
        else:
            raise Exception(f'Alarm direct {direction} ')
    return coords




class MyTestCase(unittest.TestCase):
    def test_something(self):
        first, second = read_input('input3.txt')
        s1 = create_coordinates(first.split(','))
        dst1 = dict()
        for ix, d in enumerate(s1):
            dst1[d] = min(ix + 1, dst1.get(d, 999999))
        first_set = set(s1)
        s2 = create_coordinates(second.split(','))
        dst2 = dict()
        for ix, d in enumerate(s2):
            dst2[d] = min(ix + 1, dst2.get(d, 999999))
        second_set = set(s2)

        intersections = first_set.intersection(second_set)
        print(intersections)
        m = 9999999999999
        for i in intersections:
            el = dst1[i] + dst2[i]
            if el < m:
                print(f'Candidate {i} dist {el}, prev {m}')
                m = el


if __name__ == '__main__':
    unittest.main()
