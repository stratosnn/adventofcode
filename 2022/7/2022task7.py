import unittest


class Entry:
    files = {}
    dirs = []
    size = 0

    def __init__(self, files: dict, dirs: list, size: int):
        self.files = files
        self.dirs = dirs
        self.size = size


def read_data(filename):
    with open(filename) as f:
        f.readline()  # first one is cd root, we can ignore
        catalog = {'': Entry({}, [], 0)}
        path = ''
        for line in f.readlines():
            cmd = [c.strip() for c in line.strip().split(' ')]
            if cmd[0] == '$':
                if cmd[1] == "cd":
                    if cmd[2] == "..":
                        newpath = path.split('/')
                        newpath.pop()
                        path = '/'.join(newpath)
                    else:
                        path = '/'.join(path.split('/') + [cmd[2]])
                elif cmd[1] == 'ls':
                    pass
            elif cmd[0] == 'dir':
                e = catalog.setdefault(path, Entry({}, [], 0))
                e.dirs.append(cmd[1])
            else:
                e = catalog.setdefault(path, Entry({}, [], 0))
                e.files[cmd[1]] = int(cmd[0])
        return catalog


def get_sizes(catalog: dict, path: str):
    entry = catalog[path]
    sizes = 0 + sum(entry.files.values()) + + sum(map(lambda p: get_sizes(catalog, p), map(lambda d: path + '/' + d, entry.dirs)))
    entry.size = sizes
    return sizes


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        catalog = read_data('input7.txt')
        get_sizes(catalog, '')
        print(sum(filter(lambda s: s <= 100000, map(lambda e: e.size, catalog.values()))))
        pass

    def test_part2(self):
        catalog = read_data('input7.txt')
        get_sizes(catalog, '')
        space_needed = 30000000 - (70000000 - catalog[''].size)
        ordered = sorted(map(lambda e: e.size, catalog.values()))
        print(list(filter(lambda x: x >= space_needed, ordered))[0])
        pass


if __name__ == '__main__':
    unittest.main()
