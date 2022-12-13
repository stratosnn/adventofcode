import unittest
import functools

STEPS = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0)
]


def read_data(filename):
    with open(filename) as f:
        return [[ord(c) for c in l.strip()] for l in f.readlines()]


def find_nodes(grid: list, c: str):
    matching = []
    for i, r in enumerate(grid):
        matching += list(functools.reduce(lambda acc, x: acc + [(i, x[0])] if x[1] == ord(c) else acc, enumerate(grid[i]), []))
    return matching


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        grid = read_data('input12.txt')
        s, e = tuple(map(lambda x: find_nodes(grid, x)[0], ['S', 'E']))
        grid[s[0]][s[1]], grid[e[0]][e[1]] = ord('a'), ord('z')
        visited = {s: 0}
        bfs = [s]
        while bfs[0] != e:
            n = bfs.pop(0)
            for st in STEPS:
                pos = (n[0] + st[0], n[1] + st[1])
                if pos not in visited and 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0]) \
                        and grid[pos[0]][pos[1]] <= grid[n[0]][n[1]] + 1:
                    bfs.append(pos)
                    visited[pos] = visited[n] + 1
        print(visited[e])

    def test_part2(self):
        grid = read_data('input12.txt')
        e = find_nodes(grid, 'E')[0]
        grid[e[0]][e[1]] = ord('z')
        shortest_path = 9999999999
        start_points = find_nodes(grid, 'a')
        for s in start_points:
            visited = {s: 0}
            bfs = [s]
            while bfs and bfs[0] != e:
                n = bfs.pop(0)
                for st in STEPS:
                    pos = (n[0] + st[0], n[1] + st[1])
                    if pos not in visited and 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0]) \
                            and grid[pos[0]][pos[1]] <= grid[n[0]][n[1]] + 1:
                        bfs.append(pos)
                        visited[pos] = visited[n] + 1
            if e in visited:
                shortest_path = min(shortest_path, visited[e])
        print(shortest_path)


if __name__ == '__main__':
    unittest.main()
