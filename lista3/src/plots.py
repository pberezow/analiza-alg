import matplotlib.pyplot as plt
import pandas as pd
import os
import math

def chebyshev_delta(alpha, m):
    delta = math.sqrt(1/(m-2)) / math.sqrt(alpha)
    return delta

def get_data_files(base_dir):
    files = []
    for file in os.listdir(base_dir):
        if file.endswith(".csv"):
            files.append(os.path.join(base_dir, file))
    return files


# read parameters in first line of input file
# file - path to csv file
# params_types - list of tuples describing each param, eg. [('name', str), ('n_value', int), ('prob', float), ...]
def _read_params(file, params_types, sep=','):
    # dict with param name as key and it's value written in file
    params_values = {}
    with open(file, 'r') as f:
        line = f.readline()
        values = line[:-1].split(sep)
        params_values = {param_type[0]: param_type[1](val) for param_type, val in zip(params_types, values)}
    return params_values

def draw_1(data_file):
    params_types = [('m', int), ('title', str)]
    params = _read_params(data_file, params_types)
    
    df = pd.read_csv(data_file, skiprows=[0], header=None, names=['n', 'estimated', 'actual'])

    plt.figure() #figsize=(8,8))
    plt.title(params['title'])
    plt.scatter(
        df['n'],
        df['estimated'] / df['actual'],
        linewidths=0.01
    )
    plt.grid()
    plt.xlabel('n')
    plt.ylabel('estimated/actual')
    plt.savefig(data_file.split('.csv')[0] + '.png')
    # plt.show()
    plt.close()

def draw_2(data_file, alpha):
    params_types = [('m', int), ('title', str)]
    params = _read_params(data_file, params_types)
    
    df = pd.read_csv(data_file, skiprows=[0], header=None, names=['n', 'estimated', 'actual'])
    delta = chebyshev_delta(alpha, params['m'])

    plt.figure() #figsize=(8,8))
    plt.title(params['title'])
    plt.scatter(
        df['n'],
        df['estimated'] / df['actual'],
        linewidths=0.01
    )
    plt.plot(df['n'], [1+delta for i in range(len(df['n']))], 'r-')
    plt.plot(df['n'], [1-delta for i in range(len(df['n']))], 'r-')
    plt.grid()
    plt.xlabel('n')
    plt.ylabel('estimated/actual')
    plt.savefig(data_file.split('.csv')[0] + f'_cheb_{alpha*100}.png')
    # plt.show()
    plt.close()


if __name__ == '__main__':
    alphas = [0.005, 0.01, 0.05]
    files = get_data_files('./unique_sum_data/')
    for file in files:
        # draw_1(file)
        draw_2(file, alphas[2])

    # files = get_data_files('./unique_avg_data/')
    # for file in files:
    #     draw_1(file)
        # draw_2(file, alphas[2])
