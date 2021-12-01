import unittest
from copy import deepcopy


def read_data(filename):
    with open(filename) as f:
        return [int(x) for x in f.read().split(',')]


# def get_args(mem, ix, asm, nargs):
#     asm = f'{mem[ix]:05d}'
#     return [mem[mem[ix+shift]] if asm[-2-shift] == '0' else mem[ix+shift] for shift in range(1, nargs)]
#     #arg1 = mem[mem[ix+1]] if asm[-3] == '0' else mem[ix+1]


class MyTestCase(unittest.TestCase):
    def test_something(self):
        mem = read_data('input5.txt')
        ix = 0
        while ix < len(mem):
            asm = f'{mem[ix]:05d}'
            instr = int(asm[-2:])
            if instr == 1:  # add
                arg1 = mem[mem[ix+1]] if asm[-3] == '0' else mem[ix+1]
                arg2 = mem[mem[ix+2]] if asm[-4] == '0' else mem[ix+2]
                mem[mem[ix+3]] = arg1 + arg2
                ix += 4
            elif instr == 2:  # multi
                arg1 = mem[mem[ix+1]] if asm[-3] == '0' else mem[ix+1]
                arg2 = mem[mem[ix+2]] if asm[-4] == '0' else mem[ix+2]
                mem[mem[ix+3]] = arg1 * arg2
                ix += 4
            elif instr == 3:  # input
                mem[mem[ix+1]] = 5  # regs[0]
                ix += 2
            elif instr == 4:  # output
                arg1 = mem[mem[ix+1]] if asm[-3] == '0' else mem[ix+1]
                print(f'outout {arg1}')
                ix += 2
            elif instr == 5:  # jump-if-true
                arg1 = mem[mem[ix+1]] if asm[-3] == '0' else mem[ix+1]
                arg2 = mem[mem[ix+2]] if asm[-4] == '0' else mem[ix+2]
                ix = arg2 if arg1 != 0 else ix + 3
            elif instr == 6:  # jump-if-false
                arg1 = mem[mem[ix+1]] if asm[-3] == '0' else mem[ix+1]
                arg2 = mem[mem[ix+2]] if asm[-4] == '0' else mem[ix+2]
                ix = arg2 if arg1 == 0 else ix + 3
            elif instr == 7:  # less than
                arg1 = mem[mem[ix+1]] if asm[-3] == '0' else mem[ix+1]
                arg2 = mem[mem[ix+2]] if asm[-4] == '0' else mem[ix+2]
                mem[mem[ix+3]] = 1 if arg1 < arg2 else 0
                ix += 4
            elif instr == 8:  # equals
                arg1 = mem[mem[ix+1]] if asm[-3] == '0' else mem[ix+1]
                arg2 = mem[mem[ix+2]] if asm[-4] == '0' else mem[ix+2]
                mem[mem[ix+3]] = 1 if arg1 == arg2 else 0
                ix += 4
            elif instr == 99:
                ix += 1
                return
            else:
                raise Exception(f'Unexpected opcode {instr}')


if __name__ == '__main__':
    unittest.main()
