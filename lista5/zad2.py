import random

class Graph:
    
    def __init__(self, edges):
        self.vertices = [i for i in range(len(edges))]
        self.edges = edges
        self.r = [random.randint(0, 1) for i in self.vertices]
        # print(self.r)

    def _max_independent_set(self):
        changed = True
        vertices_copy = [*self.vertices]

        while changed:
            random.shuffle(vertices_copy)
            changed = False
        
            for v in vertices_copy:
                sum_neg_prefs = sum([self.r[q] for q in self.edges[v]] or [0])
                prev_r = self.r[v]
        
                if sum_neg_prefs > 0:
                    self.r[v] = 0
                else:
                    self.r[v] = 1
                if self.r[v] != prev_r:
                    changed = True
        
            # print(self.r)

    def get_max_independent_set(self):
        self._max_independent_set()
        max_ind_set = [z[0] for z in filter(lambda z: z[1] == 1, zip(self.vertices, self.r))]
        return max_ind_set

def create_graph(num_vertices):
    edges = [[] for i in range(num_vertices)]
    for i in range(num_vertices):
        edges[i] = [j for j in range(num_vertices) if j != i]
    return edges

if __name__ == '__main__':
    # edges = create_graph(100)
    # edges = [
    #     [2, 4],  # 0
    #     [2, 4],  # 1
    #     [0, 1, 3],  # 2
    #     [2],  # 3
    #     [0, 1]  # 4
    # ]
    edges = [
        [3, 4],
        [3, 5],
        [3, 4, 5],
        [0, 1, 2],
        [0, 2],
        [1, 2]
    ]

    g = Graph(edges)
    mis = g.get_max_independent_set()
    print(f'Max Independent set: {mis}')
