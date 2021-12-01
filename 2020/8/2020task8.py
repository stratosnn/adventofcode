import unittest
from copy import deepcopy


def read_data(filename):
    with open(filename) as f:
        return [x for x in map(lambda v: (v[0], int(v[1])), [line.strip().split(' ') for line in f.readlines()])]


def run_comp(mem):
    acc = 0
    ix = 0
    visited = set()
    while ix < len(mem):
        i, param = mem[ix]
        if i == 'nop':
            ix += 1
        elif i == 'acc':
            acc += param
            ix += 1
        elif i == 'jmp':
            ix += param
        else:
            raise Exception(f'Unknown op {i, param}')

        if ix in visited:
            return acc
        else:
            visited.add(ix)
    print(f'reached end! {acc}')
    return acc


def alter(instr):
    i, offset = instr
    return ('nop', offset) if i == 'jmp' else ('jmp', offset)


class MyTestCase(unittest.TestCase):
    def test_something(self):
        mem = read_data('input8.txt')
        print(run_comp(mem))

    def test_loop(self):
        omem = read_data('input8.txt')
        alterable = map(lambda e: e[0], filter(lambda i: i[1] in ['nop', 'jmp'], [(ix, opcode[0]) for ix, opcode in enumerate(omem)]))
        for p in alterable:
            mem = deepcopy(omem)
            mem[p] = alter(mem[p])
            run_comp(mem)

if __name__ == '__main__':
    unittest.main()
