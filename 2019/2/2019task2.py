import unittest
from copy import deepcopy

def read_data(filename):
    with open(filename) as f:
        return [int(x) for x in f.read().split(',')]


def exec_prog(inst, ix):
    #print(inst)
    opcode = inst[ix]
    if opcode == 99:
        return

    arg1 = inst[inst[ix+1]]
    arg2 = inst[inst[ix+2]]
    pos = inst[ix+3]
    #print(f'opcode {opcode}, {arg1}, {arg2} pos {pos}')
    if opcode == 1:  # add
        inst[pos] = arg1 + arg2
        exec_prog(inst, ix + 4)
    elif opcode == 2:  # multi
        inst[pos] = arg1 * arg2
        exec_prog(inst, ix + 4)
    elif opcode == 99:
        return
    else:
        return
        #raise Exception(f'invalid opcode {opcode} pos {ix}')


class MyTestCase(unittest.TestCase):
    def test_something(self):
        lst = read_data('input2.txt')
        for noun in range(0, 99):
            for verb in range(0, 99):
                mem = deepcopy(lst);
                mem[1] = noun
                mem[2] = verb
                exec_prog(mem, 0)
                if mem[0] == 19690720:
                    print(f'found {noun} {verb} keycode {100 * noun + verb}')
                    exit(0)


if __name__ == '__main__':
    unittest.main()
