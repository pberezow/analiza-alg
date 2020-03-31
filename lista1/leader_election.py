from enum import Enum
from math import log2, ceil
from random import random
from matplotlib import pyplot as plt


class Status(Enum):
    NULL = 0
    SINGLE = 1
    COLLISION = 2


class Scenario(Enum):
    SECOND = 1
    THIRD = 2


def n_nodes_prob_generator(n_nodes):
    """
    Probability generator for 2nd scenatio.
    """
    while True:
        yield 1/n_nodes

def upper_bound_generator(upper_bound):
    """
    Probability generator for 3rd scenatio.
    """
    r = ceil(log2(upper_bound))

    while True:
        for i in range(1, r+1):
            yield 1/2 ** i

def leader_election(n_nodes=2, upper_bound=None, scenario=Scenario.SECOND):
    """
    Simulator for exercise 1
    """
    status = Status.NULL
    slot = 0

    # Pick proper generator
    prob_generator = None
    if scenario == Scenario.SECOND:
        prob_generator = n_nodes_prob_generator(n_nodes)
    else:
        if not upper_bound or upper_bound < n_nodes:
            upper_bound = n_nodes
        prob_generator = upper_bound_generator(upper_bound)

    # Elect leader
    while status != Status.SINGLE:
        status = Status.NULL
        slot += 1
        prob = next(prob_generator)
        for i in range(0, n_nodes):
            if random() <= prob:
                if status == Status.NULL:
                    status = Status.SINGLE
                else:
                    status = Status.COLLISION
                    break
    
    return slot

def leader_election_n_times(n_nodes=2, upper_bound=None, scenario=Scenario.SECOND, n_times=1000):
    """
    Repeat experiment n_times and return results
    """
    results = {}
    for i in range(0, n_times):
        result = leader_election(n_nodes, upper_bound, scenario)
        m = results.get(result, 0)
        m += 1
        results[result] = m
    
    res_list = []
    for k, v in results.items():
        res_list.append((k, v))
    res_list.sort()

    return res_list

def plot_hist(result_list):
    fig = plt.figure(figsize=(8,8))
    max_val = max([k for k,v in result_list])
    bins = [i for i in range(1, max_val+2)]
    plt.hist([k for k,v in result_list], bins=bins, weights=[v for k,v in result_list], histtype='bar', rwidth=0.5, align='left')
    plt.grid()
    plt.xlabel('Numer rundy')
    plt.ylabel('Ilość sukcesów')
    plt.show()

def calc_expected_value(result_list):
    n_times = sum([v for k,v in result_list])
    expected_val = sum([k * v/n_times for k,v in result_list])
    return expected_val

def calc_variance(result_list):
    n_times = sum(v for k,v in result_list)
    avg = sum([k*v for k,v in result_list]) / n_times

    var = sum([(k-avg)**2 for k,v in result_list for i in range(0,v)]) / n_times
    return var
