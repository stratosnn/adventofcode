import functools
import operator
import re


def entry_valid(number, letter, password):
    letter = letter.replace(':', '')
    number = number.replace('-', ',')
    rex = f'.*({letter}.*){{{number}}}'
    m = bool(re.match(rex, password))
    #print(f'{rex} : {password} : {m}')
    return m


def dumb_match(number, letter, password):
    letter = letter.replace(':', '')
    min, max = [int(x) for x in number.split('-')]
    cnt = sum(map(lambda c: c == letter, password))
    return min <= cnt <= max


def policy2_match(number, letter, password):
    letter = letter.replace(':', '')
    pos1, pos2 = map(lambda x: int(x) - 1, number.split('-'))
    return sum(map(lambda l: l == letter, [password[pos1], password[pos2]])) == 1


def run(filename):
    with open(filename) as f:
        values = [l.split() for l in f]
        check = [entry_valid(*x) for x in values]
        check2 = [dumb_match(*x) for x in values]
        check3 = [policy2_match(*x) for x in values]
        return sum(check), sum(check2), sum(check3)




if __name__ == "__main__":
    print(run("input2.txt"))