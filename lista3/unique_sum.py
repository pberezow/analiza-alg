import math
import random
import time

def _reverse(val):
    val_bit_len = val.bit_length()
    reversed_val = 0
    while val.bit_length() > 0:
        reversed_val <<= 1
        if val % 2 == 1:
            reversed_val += 1
        val >>= 1
    return (reversed_val, val_bit_len)

def _concat(i, k):
    rev_k, k_bit_len = _reverse(k)
    for _ in range(0, k_bit_len):
        i <<= 1
        if rev_k % 2 == 1:
            i += 1
        rev_k >>= 1
    return i


class UniqueSum:

    def __init__(self, h, m):
        if not callable(h):
            raise Exception("'h' have to be a function.")
        if m < 1:
            raise Exception("'m' has to be a positive integer")
        self.M = [math.inf for i in range(0,m)]
        self.h = h

    def add(self, element):  # element is 2-tuple -> (id, lambda_id)
        for k, _ in enumerate(self.M):
            u = self.h(_concat(element[0], k+1))
            self.M[k] = min(self.M[k], -(math.log(u) / element[1]))

    def eval(self):
        return (len(self.M) - 1) / sum(self.M)

    @classmethod
    def unique_sum(cls, s, h, m):
        us = cls(h, m)
        for el in s:
            us.add(el)
        estimated_sum = us.eval()
        actual_sum = sum(el[1] for el in s)

        return estimated_sum, abs(estimated_sum - actual_sum) / abs(actual_sum)


def h_func(x, q=32):
    w = (1 << 32)
    x = ((x >> 16) ^ x) * 0x45d9f3b % w
    x = ((x >> 16) ^ x) * 0x45d9f3b % w
    x = (x >> 16) ^ x
    return x / w % 1


def make_set(a, b, size, first_id=1, seed=None):
    if a < b:
        a, b = b, a
    rng = random.Random(seed)
    s = [(first_id + i, rng.random() * (b-a) + a) for i in range(size)]
    return s

if __name__ == '__main__':
    a = 1
    b = 1000
    size = 10000
    h = h_func

    s = make_set(a, b, size)

    start = time.time()

    result, relative_err = UniqueSum.unique_sum(s, h, 50)

    elapsed = time.time() - start
    print(f'Elapsed: {elapsed} sec\n')
    print(f'Estimated sum: {result}    Relative error: {relative_err}\n')
