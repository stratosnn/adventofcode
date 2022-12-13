import unittest


def read_data(filename):
    with open(filename) as f:
        return [l.strip().split(' ') for l in f.readlines()]


def chunk(l: list, size: int):
    for i in range(0, len(l), size):
        yield l[i:i + size]


def calc_state(data: list):
    state = [1]
    for d in data:
        if d[0] == 'noop':
            state.append(state[-1])
        elif d[0] == 'addx':
            state.append(state[-1])
            state.append(state[-1] + int(d[1]))
    return state


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        data = read_data('input10.txt')
        state = calc_state(data)
        print(sum(map(lambda x: x * state[x-1], range(20, 221, 40))))

    def test_part2(self):
        data = read_data('input10.txt')
        state = calc_state(data)
        t = list(map(lambda x: '#' if (x[1] - 1 <= x[0] % 40 <= x[1] + 1) else ' ', enumerate(state)))
        for row in chunk(t, 40):
            print(''.join(row))


if __name__ == '__main__':
    unittest.main()
