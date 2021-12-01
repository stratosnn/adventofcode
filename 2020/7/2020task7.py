import unittest
import re
from pprint import pprint


def read_data(filename):
    mapping = dict()
    with open(filename) as f:
        for l in f:
            m = re.search(r'(.*) bags contain (.*bags*)[,.]', l)
            key = m.group(1)
            if m.group(2) == 'no other bags':
                contains = ['0 STOP bag']
            else:
                contains = map(str.strip, m.group(2).split(','))
            for bg in contains:
                bgm = re.search(r'(\d+) (.*) bag.*', bg)
                cnt = int(bgm.group(1))
                name = bgm.group(2)
                mapping.setdefault(key, []).append((name, cnt))
        return mapping


def simple_reverse_graph(data):
    rvrsd = dict()
    for k, v in data.items():
        for (bag, cnt) in v:
            rvrsd.setdefault(bag, []).append(k)
    return rvrsd


def walk_color(color, data, processed=set()):
    childs = data.get(color, [])
    #print(childs)

    res = sum([walk_color(c, data, processed) for c in filter(lambda x: x not in processed, childs)])
    processed |= set(childs)
    #print(f'result {res} set {processed}')
    return len(processed)


def get_inner_bags(color, bags):
    if color == 'STOP':
        return 1
    #print(bags)
    r = [cnt + cnt * get_inner_bags(bg, bags) for (bg, cnt) in bags[color]]
    #print(r)
    return sum(r)


class MyTestCase(unittest.TestCase):
    def test_something(self):
        data = read_data('input7.txt')
        #print(data)
        rvrsd = simple_reverse_graph(data)
        #pprint(rvrsd)
        print(f'total {walk_color("shiny gold", rvrsd)}')

    def test_something2(self):
        data = read_data('input7.txt')
        #pprint(data)
        print(f'Number of bags {get_inner_bags("shiny gold", data)}')


if __name__ == '__main__':
    unittest.main()
