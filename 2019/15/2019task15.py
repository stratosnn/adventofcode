import unittest
from pprint import pprint
import itertools
import math
from copy import deepcopy
from collections import deque


def read_data(filename):
    with open(filename) as f:
        return [int(x) for x in f.read().split(',')]


def parse_arg(mem, ix, base, asm, nargs):
    args = []
    # print(f'ix {ix} base {base} asm {asm} nargs {nargs}')
    for i in range(nargs):
        if asm[-(i+1)] == '0':
            args.append(mem[mem[ix+(i+1)]])
        elif asm[-(i+1)] == '1':
            args.append(mem[ix+(i+1)])
        elif asm[-(i+1)] == '2':
            args.append(mem[base + mem[ix+(i+1)]])
    return args


def get_pos(mem, ix, base, asm):
    # print(f'ix {ix} base {base} asm {asm}')
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
            # print(f'outout {arg1}')
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


DIRECTIONS = [1, 2, 3, 4]
REVERSE = [None, 2, 1, 4, 3]
OFFSETS = [None, (0, 1), (0, -1), (-1, 0), (1, 0)]


def search(mem, distance, pos, action, visited={}):
    # prevent from going where we have been already
    if visited.setdefault(pos, 2 ** 30) < distance:
        return

    status = 1 if action is None else next(run_compute_engine(mem, [action]))
    # print(f'Position {pos} d {distance} a {action} s {status}')

    if status == 0:
        visited[pos] = -1
    elif status == 1:
        visited[pos] = distance
        for d in DIRECTIONS:
            newpos = pos[0] + OFFSETS[d][0], pos[1] + OFFSETS[d][1]
            # print(f'Entering search in direction {d} new pos {newpos}')
            search(mem, distance + 1, newpos, d, visited)
    elif status == 2:
        visited[pos] = distance
        print(f'Position found {pos} distance {visited[pos]}')

    # reverse actions when applicable
    if status != 0 and action is not None:
        next(run_compute_engine(mem, [REVERSE[action]]))
        assert status != 0


def bfs_fill(start, visited):
    queue = deque([start])
    new_queue = deque()
    cnt = 0
    while len(queue) > 0:
        e = queue.pop()
        del visited[e]
        for new_el in [(e[0], e[1] + 1), (e[0], e[1] - 1), (e[0] + 1, e[1]), (e[0] - 1, e[1])]:
            if 0 <= visited.get(new_el, -1) < 2 ** 30:
                new_queue.append(new_el)
        if len(queue) == 0:
            cnt += 1
            queue, new_queue = new_queue, queue
    return cnt - 1  # we don't count the very first position


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        mem = read_data('input15.txt') + [0]*1024*1024
        visited = {(0, 0): 0}
        search(mem, 0, (0, 0), None, visited)

    def test_part2(self):
        mem = read_data('input15.txt') + [0]*1024*1024
        visited = {(0, 0): 0}
        search(mem, 0, (0, 0), None, visited)
        # Position found (-20, -18) distance 270
        print(bfs_fill((-20, -18), visited))


if __name__ == '__main__':
    unittest.main()
