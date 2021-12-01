import unittest
from pprint import pprint
import itertools
import math
import functools

def read_data(filename):
    with open(filename) as f:
        data = list(map(str.strip, f.readlines()))
        ix = data.index('')
        rules_data = data[:ix]

        rules = {}
        for rule in rules_data:
            field, ranges_data = tuple(map(str.strip, rule.split(':')))
            first, _, second = ranges_data.split(' ')
            rules[field] = [tuple(int(v) for v in first.split('-')), tuple(int(v) for v in second.split('-'))]

        rest = data[ix+2:]
        ix = rest.index('')
        your_data = rest[:ix]
        yours = [int(v) for v in your_data[0].split(',')]

        other_data = rest[ix+2:]
        other = [[int(v) for v in l.split(',')] for l in other_data]

        return rules, yours, other


def satisfies(value, ranges):
    return any([r[0] <= value <= r[1] for r in ranges])


class MyTestCase(unittest.TestCase):
    def test_part1(self):
        rules_data, _, other = read_data('input16.txt')
        invalid = []
        rules = []
        for v in rules_data.values():
            rules += [v[0], v[1]]

        for ticket in other:
            for v in ticket:
                valid = any(map(lambda rng: rng[0] <= v <= rng[1], rules))
                if not valid:
                    invalid.append(v)
        print(sum(invalid), invalid)


    def test_part2(self):
        rules_data, yours, other = read_data('input16.txt')
        valid_tickets = []
        rules = []
        for v in rules_data.values():
            rules += [v[0], v[1]]

        for ticket in other:
            if all([any(map(lambda rng: rng[0] <= v <= rng[1], rules)) for v in ticket]):
                valid_tickets.append(ticket)

        print(valid_tickets)

        matching_fields = {}
        for k, ranges in rules_data.items():
            print(f'Searching fields for {k} ranges {ranges}')
            matching_fields[k] = []
            for fix in range(len(valid_tickets[0])):  # iterate over fields
                if all([satisfies(t[fix], ranges) for t in valid_tickets]):
                    #print(f'field index {fix} passes')
                    matching_fields[k].append(fix)

        pprint(matching_fields)

        print(list(sorted([len(v) for v in matching_fields.values()])))

        mapping = {}

        for i in range(len(valid_tickets[0])):
            fix = None
            for k, v in matching_fields.items():
                if len(v) == 1:
                    fix = v[0]
                    mapping[k] = fix
            for k, v in matching_fields.items():
                if fix in v:
                    v.remove(fix)
        pprint(mapping)  # not 1497600

        departures = {}
        for k, v in mapping.items():
            if 'departure' in k:
                departures[k] = v

        m = 1
        for k, v in departures.items():
            m *= yours[v]
        print(m)



if __name__ == '__main__':
    unittest.main()
