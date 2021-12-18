import unittest
from pprint import pprint
import itertools
import functools
import copy
import collections
import binarytree
from binarytree import Node


def build(snailfish):
    if isinstance(snailfish, int):
        return Node(snailfish)
    elif isinstance(snailfish, list):
        return Node(-1, left=build(snailfish[0]), right=build(snailfish[1]))
    else:
        assert 0 and "Unexpected result"


def read_data(filename):
    with open(filename) as f:
        result = []
        for line in f.readlines():
            result.append(build(eval(line)))
        return result


def explode(node: Node, root: Node):
    assert node.value == -1 and node.left.value >= 0 and node.right.value >= 0
    leaves = [n for n in root.inorder if n.value >= 0]
    ix_left = leaves.index(node.left)
    if ix_left > 0:
        leaves[ix_left - 1].value += node.left.value
    if ix_left + 2 < len(leaves):  # element next to the right
        leaves[ix_left + 2].value += node.right.value
    node.value, node.left, node.right = 0, None, None


def split(node: Node):
    assert node.value >= 10 and node.left is None and node.right is None
    node.left = Node(node.value // 2)
    node.right = Node((node.value + 1) // 2)
    node.value = -1


def seek_and_explode(root: Node):
    levels = root.levels
    if len(levels) > 5:
        explode(binarytree.get_parent(root, levels[-1][0]), root)
        return True
    else:
        return False


def seek_and_split(root: Node):
    splitable = [x for x in root.inorder if x.value >= 10]
    if len(splitable) > 0:
        split(splitable[0])
        return True
    else:
        return False


def snailfish_sum(left: Node, right: Node):
    tree = Node(-1, left=left, right=right)
    while seek_and_explode(tree) or seek_and_split(tree):
        pass
    return tree


def magnitude(node: Node):
    if node.value >= 0:
        return node.value
    else:
        return 3*magnitude(node.left) + 2*magnitude(node.right)


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        numbers = read_data('input1.txt')
        result = functools.reduce(snailfish_sum, numbers)
        print(f' resulting pair {result} magnitude {magnitude(result)}')

    def test_part2(self):
        magnitudes = []
        numbers = read_data('input1.txt')
        for i, x in enumerate(numbers):
            print(f'{i+1}/{len(numbers)}')
            for y in numbers[i+1:]:
                magnitudes.append(magnitude(snailfish_sum(x.clone(), y.clone())))
                magnitudes.append(magnitude(snailfish_sum(y.clone(), x.clone())))
        print(max(magnitudes))


if __name__ == '__main__':
    unittest.main()
