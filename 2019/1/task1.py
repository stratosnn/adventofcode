import functools
import operator


def recursive_calc_mass(mass):
    fuel = int(mass / 3) - 2
    return fuel + recursive_calc_mass(fuel) if fuel > 0 else 0


def run(filename):
    with open(filename) as f:
        lst = [int(x.strip()) for x in f.readlines()]
        masses = map(lambda x: int(x/3) - 2, lst)
        return functools.reduce(operator.add, masses), functools.reduce(operator.add, map(recursive_calc_mass, lst))


def gsum(b1, q, n):
    return (b1 * (1 - q**n)) / (1 - q)


if __name__ == "__main__":
    print(run("input1.txt"))