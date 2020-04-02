import math
import time
from matplotlib import pyplot as plt

from utils import get_random_multiset, get_test_multiset, plot_5b, plot_8, plot_hash_values, chebyshev_delta
from hash_functions import *
from min_count import MinCount
from hyper_log_log import HyperLogLog


def a():
    results_shift = ([], [])
    results_hash = ([], [])
    for n in range(1, 30000):
        ms = get_random_multiset(n, seed=10)
        count1 = MinCount.min_count(ms, h=shift_hash, k=400)
        results_shift[0].append(n)
        results_shift[1].append(count1/n)
        count2 = MinCount.min_count(ms, h=hash1, k=400)
        results_hash[0].append(n)
        results_hash[1].append(count2/n)
        if n % 1000 == 1:
            print(n)

    plt.figure(figsize=(8,8))
    plt.plot(results_shift[0], results_shift[1], label='shift_hash')
    plt.legend()
    plt.plot(results_hash[0], results_hash[1], label='hash1')
    plt.legend()
    plt.grid()
    plt.ylabel("n' / n")
    plt.xlabel("n")
    plt.title(f"MinCount")
    plt.show()

def b():
    k = 400
    alpha = 0.005
    res = ([], [])
    for n in range(1, 1000):
        ms = get_random_multiset(n)
        est = MinCount.min_count(ms, k=400)
        res[0].append(n)
        res[1].append(est/n)
    
    delta = chebyshev_delta(alpha, k)
    print(delta)
    plt.figure()
    plt.plot(res[0], res[1])
    plt.plot(res[0], [1+delta for i in range(len(res[0]))], marker=1)
    plt.plot(res[0], [1-delta for i in range(len(res[0]))], marker=1)
    plt.grid()
    plt.show()


if __name__ == '__main__':
    # uni = 9000000
    # # multiset = get_test_multiset(uni)
    # multiset = get_random_multiset(uni, seed=10)

    # k = 100
    # h_func = lambda x : hash1(x, 32)
    
    # t1 = time.time()
    # count = MinCount.min_count(multiset, h_func, k)
    # t2 = time.time()
    # print(f'MinCount result: {count}  d={abs(count-uni)/uni}    in {t2-t1} sec')

    # t1 = time.time()
    # hll = HyperLogLog(hyper_hash1, 12)
    # for x in multiset:
    #     hll.add(x)
    # count = len(hll)
    # t2 = time.time()
    # print(f'HyperLogLog result: {count}  d={abs(count-uni)/uni}    in {t2-t1} sec')

    # t1 = time.time()
    # count = HyperLogLog._paralell_hyper_log_log(multiset, hyper_hash1, 12)
    # t2 = time.time()
    # print(f'Parallel HyperLogLog result: {count}  d={abs(count-uni)/uni}    in {t2-t1} sec')
    # a()
    b()

    # plot_5b(data_gen=lambda x : get_random_multiset(x, seed=10))
    # plot_8(max_set_len=20000, data_gen=lambda x : get_random_multiset(x, 10))
    # plot_hash_values(hyper_fib_hash, get_test_multiset(100000))
