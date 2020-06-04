class Graph:
    
    def __init__(self, edges):
        self.vertices = [i for i in range(len(edges))]
        self.edges = edges
        self.pref = [None for i in self.vertices]
    
    def get_neighbors(self, v0):
        return self.edges.get(v0, [])

    def set_pref(self, v0, value):
        self.pref[v0] = value

    def get_pref(self, v0):
        return self.pref.get(v0, None)

    def married(self, p):
        q = self.get_pref(p)
        return q in self.get_neighbors(p) and p in self.get_neighbors(q)


    def maximal_matching(self):
