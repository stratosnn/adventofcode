import unittest
from pprint import pprint
import itertools
import math
import re


def read_data(filename):
    with open(filename) as f:
        data = f.readlines()
        ix = data.index('\n')
        raw_rules = list(map(str.strip, data[:ix]))
        messages = list(map(str.strip, data[ix+1:]))

        rules = dict()
        for l in raw_rules:
            rule_ix, rule_data = l.split(':')
            rules[rule_ix] = []
            for r in [rd.strip() for rd in rule_data.split('|')]:
                rules[rule_ix].append([rule.replace('"', '').strip() for rule in r.split(' ')])

        return rules, messages


def matches(msg, ix, input_rix, rules):
    rule = rules[input_rix]
    for rl in rule:  # pipe level
        for rix, r in enumerate(rl):  # rule level
            if r in ['a', 'b']:
                return 1 if msg[ix] == r else 0
            res = matches(msg, ix+rix, r, rules)
            if res - 1 == ix:
                return 1 + res
    return 0


def create_rex(rix, rules, depth=0):
    if depth >= 30:
        return ''

    result = []
    if rix in ['a', 'b']:
        return rix

    rule = rules[rix]

    for rl in rule:  # pipe level
        result.append(''.join([create_rex(r, rules, depth + 1) for r in rl]))

    if len(result) == 1:
        return f'{str(result[0])}'
    else:
        tmp = "|".join([f'{str(rs)}' for rs in result])
        return f'({tmp})'


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        rules, messages = read_data('input19.txt')
        rex = f'^{create_rex("0", rules)}$'
        print(rex)
        cnt = 0
        for m in messages:
            yes = bool(re.match(rex, m))
            print(yes, m)
            cnt += yes

        print(cnt)
        #pprint(messages)

    def test_part2(self):
        rules, messages = read_data('input19.txt')
        rules['8'] = [['42'], ['42', '8']]
        rules['11'] = [['42', '31'], ['42', '11', '31']]
        rex = f'^{create_rex("0", rules)}$'
        print(rex)
        cnt = 0
        for m in messages:
            yes = bool(re.match(rex, m))
            print(yes, m)
            cnt += yes

        print(cnt)


if __name__ == '__main__':
    unittest.main()
