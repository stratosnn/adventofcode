import unittest
import functools
from pprint import pprint


def read_and_split_data(filename, width, height):
    with open(filename) as f:
        layers = []
        while True:
            layer = []
            for i in range(height):
                data = f.read(width).strip()
                if len(data) == 0:
                    return layers
                layer.append([int(x) for x in data])
            layers.append(layer)


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def merge_layers(prev, next):
    return [n if p == 2 else p for p, n in zip(prev, next)]


class MyTestCase(unittest.TestCase):
    def test_something(self):
        image = read_and_split_data('input8.txt', 25, 6)
        min_zeros, selected_layer = 90000, 0
        print(f'Number of layer {len(image)}')
        # assert all([len(x) == 25 * 6 for x in image])
        for ix, layer in enumerate(image):
            flat = [b for sublist in layer for b in sublist]
            print(flat)
            sm = flat.count(0)
            if sm < min_zeros:
                min_zeros = sm
                selected_layer = ix
        layer = image[selected_layer]
        flat = [b for sublist in layer for b in sublist]
        print(flat.count(1) * flat.count(2))


    def test_part2(self):
        image = read_and_split_data('input8.txt', 25, 6)
        print(f'Number of layer {len(image)}')

        flat = []
        for layer in image:
            flat.append([b for sublist in layer for b in sublist])

        result = functools.reduce(merge_layers, flat, [2]*25*6)
        result = [8 if x == 1 else 1 for x in result]
        pprint([x for x in chunks(result, 25)])


if __name__ == '__main__':
    unittest.main()
