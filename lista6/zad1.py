import sys
from time import time
from numba import jit

@jit(nopython=True)
def f(n):
    if n == 0:
        return 1, 0
    
    s = 0
    calls = 0
    for i in range(n):
        x, y = f(i)
        s += x
        calls += y + 1
    return s, calls

if __name__ == '__main__':
    try:
        for i in range(0, int(sys.argv[1]) + 1):
            t0 = time()
            res = f(i)
            t1 = time()
            # print(f'n = {i}   ==>   f({i}) = {res}      [{t1-t0} sec.]')
            print(f'{i} & {2**i - 1} & {res[1]} \\\\')
    except ValueError:
        print(f'Nieprawidłowa wartość n - {sys.argv[1]} - podaj liczbę naturalną')
    except IndexError:
        print(f'Podaj wartość n jako pierwszy argument')
