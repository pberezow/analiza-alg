import math
from utils import get_random_multiset, get_test_multiset, plot_5b, plot_8, plot_hash_values
from hash_functions import fibonacci_hash, hyper_fib_hash, hyper_hash_function
from min_count import MinCount
from hyper_log_log import HyperLogLog
import timeit
import time

if __name__ == '__main__':
    # uni = 3000000
    # # multiset = get_test_multiset(uni)
    # multiset = get_random_multiset(uni, seed=10)

    # k = 100
    # h_func = lambda x : fibonacci_hash(x, 32)
    # count = MinCount.min_count(multiset, h_func, k)

    # print(f'MinCount result: {count}')

    # t1 = time.time()
    # hll = HyperLogLog(hyper_fib_hash, 12)
    # for x in multiset:
    #     hll.add(x)
    # count = len(hll)
    # t2 = time.time()
    # print(f'HyperLogLog result: {count}    in {t2-t1} sec')

    # t1 = time.time()
    # count = HyperLogLog.paralell_hyper_log_log(multiset, h=hyper_fib_hash, b=12)
    # t2 = time.time()
    # print(f'Parallel HyperLogLog result: {count}    in {t2-t1} sec')


    # plot_5b(data_gen=lambda x : get_random_multiset(x, 1))
    plot_8(max_set_len=20000, data_gen=lambda x : get_random_multiset(x, 10))
    # plot_hash_values(hyper_fib_hash, get_test_multiset(100000))
