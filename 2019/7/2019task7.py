import unittest
from copy import deepcopy
from itertools import permutations


def read_data(filename):
    with open(filename) as f:
        return [int(x) for x in f.read().split(',')]


def run_compute_engine(mem, input=[]):
    ix = 0
    output = []
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
            mem[mem[ix+1]] = input.pop(0)
            ix += 2
        elif instr == 4:  # output
            arg1 = mem[mem[ix+1]] if asm[-3] == '0' else mem[ix+1]
            #print(f'outout {arg1}')
            output.append(arg1)
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
            return output
        else:
            raise Exception(f'Unexpected opcode {instr}')
    return output


def compute_engine2(mem, phase, stack):
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
            if phase is not None:
                mem[mem[ix+1]] = phase
                phase = None
            else:
                mem[mem[ix+1]] = stack.pop(0)
            ix += 2
        elif instr == 4:  # output
            arg1 = mem[mem[ix+1]] if asm[-3] == '0' else mem[ix+1]
            print(f'outout {arg1}')
            # stack.insert(1, arg1)
            yield arg1
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
    raise Exception('Reached the end!')


class MyTestCase(unittest.TestCase):
    def test_something(self):
        srcmem = read_data('input7.txt')
        max_thrust = 0
        for amp_inputs in permutations(range(5)):
            inputs = list(amp_inputs)
            inputs.insert(1, 0)
            out = 0
            for i in range(5):
                mem = deepcopy(srcmem)
                outs = run_compute_engine(mem, inputs)
                assert len(outs) == 1
                out = outs[0]
                inputs.insert(1, out)
            max_thrust = max(max_thrust, out)
        print(f'max_thrust {max_thrust}')

    def test_task2(self):
        srcmem = read_data('input7.txt')
        max_thrust = 0
        for amp_inputs in permutations(range(5, 10)):
            inputs = list(amp_inputs)
            engines = []
            stack = [0]
            for i in range(5):
                mem = deepcopy(srcmem)
                engines.append(compute_engine2(mem, inputs[i], stack))

            while True:
                try:
                    for i in range(5):
                        stack.insert(0, next(engines[i]))
                except StopIteration:
                    print(f'Stopped {stack}')
                    max_thrust = max(max_thrust, stack[0])
                    break
        print(f'Max thrust {max_thrust}')


if __name__ == '__main__':
    unittest.main()
