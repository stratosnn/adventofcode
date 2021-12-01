import unittest
from pprint import pprint
import itertools
import math
from collections import deque


def read_data(filename):
    with open(filename) as f:
        result = []
        for line in f:
            out = []
            for ix, c in enumerate(line):
                if c == '*':
                    jx = len(out) - 1
                    cb_cnt = 0
                    while jx >= 0:
                        if (out[jx] == '(' and cb_cnt == 0) or (jx == 0):
                            out.insert(jx, '(')
                            out.append(')')
                            break
                        cb_cnt += 1 if out[jx] == ')' else 0
                        cb_cnt -= 1 if out[jx] == '(' else 0
                        jx -= 1

                out.append(c)
            result.append(''.join(out))
        return result


DIGITS = tuple(str(c) for c in range(10))

def invert_prio(out, skip=0):
    #print(skip, ''.join(out))

    s = skip
    for ix in range(len(out)):
        if out[ix] == '+':
            if s == 0:
                jx = ix - 1
                bc_cnt = 0
                while jx >= 0:
                    bc_cnt -= 1 if out[jx] == '(' else 0
                    if out[jx] == ')':
                        bc_cnt += 1
                    elif bc_cnt == 0 and (out[jx] == '(' or out[jx] in DIGITS):
                        out.insert(jx, '(')
                        #out.insert(ix+1, ')')
                        break
                    # elif out[jx] in DIGITS:
                    #     out.insert(jx, '(')
                    #     out.insert(ix+1, ')')
                    #     break
                    jx -= 1

                jx = ix+2
                bc_cnt = 0
                while jx < len(out):
                    bc_cnt -= 1 if out[jx] == ')' else 0
                    if out[jx] == '(':
                        bc_cnt += 1
                    elif bc_cnt == 0 and (out[jx] == ')' or out[jx] in DIGITS):
                        out.insert(jx+1, ')')
                        #out.insert(ix+1, '(')
                        break
                    # elif out[jx] in DIGITS:
                    #     out.insert(jx, '(')
                    #     out.insert(ix+1, ')')
                    #     break
                    jx += 1
                invert_prio(out, skip + 1)
                break
            else:
                s -= 1


def read_data2(filename):
    with open(filename) as f:
        result = []
        for line in f:
            out = [c for c in line]
            invert_prio(out, 0)
            result.append(''.join(out))
        return result


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        data = read_data('input18.txt')
        # pprint(data)
        # for l in data:
        #     print(eval(l))
        print(sum([eval(x) for x in data]))  # 21347713555555

    def test_part2(self):
        data = read_data2('input18.txt')
        # pprint(data)
        # for l in data:
        #     print(eval(l))
        print(sum([eval(x) for x in data]))


if __name__ == '__main__':
    unittest.main()
