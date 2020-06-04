import math
import time
from matplotlib import pyplot as plt

from utils import *
from hash_functions import *
from min_count import MinCount
from hyper_log_log import HyperLogLog


def test():
    uni = 5000000
    multiset = get_random_multiset(uni, seed=10)

    k = 100
    h_func = lambda x : hash1(x, 32)
    
    t1 = time.time()
    count = MinCount.min_count(multiset, h_func, k)
    t2 = time.time()
    print(f'MinCount result: {count}  d={abs(count-uni)/uni}    in {t2-t1} sec')

    t1 = time.time()
    hll = HyperLogLog(hyper_hash1, 12)
    for x in multiset:
        hll.add(x)
    count = len(hll)
    t2 = time.time()
    print(f'HyperLogLog result: {count}  d={abs(count-uni)/uni}    in {t2-t1} sec')

    t1 = time.time()
    count = HyperLogLog._paralell_hyper_log_log(multiset, hyper_hash1, 12)
    t2 = time.time()
    print(f'Parallel HyperLogLog result: {count}  d={abs(count-uni)/uni}    in {t2-t1} sec')


if __name__ == '__main__':
    # Zad 5
    # plot_5b()
    # plot_5c()

    # Zad 6
    # a()
    plot_7a()
    # plot_8_comp()

    # plot_5b(data_gen=lambda x : get_random_multiset(x, seed=10))
    # plot_8(max_set_len=20000, data_gen=lambda x : get_random_multiset(x, 10))
    # plot_hash_values(hyper_fib_hash, get_test_multiset(100000))
