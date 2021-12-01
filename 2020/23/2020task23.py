import unittest
from pprint import pprint
import itertools
import math
from collections import deque


def get_destimation(current, move, max_value, min_value):
    destination = current
    while True:
        destination = destination - 1
        if destination < min_value:
            destination = max_value + 1
            continue
        if destination in move:
            continue
        break
    return destination


def get_chain(after, current, count):
    chain = []
    for _ in range(count):
        chain.append(after[current])
        current = after[current]
    return chain


def simulate(seed, cups, steps):
    order = [int(seed[pos]) if pos < len(seed) else pos+1 for pos in range(cups)]
    after = {order[i]: order[(i+1) % cups] for i in range(cups)}
    current = order[0]
    for _ in range(steps):
        p = get_chain(after, current, 3)
        dest = current - 1 if current > 1 else cups
        while dest in p:
            dest = dest - 1 if dest > 1 else cups

        after[current] = after[p[-1]]
        after[p[-1]] = after[dest]
        after[dest] = p[0]

        current = after[current]
    return after



class MyTestCase(unittest.TestCase):
    def test_part1(self):
        # data = deque([int(x) for x in '389125467'])
        data = deque([int(x) for x in '496138527'])
        current = data[0]
        mx = max(data)
        mn = min(data)


        for i in range(100):
            print(data)
            current = data.popleft()
            move = [data.popleft() for x in range(3)]
            next = data[0]
            data.appendleft(current)
            destination = get_destimation(current, move, mx, mn)
            #print(f'current {current} destination {destination} move {move}')
            ix = data.index(destination) + 1
            for x in reversed(range(3)):
                data.insert(ix, move[x])
            while data[0] != next:
                tmp = data.popleft()
                data.append(tmp)
        print('result')
        print(data)

        while data[0] != 1:
            tmp = data.popleft()
            data.append(tmp)
        data.popleft()

        print(''.join(map(str, list(data))))



    def test_part2(self):
        after = simulate('389125467', 1000000, 10000000)
        print(after[1] * after[after[1]])


    def test_part3(self):
        input = '389125467'
        after = simulate(input, len(input), 10)



    # def test_part2(self):
    #     # data = deque([int(x) for x in '389125467'])
    #     data = [int(x) for x in '496138527']
    #     current = data[0]
    #     mx = max(data)
    #     mn = min(data)
    #
    #     i = mx + 1
    #     while i <= 1000000:
    #         data.append(i)
    #         i += 1
    #
    #     mx = max(data)
    #     mn = min(data)
    #     for i in range(10000000):
    #         #print(data)
    #         current = data[0]
    #         move = data[1:4]
    #         next = data[4]
    #         data = [current] + data[4:]
    #         destination = get_destimation(current, move, mx, mn)
    #         #print(f'current {current} destination {destination} move {move}')
    #         ix = data.index(destination) + 1
    #         for x in reversed(range(3)):
    #             data.insert(ix, move[x])
    #
    #         data = data[data.index(next):] + data[:data.index(next)]
    #
    #         if i % 10000 == 0:
    #             print(i)
    #
    #     print('result')
    #     print(data)
    #
    #     dt = deque(data)
    #     while dt[0] != 1:
    #         tmp = dt.popleft()
    #         dt.append(tmp)
    #     dt.popleft()
    #
    #     print(','.join(map(str, list(dt))))


if __name__ == '__main__':
    unittest.main()
