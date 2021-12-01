import unittest
from pprint import pprint


def read_data(filename):
    with open(filename) as f:
        return [int(x) for x in f.readlines()]


class MyTestCase(unittest.TestCase):
    def test_something(self):
        data = [0] + sorted(read_data('input10.txt'))
        data = data + [max(data) + 3]

        diffs = [data[ix + 1] - data[ix] for ix in range(len(data) - 1)]
        print(f'data min {min(data)} max {max(data)}')
        print(f'diffs min {min(diffs)} max {max(diffs)}')
        print(f'count 1 diff {diffs.count(1)} 3 diff {diffs.count(3)} res {diffs.count(1) * diffs.count(3)} ')

    def test_something2(self):
        data = [0] + sorted(read_data('input10.txt'))
        data = data + [max(data) + 3]

        cnt = 0
        inedge = {0: 1}
        edgecnt = {0: 1}

        for ix in range(len(data)):
            e = data[ix]
            window = data[ix+1:ix+4]
            for we in filter(lambda x: x - e <= 3, window):
                inedge[we] = inedge.get(we, 0) + 1
                edgecnt[we] = edgecnt.setdefault(we, 0) + edgecnt[e]

            #pprint(inedge)
            #pprint(edgecnt)
            #branches = sum(map(lambda x: x - e <= 3, window))
            #cnt += branches if branches > 1 else 0
        #cnt += 1  # final branch

        #print(f'data min {min(data)} max {max(data)}')
        #print(f'data cnt {cnt}')
        key = max(edgecnt.keys())
        print(f' key {key} val {edgecnt[key]}')


if __name__ == '__main__':
    unittest.main()
