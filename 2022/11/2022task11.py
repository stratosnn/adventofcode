import unittest
import functools


class Monkey:
    items = []
    op = ""
    test_div = 0
    on_true = -1
    on_false = -1
    count = 0

    def execute_op(self, old: int):
        self.count += 1
        return eval(self.op)


def read_data(filename):
    with open(filename) as f:
        monkeys = []
        monkey = Monkey()
        for l in map(lambda x: x.strip(), f.readlines() + ['']):
            if not l:
                monkeys.append(monkey)
                monkey = Monkey()
            elif "Starting items" in l:
                monkey.items = list(map(lambda x: int(x.strip()), l.split(':')[1].split(',')))
            elif "Operation" in l:
                monkey.op = l.split('=')[1].strip()
            elif "Test:" in l:
                monkey.test_div = int(l.split(' ')[-1])
            elif "If true" in l:
                monkey.on_true = int(l.split(' ')[-1])
            elif "If false" in l:
                monkey.on_false = int(l.split(' ')[-1])
        return monkeys


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        monkeys = read_data('input11.txt')
        for turn in range(20):
            for i, m in enumerate(monkeys):
                for item in m.items:
                    n = m.execute_op(item) // 3
                    monkeys[m.on_true if n % m.test_div == 0 else m.on_false].items.append(n)
                m.items = []
        inspected = list(sorted(map(lambda m: m.count, monkeys)))
        print(inspected[-1] * inspected[-2])

    def test_part2(self):
        monkeys = read_data('input11.txt')
        com_div = functools.reduce(lambda x, y: x * y, map(lambda x: x.test_div, monkeys))
        for turn in range(10000):
            for i, m in enumerate(monkeys):
                for item in m.items:
                    n = m.execute_op(item)
                    monkeys[m.on_true if n % m.test_div == 0 else m.on_false].items.append(n % com_div)
                m.items = []
        inspected = list(sorted(map(lambda m: m.count, monkeys)))
        print(inspected[-1] * inspected[-2])


if __name__ == '__main__':
    unittest.main()
