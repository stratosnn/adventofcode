import unittest
from pprint import pprint
import itertools
import math


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        input = [1, 0, 18, 10, 19, 6]
        while len(input) < 2020:
            turn = len(input)
            last = input[-1]
            if input.count(last) == 1:
                input.append(0)
            else:
                ix = max(loc for loc, val in enumerate(input[:-1]) if val == last)
                input.append(turn - ix - 1)
        print(input[-3:])

    def test_part2(self):
        input = [1, 0, 18, 10, 19, 6]
        #input = [0, 3, 6]
        data = {v: [ix] for ix, v in enumerate(input)}

        last = input[-1]
        turn = len(input)

        while turn < 30000000:
            pturn = data[last]
            if len(pturn) == 1:
                last = 0
                data[0] = [turn, data[0][0]]
            else:
                last = turn - pturn[1] - 1
                data[last] = [turn] + data.get(last, [])[:1]

            turn += 1
            if turn % 100000 == 0 or turn == 2020:
                print(turn, last)
                #pprint(data)
        print(last)



if __name__ == '__main__':
    unittest.main()
