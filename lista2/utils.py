import math
import random
from matplotlib import pyplot as plt
from min_count import MinCount
from hyper_log_log import HyperLogLog
from hash_functions import *


"""
"""
def chebyshev_delta(alpha, k):
    delta = math.sqrt(1/(k-2)) / math.sqrt(alpha)
    return delta

"""
Data generators
"""
def get_test_multiset(unique_elements, n_times_repeat=1):
    return [i for i in range(unique_elements) for j in range(n_times_repeat)]
        
def get_random_multiset(unique_elements, seed=None):
    if seed:
        random.seed(seed)
    a = set()
    while len(a) != unique_elements:
        a.add(random.randint(0, (1 << 32)-1))
    return list(a)

"""
Plotting
"""
def plot_hash_values(h, data_set):
    results = [h(x) for x in data_set]
    print('unique hashes: ', len(set(results)), '    all values: ', len(data_set))
    plt.figure()
    plt.scatter([i for i in range(len(data_set))], results, s=1.5)
    plt.grid()
    plt.xlabel('Value index')
    plt.ylabel('h(x)')
    plt.show()


def plot_5b(max_set_len=10000, step=1, data_gen=get_test_multiset):
    possible_k = [2, 3, 10, 100, 400]

    results = {}
    for k in possible_k:
        result_k = ([], [])
        results[k] = result_k

    for n in range(1, max_set_len, step):
        ms = data_gen(n)
        for k in possible_k:
            count = MinCount.min_count(ms, h=hash1, k=k)
            results[k][0].append(n)
            results[k][1].append(count/n)
        if n % 1000 == 1:
            print(n)

    plt.figure(figsize=(8,8))
    for k, arg in results.items():
        plt.plot(arg[0], arg[1], label=f'k = {k}')
        plt.legend()
    plt.grid()
    plt.ylabel("n' / n")
    plt.xlabel("n")
    plt.title(f"MinCount for different k values")
    plt.show()

    for k, arg in results.items():
        plt.figure(figsize=(8,8))
        plt.plot(arg[0], arg[1])
        plt.grid()
        plt.ylabel("n' / n")
        plt.xlabel("n")
        plt.title(f"MinCount for k = {k}")
        plt.savefig(f'{k}.png')
    

def plot_8(max_set_len=10000, step=1, data_gen=get_test_multiset):
    possible_b = [6, 12, 16]

    results = {}
    for b in possible_b:
        results[b] = ([], [])
    
    for n in range(1, max_set_len, step):
        M = data_gen(n)
        for b in possible_b:
            est = HyperLogLog.hyper_log_log(M, h=hyper_hash1, b=b)
            results[b][0].append(n)
            results[b][1].append(est/n)
        if n % 1000 == 1:
            print(n)
    
    plt.figure(figsize=(8,8))
    for b, arg in results.items():
        m = 1 << b
        plt.plot(arg[0], arg[1], label=f'm = {m}')
        plt.legend()
    plt.grid()
    plt.ylabel("n' / n")
    plt.xlabel("n")
    plt.title(f"HyperLogLog for different m values")
    plt.show()

    for b, arg in results.items():
        m = 1 << b
        plt.figure(figsize=(8,8))
        plt.plot(arg[0], arg[1])
        plt.grid()
        plt.ylabel("n' / n")
        plt.xlabel("n")
        plt.title(f"HyperLogLog for m = {m}")
        plt.savefig(f'{m}.png')
