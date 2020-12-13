import sys
from random import random

def f(n):
    if n < 2:
        return 1
    s = 0
    for k in range(1, n+1):
        if random() < 0.5:
            s += f(k)
    return s


if __name__ == '__main__':
    try:
        for i in range(0, int(sys.argv[1]) + 1):
            r = 500
            avg = sum([f(i) for _ in range(0, r)]) / r
            print(f'n = {i}   ==>   ~f({i}) = {avg}')
    except ValueError:
        print(f'Nieprawidłowa wartość n - {sys.argv[1]} - podaj liczbę naturalną')
    except IndexError:
        print(f'Podaj wartość n jako pierwszy argument')