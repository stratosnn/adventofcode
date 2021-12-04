import unittest
from pprint import pprint
import itertools
import math


def read_data(filename):
    with open(filename) as f:
        numbers = [int(x.strip()) for x in f.readline().split(',')]
        boards = []
        board = []
        for l in f:
            if len(l.strip()) == 0:
                continue
            board.append([int(x) for x in l.split()])
            if len(board) == 5:
                boards.append(board)
                board = []
        return numbers, boards


def column(ix: int, array: list):
    return [row[ix] for row in array]


def get_winning_board(numbers, boards):
    for step in range(5, len(numbers)):
        round = frozenset(numbers[0:step])
        for bix, board in enumerate(boards):
            # rows
            for line in board:
                if frozenset(line) <= round:
                    return bix, numbers[0:step]
            # columns
            for c in [column(ix, board) for ix in range(len(board[0]))]:
                if frozenset(c) <= round:
                    return bix, numbers[0:step]


def get_last_winning_board(numbers, boards):
    winning_boards = []
    for step in range(5, len(numbers)):
        round = frozenset(numbers[0:step])
        for bix, board in enumerate(boards):
            # rows
            for line in board:
                if frozenset(line) <= round:
                    if bix not in map(lambda e: e[0], winning_boards):
                        winning_boards.append((bix, numbers[0:step]))
                        break
            # columns
            for c in [column(ix, board) for ix in range(len(board[0]))]:
                if frozenset(c) <= round:
                    if bix not in map(lambda e: e[0], winning_boards):
                        winning_boards.append((bix, numbers[0:step]))
                        break

    return winning_boards[-1]


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        numbers, boards = read_data('input1.txt')
        ix, round = get_winning_board(numbers, boards)
        board = boards[ix]
        unmarked = frozenset(itertools.chain.from_iterable(board)) - frozenset(round)
        print(sum(unmarked) * round[-1])

    def test_part2(self):
        numbers, boards = read_data('input1.txt')
        ix, round = get_last_winning_board(numbers, boards)
        board = boards[ix]
        unmarked = frozenset(itertools.chain.from_iterable(board)) - frozenset(round)
        print(sum(unmarked) * round[-1])


if __name__ == '__main__':
    unittest.main()
