import unittest



def read_data(filename):
    result = []
    with open(filename) as f:
        group = set()
        for l in f:
            if len(l.strip()) == 0:
                result.append(group)
                group = set()
                continue
            for c in l.strip():
                group.add(c)
        return result


def read_data2(filename):
    result = []
    with open(filename) as f:
        group = set([chr(x) for x in range(ord('a'), ord('z')+1)])
        for l in f:
            if len(l.strip()) == 0:
                result.append(group)
                group = set([chr(x) for x in range(ord('a'), ord('z')+1)])
                continue
            group = group.intersection(set([c for c in l.strip()]))
        return result



class MyTestCase(unittest.TestCase):
    def test_something(self):
        groups = read_data('input6.txt')
        print(groups)
        total = sum([len(s) for s in groups])
        print(f'groups {len(groups)} total size {total}')

    def test_something2(self):
        groups = read_data2('input6.txt')
        print(groups)
        total = sum([len(s) for s in groups])
        print(f'groups {len(groups)} total size {total}')

if __name__ == '__main__':
    unittest.main()
