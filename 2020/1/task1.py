import sys


def parse_input(filename):
    with open(filename) as f:
        content = f.readlines()
    return [int(x.strip()) for x in content]


def run(filename):
    lst = parse_input(filename)
    for ix, e1 in enumerate(lst):
        lst2 = lst[ix:]
        for jx, e2 in enumerate(lst2):
            for kx, e3 in enumerate(lst2[jx:]):
                if e1 + e2 + e3 == 2020:
                    print(f'{e1} ({ix}) + {e2} ({jx}) + {e3} ({kx})== 2020, multiply {e1*e2*e3}')
            #print(f'{ix}/{len(lst)}')


if __name__ == '__main__':
    #run(sys.argv[1])
    run('input1.txt')
