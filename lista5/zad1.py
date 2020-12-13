import time

def index_to_configuration(index, n):
    """
    Map index to configuration
    """
    # C = (1,2,3,4,5)  ==>  idx = 1 + 2*6 + 3*6^2 + 4*6^3 + 5*6^4
    conf = [0 for i in range(n)]
    for i in reversed([j for j in range(n)]):
        val = index // (n+1)**i
        conf[i] = val
        index -= val * (n+1)**i
    
    return conf

def configuration_to_index(conf):
    """
    Map configuration to index
    """
    index = 0
    n = len(conf)
    for i in range(n):
        index += conf[i] * (n+1)**i
    return index

def get_configurations(n):
    """
    Return list with bool values for all configurations for given 'n'
    Set safe configurations to True
    """
    configurations = [False for i in range((n+1)**n)]
    for safe_idx in [configuration_to_index(c) for c in [[i for j in range(n)] for i in range(n+1)]]:
        configurations[safe_idx] = True
    return configurations

def get_possible_transitions(conf):
    """
    Return list of all possible transitions from configuration 'conf'
     - Configurations as lists
    """
    transitions = []
    
    if conf[0] == conf[-1]:
        new_conf = [*conf]
        new_conf[0] = (new_conf[0] + 1) % (len(conf) + 1)
        transitions.append(new_conf)
    
    for i in range(1, len(conf)):
        if conf[i] != conf[i-1]:
            new_conf = [*conf]
            new_conf[i] = new_conf[i-1]
            transitions.append(new_conf)
    
    return transitions

def dfs(actual_idx, configurations, order, n):
    """
    Calculate dfs nodes order, and verify algorithm - verified if all 
        configurations are True
    """
    if configurations[actual_idx]:
        return
    
    conf = index_to_configuration(actual_idx, n)
    transitions = get_possible_transitions(conf)

    for c in transitions:
        i = configuration_to_index(c)
        if configurations[i]:
            continue
        dfs(i, configurations, order, n)

    order.append(actual_idx)
    configurations[actual_idx] = True

def simulation(n):
    order = []
    configurations = get_configurations(n)
    
    # calculate dfs order
    for idx in range(len(configurations)):
        dfs(idx, configurations, order, n)
    
    # max path len for each configuration -> if safe configuration then path len is set to -1
    path_len = [0 if i == True else -1 for i in get_configurations(n)]
    
    # calculate longest paths for each node
    for idx in order:
        conf = index_to_configuration(idx, n)
        transitions = get_possible_transitions(conf)

        path_len[idx] = 1
        for c in transitions:
            i = configuration_to_index(c)
            if path_len[i] >= path_len[idx]:
                path_len[idx] = path_len[i] + 1

    print(f'n = {n} \n  Valid configurations: {sum(configurations)}\n  All configurations: {len(configurations)}\n  Longest path: {max(path_len)}')


if __name__ == '__main__':
    n = 8
    t0 = time.time()
    simulation(n)
    print(f'Time: {time.time() - t0} s')