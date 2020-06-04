import time

def index_to_configuration(index, n):
    # C = (1,2,3,4,5) ==> 1 + 2*6 + 3*6^2 + 4*6^3 + 5*6^4
    conf = [0 for i in range(n)]
    for i in reversed([j for j in range(n)]):
        val = index // (n+1)**i
        conf[i] = val
        index -= val * (n+1)**i
    
    return conf

def configuration_to_index(conf):
    index = 0
    n = len(conf)
    for i in range(n):
        index += conf[i] * (n+1)**i
    return index

def get_configurations(n):
    return [0 for i in range((n+1)**n)]

def get_possible_transitions(conf):
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

    

# def get_reversed_transitions(conf):
#     transitions = []

#     if (conf[0] - 1) % (len(conf) + 1) == conf[-1]:
#         pre_conf = [*conf]
#         pre_conf[0] = (pre_conf[0] - 1) % (len(conf) + 1)
#         transitions.append(pre_conf)

#     for i in range(1, len(conf)):
#         if conf[i] == conf[i-1]:
#             for j in range(len(conf)+1):
#                 if j == conf[i]:
#                     continue
#                 pre_conf = [*conf]
#                 pre_conf[i] = j
#                 transitions.append(pre_conf)
    
#     return transitions

# def traverse_back(actual_conf, configurations, edges):
#     idx = configuration_to_index(actual_conf)
#     if configurations[idx]:
#         return
#     configurations[idx] = 1

#     transitions = get_reversed_transitions(actual_conf)
#     for conf in transitions:
#         i = configuration_to_index(conf)
#         edges.append((i, idx))
#         if configurations[i]:
#             continue
#         traverse(conf, configurations, edges)

# def rev_simulation(n):
#     configurations = get_configurations(n)
#     edges = []
#     safe_confs = [[i for j in range(n)] for i in range(n+1)]

#     for sc in safe_confs:
#         traverse(sc, configurations, edges)

#     safe_confs_indices = [configuration_to_index(c) for c in safe_confs]
#     # t0 = time.time()
#     # paths = []
#     # for sc in safe_confs_indices:
#     #     path_len = get_longest_path(edges, safe_confs_indices, sc, True)
#     #     paths.append(path_len)
#     # print(f'Time (list of edges): {time.time() - t0} s')

#     # t0 = time.time()
#     edges_matrix = _to_list_of_edges(edges, len(configurations))
#     paths = []
#     for sc in safe_confs_indices:
#         path_len = get_longest_path2(edges_matrix, safe_confs_indices, sc, True)
#         paths.append(path_len)
#     # print(f'Time (matrix-like): {time.time() - t0} s')


    # print(f'[<<<] Sum: {sum(configurations)},   Len: {len(configurations)},   Edges: {len(edges)},   MaxLen: {max(paths)}')

def _convert_edges(edges_list, num_of_vertices):
    edges = [[] for i in range(num_of_vertices)]
    for i in range(num_of_vertices):
        edges[i] = [e[0] for e in filter(lambda e: e[1] == i, edges_list)]

    return edges


def get_longest_path(edges, safe_indices, curr_idx, is_root=False):
    """
    Edges as list of list with edges for e[1]
    """
    if curr_idx in safe_indices and not is_root:
        return 0

    # filtered_edges = filter(lambda e: e[1] == curr_idx, edges)
    paths = []
    for e in edges[curr_idx]:
        path_len = get_longest_path(edges, safe_indices, e[0])
        paths.append(path_len)
    path_len = 1 + max(paths or [0])
    
    return path_len

def simulation(n):
    configurations = get_configurations(n)
    edges = []

    for i in range(len(configurations)):
        if configurations[i] == 1:
            continue

        conf = index_to_configuration(i, n)
        configurations[i] = 1  # visited

        possible_transitions = get_possible_transitions(conf)
        indices = [configuration_to_index(c) for c in possible_transitions]

        for idx in indices:
            edges.append((i, idx))
    
    print(f'[>>>] Sum: {sum(configurations)},   Len: {len(configurations)},   Edges: {len(edges)}')


if __name__ == '__main__':
    n = 5
    # t0 = time.time()
    # simulation(n)
    # print(f'Time: {time.time() - t0} s')
    t0 = time.time()
    rev_simulation(n)
    print(f'Time: {time.time() - t0} s')
