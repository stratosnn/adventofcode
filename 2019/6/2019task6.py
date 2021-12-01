import unittest


def read_data(filename):
    with open(filename) as f:
        return {k.strip(): v.strip() for v, k in map(lambda x: x.split(')'), f.readlines())}


def get_depth(universe, planet, end='COM'):
    if planet == end:
        return 0
    else:
        return 1 + get_depth(universe, universe[planet], end)


def get_path(universe, planet, end='COM'):
    return [end] if planet == end else [planet] + get_path(universe, universe[planet], end)


class MyTestCase(unittest.TestCase):
    def test_something(self):
        cnt = 0
        data = read_data('input6.txt')
        for k, v in data.items():
            cnt += get_depth(data, k)
        print(f'checksum {cnt}')

        path_from_you = get_path(data, 'YOU')
        path_from_san = get_path(data, 'SAN')

        overlap = (set(path_from_san).intersection(set(path_from_you)))
        point = None
        for p in path_from_you:
            if p in overlap:
                point = p
                break

        print(path_from_you)
        print(path_from_san)
        print(overlap)
        print(point)
        print(f'Distance via {point} is {get_depth(data, "YOU", point) + get_depth(data, "SAN", point) - 2}')
        #print(min([get_depth(data, "YOU", p) + get_depth(data, "SAN", p) - 2 for p in overlap]))



if __name__ == '__main__':
    unittest.main()
