import random
import math
from matplotlib import pyplot as plt
from functools import reduce


class MultiSet:

    def __init__(self, S, m):
        # assert type(S) == list
        # assert type(m) == type(print)
        self.S = S
        self.m = m


def hash_function(x):
    return random.Random(x).random()

def min_count(multi_set, h, k):
    M = [1 for i in range(0,k)]
    
    for x in multi_set.S:
        if h(x) < M[-1] and h(x) not in M:
            M[-1] = h(x)
            M.sort()
    
    if M[-1] == 1:
        return len(list(filter(lambda x: x != 1, M)))
    else:
        return (k-1)/M[-1]




def get_test_multiset(unique_elements, n_times_repeat):
    return MultiSet([i for i in range(unique_elements) for j in range(n_times_repeat)], lambda x: x)

# ========================== 1. =======================
def plot1b():
    possible_k = [2, 3, 10, 100, 400]
    results = []
    for k in possible_k:
        result_k = []
        for n in range(1, 10**4, 5):
            ms = get_test_multiset(n, 1)
            count = min_count(ms, hash_function, k)
            result_k.append( (n, count/n) )
            if n % 1000 == 1:
                print(k, n)
        results.append(result_k)

    data = list(zip(possible_k, results))
    # print(data)

    def plot(k, arg):
        plt.figure(figsize=(8,8))
        plt.plot([i[0] for i in arg], [i[1] for i in arg])
        plt.grid()
        plt.ylabel("n' / n")
        plt.xlabel("n")
        plt.title(f"k = {k}")
        plt.show()

    for k, arg in data:
        plot(k, arg)
    
    

if __name__ == '__main__':
    plot1b()
    # uni = 10000
    # repeat = 10
    # k = 1000
    # multiset = get_test_multiset(uni, repeat)
    # count = min_count(multiset, hash_function, k)
    # print(f'Unique elements: {uni}')
    # print(f'Every element repeated {repeat} times.')
    # print(f'k = {k}')
    # print(f'MinCount result: {math.floor(count)}')


"""
1a. Nie ma wpływu, bo wykluczamy to przez funkcję hash
1b. 
"""