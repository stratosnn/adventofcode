import unittest
from operator import add
from pprint import pprint
import functools
from copy import deepcopy


global bposx
bposx = 0


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
        mem[392] = bposx
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
            mem[get_pos(mem, ix+1, base, params[2])] = yield
            ix += 2
        elif instr == 4:  # output
            arg1 = parse_arg(mem, ix, base, params, 1)[0]
            #mem[392] = 2
            #print(f'outout {arg1}')
            yield arg1
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


def pic(code):
    mapping = {0: ' ',
               1: '+',
               2: '#',
               3: '_',
               4: '@'}
    return mapping[code]


def render(pos, score):
    game = [[' ' for x in range(40)] for y in range(22)]
    for (x, y), p in pos.items():
        game[y][x] = pic(p)

    for l in game:
        print(''.join(l))
    print(score)


def trace(orig, diff1, diff2):
    print('DIff1:')
    print('')
    for ix in range(len(orig)):
        if orig[ix] != diff1[ix]:
            print(f'Missmatch pos {ix} orig {orig[ix]} diff1 {diff1[ix]}')

    print('DIff2:')
    print('')
    for ix in range(len(orig)):
        if orig[ix] != diff2[ix]:
            print(f'Missmatch pos {ix} orig {orig[ix]} diff2 {diff2[ix]}')

    print('between diffs:')
    print('')
    for ix in range(len(diff1)):
        if diff1[ix] != diff2[ix]:
            print(f'Missmatch pos {ix} diff1 {diff1[ix]} diff2 {diff2[ix]}')
    pass


def game_engine(filename):
    data = read_data(filename) + ([0] * 3446333)
    data[0] = 2
    engine = run_compute_engine(data, [])
    pos = dict()
    score = 0

    # data_orig = deepcopy(data)
    # data1 = []
    # data2 = []


    while True:
        try:
            probe = next(engine)
            # wants input
            if probe is None:
                render(pos, score)
                inp = 'a' #  input('')
                mp = {'a': -1, 's': 0, 'd': 1}
                key = mp[inp.strip()]
                probe = engine.send(key)
                # if not data1:
                #     data1 = deepcopy(data)
                # elif not data2:
                #     data2 = deepcopy(data)
                # else:
                #     trace(data_orig, data1, data2)

            x, y, tile = probe, next(engine), next(engine)
            if tile == 4:
                global bposx
                bposx = x
            if (x, y) == (-1, 0):
                score = tile
            else:
                pos[(x, y)] = tile
        except StopIteration:
            print(f'Done: {score}')
            break



class MyTestCase(unittest.TestCase):
    def test_something(self):
        data = read_data('input13.txt') + ([0] * 34463338)
        data[0] = 2
        stack = []
        engine = run_compute_engine(data, stack)
        pos = []
        score = 0
        while True:
            try:
                x = next(engine)
                y, tile = next(engine), next(engine)
                if not x:
                    pass
                elif (x, y) == (-1, 0):
                   score = tile
                else:
                    pos.append((x, y, tile))
            except StopIteration:
                break
        print(len([x for x in filter(lambda x: x[2] == 2, pos)]))
        print(f' max x {max(map(lambda x: x[0], pos))} max y{max(map(lambda x: x[1], pos))} size {len(pos)}')

        game = [[' ' for x in range(40)] for y in range(22)]
        for (x, y, p) in pos:
            game[y][x] = pic(p)

        for l in game:
            print(''.join(l))

    def test_part2(self):
        game_engine('input13.txt')


if __name__ == '__main__':
    unittest.main()
