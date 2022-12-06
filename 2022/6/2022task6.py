import unittest


def end_of_marker(input: str, length: int):
    for i in range(len(input)):
        if len(set(input[i:i+length])) == length:
            return i+length


def read_data(filename):
    with open(filename) as f:
        return f.readline().strip()


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        stream = read_data('input6.txt')
        print(end_of_marker(stream, 4))

    def test_part2(self):
        stream = read_data('input6.txt')
        print(end_of_marker(stream, 14))


if __name__ == '__main__':
    unittest.main()
