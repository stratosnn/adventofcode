import unittest
from pprint import pprint
import itertools
import functools
import math
import collections
import copy
from functools import lru_cache


def is_big_cave(name: str):
    return ord('A') <= ord(name[0]) <= ord('Z')


@lru_cache(maxsize=4096)
def path_has_double_entry(path: tuple):
    mapping = collections.defaultdict(int)
    for p in filter(lambda x: not is_big_cave(x), path):
        mapping[p] = mapping[p] + 1
    return any(map(lambda x: x > 1, mapping.values()))


def is_valid_path2(name: str, path: tuple):
    in_path = name in path
    is_start_and_entered = name == 'start' and in_path
    return is_big_cave(name) or (not (path_has_double_entry(path) and in_path) and not is_start_and_entered)


def read_data(filename):
    graph = collections.defaultdict(list)
    with open(filename) as f:
        for line in f:
            left, right = line.strip().split('-')
            graph[left].append(right)
            graph[right].append(left)
    return graph


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        graph = read_data('input1.txt')
        bfs = [('start', [])]
        result = []
        while bfs:
            point, path = bfs.pop()
            path = copy.deepcopy(path)
            path.append(point)
            if point == 'end':
                result.append(path)
                continue
            for n in graph[point]:
                if n not in path or is_big_cave(n):
                    bfs.append((n, path))
        print(len(result))

    def test_part2(self):
        graph = read_data('input1.txt')
        bfs = [('start', ())]
        count = 0
        while bfs:
            point, path = bfs.pop()
            if point == 'end':
                count += 1
                continue
            path = path + (point,)
            for n in graph[point]:
                if is_valid_path2(n, path):
                    bfs.append((n, path))
        print(count)


if __name__ == '__main__':
    unittest.main()
