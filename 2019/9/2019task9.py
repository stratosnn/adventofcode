import unittest
from copy import deepcopy
from itertools import permutations


def read_data(filename):
    with open(filename) as f:
        return [int(x) for x in f.read().split(',')]


def parse_arg(mem, ix, base, asm, nargs):
    args = []
    #print(f'ix {ix} base {base} asm {asm} nargs {nargs}')
    for i in range(nargs):
        if asm[-(i+1)] == '0':
            args.append(mem[mem[ix+(i+1)]])
        elif asm[-(i+1)] == '1':
            args.append(mem[ix+(i+1)])
        elif asm[-(i+1)] == '2':
            args.append(mem[base + mem[ix+(i+1)]])
    return args


def get_pos(mem, ix, base, asm):
    #print(f'ix {ix} base {base} asm {asm}')
    if asm == '0':
        return mem[ix]
    elif asm == '1':
        raise Exception(f'Unexpected mode for output arg ix {ix} asm {asm}')
    elif asm == '2':
        return base + mem[ix]


def run_compute_engine(mem, stack=[]):
    base = 0
    ix = 0
    output = []
    while ix < len(mem):
        asm = f'{mem[ix]:05d}'
        instr = int(asm[-2:])
        params = asm[0:-2]
        if instr == 1:  # add
            arg1, arg2 = parse_arg(mem, ix, base, params, 2)
            mem[get_pos(mem, ix+3, base, params[0])] = arg1 + arg2
            ix += 4
        elif instr == 2:  # multi
            arg1, arg2 = parse_arg(mem, ix, base, params, 2)
            mem[get_pos(mem, ix+3, base, params[0])] = arg1 * arg2
            ix += 4
        elif instr == 3:  # input
            mem[get_pos(mem, ix+1, base, params[2])] = stack.pop(0)
            ix += 2
        elif instr == 4:  # output
            arg1 = parse_arg(mem, ix, base, params, 1)[0]
            print(f'outout {arg1}')
            #yield arg1
            ix += 2
        elif instr == 5:  # jump-if-true
            arg1, arg2 = parse_arg(mem, ix, base, params, 2)
            ix = arg2 if arg1 != 0 else ix + 3
        elif instr == 6:  # jump-if-false
            arg1, arg2 = parse_arg(mem, ix, base, params, 2)
            ix = arg2 if arg1 == 0 else ix + 3
        elif instr == 7:  # less than
            arg1, arg2 = parse_arg(mem, ix, base, params, 2)
            mem[get_pos(mem, ix+3, base, params[0])] = 1 if arg1 < arg2 else 0
            ix += 4
        elif instr == 8:  # equals
            arg1, arg2 = parse_arg(mem, ix, base, params, 2)
            mem[get_pos(mem, ix+3, base, params[0])] = 1 if arg1 == arg2 else 0
            ix += 4
        elif instr == 9:  # relative base shift
            arg1 = parse_arg(mem, ix, base, params, 1)[0]
            base += arg1
            ix += 2
        elif instr == 99:
            ix += 1
            return output
        else:
            raise Exception(f'Unexpected opcode {instr}')
    return output


class MyTestCase(unittest.TestCase):
    def test_something(self):
        mem = read_data('input9.txt') + ([0] * 34463338)
        stack = [2]
        run_compute_engine(mem, stack)


if __name__ == '__main__':
    unittest.main()
