import time

def index_to_configuration(index, n):
    """
    Map index to configuration
    """
    # C = (1,2,3,4,5) ==> 1 + 2*6 + 3*6^2 + 4*6^3 + 5*6^4
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

def traverse(actual_conf, configurations, edges):
    """
    Traverse from given configuration recursively to safe configuration 
        or previously visited configuration
    Set configuration's value to True in bool list for each visited configuration
    Push new edge for each possible transition
    """
    idx = configuration_to_index(actual_conf)
    if configurations[idx]:
        return

    transitions = get_possible_transitions(actual_conf)
    for conf in transitions:
        i = configuration_to_index(conf)
        edges.append((idx, i))
        if configurations[i]:
            continue
        traverse(conf, configurations, edges)

    configurations[idx] = True

def _convert_edges(edges_list, num_of_vertices):
    """
    Transforms list of edges to prevent filtering edges in each step 
    of 'get_longest_path' func
    """
    edges = [[] for i in range(num_of_vertices)]
    for v0, v1 in edges_list:
        edges[v1].append(v0)
    # for i in range(num_of_vertices):
    #     edges[i] = [e[0] for e in filter(lambda e: e[1] == i, edges_list)]

    return edges


def get_longest_path(edges, safe_indices, v1, is_root=False):
    """
    Edges has to be transformed by '_convert_edges' function
    """
    if v1 in safe_indices and not is_root:
        return 0

    longest_path = 0
    for v0 in edges[v1]:
        path_len = get_longest_path(edges, safe_indices, v0)
        longest_path = path_len if path_len > longest_path else longest_path

    return 1 + longest_path

def simulation(n, with_longest_path=True):
    configurations = get_configurations(n)
    edges = []

    for i in range(len(configurations)):
        if configurations[i]:
            continue

        conf = index_to_configuration(i, n)
        traverse(conf, configurations, edges)
    
    longest_path = None
    if with_longest_path:
        converted_edges = _convert_edges(edges, len(configurations))

        safe_indices = [configuration_to_index(c) for c in [[i for j in range(n)] for i in range(n+1)]]
        longest_path = max([get_longest_path(converted_edges, safe_indices, v1, True) for v1 in safe_indices])

    print(f'Sum: {sum(configurations)},   Len: {len(configurations)},   Edges: {len(edges)},   PathLen: {longest_path}')


if __name__ == '__main__':
    n = 5
    t0 = time.time()
    simulation(n)
    print(f'Time: {time.time() - t0} s')
