import random
import math
from hash_functions import hash1


class MinCount:
    def __init__(self, h=hash1, k=100, mem=None):
        if not callable(h):
            raise Exception('Parameter h need to be a function.')
        self.h = h
        if mem:  # memory limit first
            self.k = mem // 32
        else:
            self.k = k
        self.M = [1 for i in range(k)]

    def add(self, x):
        hash_x = self.h(x)
        if hash_x < self.M[-1] and hash_x not in self.M:
            self.M[-1] = hash_x
            self.M.sort()

    def __len__(self):
        return round(self._estimate())

    def memory(self):
        return 32 * self.k

    def _estimate(self):
        if self.M[-1] == 1:
            return len(list(filter(lambda x: x != 1, self.M)))
        else:
            return (self.k-1)/self.M[-1]

    @classmethod
    def min_count(cls, multi_set, h=hash1, k=100):
        mc = cls(h=h, k=k)
        for x in multi_set:
            mc.add(x)
        return len(mc)
