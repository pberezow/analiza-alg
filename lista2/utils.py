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

def chernoff_delta(alpha, k):
    # x = 1 - (k-1) / (k*alpha)
    # delta = x * math.e**(-x+1)
    pass

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


# ====== Zad 5 ======
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

def plot_5c(max_set_len=10000, start=50, stop=300, step=10, data_gen=lambda x : get_random_multiset(x, seed=10)):
    results = []
    multiset = data_gen(max_set_len)

    for k in range(start, stop, step):
        success = 0
        all = 0
        for i in range(1, len(multiset)):
            est = MinCount.min_count(multiset[0:i], k=k)
            if abs(est/i - 1) < 0.1:
                success += 1
            all += 1

        results.append( (k, success/all) )
    
    for k, v in results:
        print(k, '  ->  ', v*100, '%')
    
    plt.figure()
    plt.plot([k for k, v in results], [v for k, v in results])
    plt.grid()
    plt.xlabel('k')
    plt.ylabel("|n'/n - 1|")
    plt.show()


def zad_6():
    results_shift = ([], [])
    results_hash = ([], [])
    for n in range(1, 10000):
        ms = get_random_multiset(n, seed=10)
        count1 = MinCount.min_count(ms, h=shift_hash, k=400)
        results_shift[0].append(n)
        results_shift[1].append(count1/n)
        count2 = MinCount.min_count(ms, h=hash1, k=400)
        results_hash[0].append(n)
        results_hash[1].append(count2/n)

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

# ====== Zad 7 ======
def plot_7a():
    k = 400
    alphas = [0.005, 0.01, 0.05]
    
    results = {}
    for a in alphas:
        results[a] = ([], [])
    
    ms = get_random_multiset(10000)
    for n in range(1, 10000):
        est = MinCount.min_count(ms[0:n], k=400)
        for a in alphas:
            results[a][0].append(n)
            results[a][1].append(est/n)
    
    for a, res in results.items():
        delta1 = chebyshev_delta(a, k)
        # delta2 = chernoff_delta(a, k)
        # print(delta1, '    ', delta2)
        plt.figure()
        print(a)
        plt.scatter(res[0], res[1])
        plt.plot(res[0], [1+delta1 for i in range(len(res[0]))], 'r-')
        plt.plot(res[0], [1-delta1 for i in range(len(res[0]))], 'r-')
        # plt.plot(res[0], [1+delta2 for i in range(len(res[0]))], marker=1)
        # plt.plot(res[0], [1-delta2 for i in range(len(res[0]))], marker=1)
        plt.grid()
        plt.xlabel('n')
        plt.ylabel("n' / n")
        plt.title('MinCount')
        plt.show()


# ====== Zad 8 ======
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

# ====== Zad 8 ======
def plot_8_comp(max_set_len=10000, step=1, data_gen=lambda x : get_random_multiset(x, 10)):
    possible_b = [4, 6, 11, 16]
    results_mc = {}
    results_hll = {}
    for b in possible_b:
        mem = HyperLogLog(b=b).memory()
        mc = MinCount(mem=mem).k
        results_mc[b] = [[], [], mc]
        results_hll[b] = ([], [])

    for n in range(1, max_set_len, step):
        ms = data_gen(n)
        for b in possible_b:
            est = HyperLogLog.hyper_log_log(ms, hyper_hash1, b=b)
            est2 = MinCount.min_count(ms, hash1, mem=results_mc[b][2])
            results_hll[b][0].append(n)
            results_hll[b][1].append(abs(est/n-1)+1)
            results_mc[b][0].append(n)
            results_mc[b][1].append(abs(est2/n-1)+1)
    
    for b in possible_b:
        plt.figure()
        plt.plot(results_hll[b][0], results_hll[b][1], label=f'HyperLogLog, m={1 << b}')
        plt.legend()
        plt.plot(results_mc[b][0], results_mc[b][1], label=f'MinCount, k={results_mc[b][2]}')
        plt.legend()
        plt.grid()
        plt.xlabel('n')
        plt.ylabel("n' / n")
        plt.title('MinCount and HyperLogLog comparison')
        plt.show()
    