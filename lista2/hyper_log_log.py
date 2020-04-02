import math
from hash_functions import hyper_hash1
import multiprocessing


def get_alpha_m(b):
    if b < 4 or b > 16:
        raise Exception('Wrong b value - should be in range [4, ..., 16]')
    
    if b == 4:
        return 0.673
    elif b == 5:
        return 0.697
    elif b == 6:
        return 0.709
    else:
        return 0.7213 / (1 + 1.079 / ( 1 << b)) 

class HyperLogLog:

    def __init__(self, h=hyper_hash1, b=16):
        self.alpha_m = get_alpha_m(b)
        self.b = b
        self.m = 1 << b
        self.h = h
        self.M = [0 for i in range(self.m)]
    
    def _get_j(self, x):
        return x >> (32-self.b)
        # return x & (self.m-1)

    def _get_w(self, x):
        return x - ((x >> (32-self.b)) << (32-self.b))
        # return x >> self.b

    def _rho(self, x):
        rho = 32 - self.b - x.bit_length() + 1
        if rho <= 0:
            raise Exception('Wrong value of x in rho function.')
        return rho

    def add(self, x):
        hash_x = self.h(x)
        j = self._get_j(hash_x)
        w = self._get_w(hash_x)
        self.M[j] = max(self.M[j], self._rho(w))

    def __eq__(self, other):
        return self.b == other.b

    def __ne__(self, other):
        return self.b != other.b

    def __add__(self, other):
        if self != other:
            raise Exception('Exception in __add__')
        new = HyperLogLog(self.h, self.b)
        for i, _ in enumerate(new.M):
            new.M[i] = self.M[i] if self.M[i] > other.M[i] else other.M[i]
        return new

    def __iadd__(self, other):
        if self != other:
            raise Exception('Exception in __add__')
        for i, val in enumerate(self.M):
            self.M[i] = other.M[i] if other.M[i] > val else val
        return self

    def __len__(self):
        return round(self._estimate())

    def _estimate(self):
        E = self.alpha_m * self.m * self.m / sum( math.pow(2, -x) for x in self.M )
    
        if E <= 2.5 * self.m:
            # small range correction
            V = len( list(filter(lambda x : x == 0, self.M)) )
            if V != 0:
                E = self.m * math.log(self.m / V)
            else:
                pass
        elif E <= 1/30 * (1 << 32):
            # intermediate range—no correction
            pass
        else:
            # large range correction
            E = -(1 << 32) * math.log(1 - E / (1 << 32))        
        return E

    @classmethod
    def hyper_log_log(cls, multi_set, h=hyper_hash1, b=16):
        if len(multi_set) > 10000:
            return cls._paralell_hyper_log_log(multi_set, h=h, b=b)
        else:
            return cls._hyper_log_log(multi_set, h=h, b=b)

    @classmethod
    def _hyper_log_log(cls, multi_set, h, b):
        hll = cls(h=h, b=b)
        for x in multi_set:
            hll.add(x)
        return len(hll)

    @classmethod
    def get_partial_hll(cls, values, h, b):
        hll = cls(h=h, b=b)
        for x in values:
            hll.add(x)
        return hll

    @classmethod
    def _paralell_hyper_log_log(cls, multiset, h, b, workers=None):
        if not workers:
            workers = multiprocessing.cpu_count()
        
        with multiprocessing.Pool(workers) as pool:
            data = []
            l = len(multiset) // workers
            for i in range(workers):
                data.append( (multiset[i*l : (i+1)*l], h, b) )

            results = pool.starmap(cls.get_partial_hll, data)
        
            sum_hll = results[0]
            for r in results[1:]:
                sum_hll += r
            return len(sum_hll)
