import unittest
import functools
import operator
import re


def parse_data(filename):
    result = []
    with open(filename) as f:
        entry = dict()
        for line in f:
            tokens = line.strip().split(' ')
            if len(tokens) == 1 and not tokens[0]:
                result.append(entry)
                entry = dict()
            else:
                #print(tokens)
                for t in tokens:
                    key, value = t.split(':')
                    entry[key] = value
    return result


def get_validation_func(key):
    def validate_hgt(v):
        try:
            unit = v[-2:]
            hgt = int(v[0:-2])
            if unit == 'cm':
                return 150 <= hgt <= 193
            elif unit == 'in':
                return 59 <= hgt <= 79
            else:
                print(f'Invalid entry {v}')
                return False
        except:
            print(f'Invalid entry {v}')
            return False

    mapping = {'byr': lambda v: 1920 <= int(v) <= 2002,
               'iyr': lambda v: 2010 <= int(v) <= 2020,
               'eyr': lambda v: 2020 <= int(v) <= 2030,
               'hgt': validate_hgt,
               'hcl': lambda v: bool(re.match('^#[0-9a-f]{6}$', v)),
               'ecl': lambda v: v in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
               'pid': lambda v: bool(re.match('^[0-9]{9}$', v)),
               'cid': lambda v: True
               }
    return mapping[key]


def filter_data(entry):
    res = [get_validation_func(k)(v) for k, v in entry.items()]
    #print({k: get_validation_func(k)(v) for k, v in entry.items()})
    return all(res)



class MyTestCase(unittest.TestCase):
    def test_something(self):
        cnt = 0
        required = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
        data = parse_data('input4.txt')
        for d in data:
            current_set = set(d)
            cnt += 1 if len(current_set.intersection(required)) == len(required) else 0
        print(f'{cnt}/{len(data)}')
        fcnt = 0
        filtered = filter(filter_data, data)
        for d in filtered:
            current_set = set(d)
            fcnt += 1 if len(current_set.intersection(required)) == len(required) else 0
        print(f'{fcnt}/{len(data)}')


if __name__ == '__main__':
    unittest.main()
