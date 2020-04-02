import math
import random
from hashlib import sha1


"""
Hash functions for MinCount - return value from range [0, 1)
"""
def hash_function(x):
    return random.Random(x).random()

def mul_hash(x, q=64):
    # A = 191128877173556587, w = 2**32
    w = 1 << q
    return (1000000000000000009/w * hash(x)) % 1

def modular_hash(x, q=64):  # zla funkcja
    w = 1 << q
    return (hash(x) % w) / w

def fibonacci_hash(x, q=64):
    w = 1 << q
    A = math.floor(w/1.6180339)
    return (A/w * hash(x)) % 1

"""
Hash functions for HyperLogLog - return value from range [0, 2**b)
"""
def hyper_hash_function(x, q=32):
    return random.Random(x).randint(0, 2**q)

def hyper_fib_hash(x, q=32):
    w = 1 << q
    A = math.floor(w/1.6180339)
    return (hash(x) * A) % w
