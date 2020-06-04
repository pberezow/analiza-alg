import math
import random


"""
Hash functions for MinCount - return value from range [0, 1)
"""
def rand_hash(x):
    return random.Random(x).random()

def mul_hash(x, q=64):
    # A = 191128877173556587, w = 2**32
    w = 1 << q
    return (1000000000000000009/w * hash(x)) % 1

def mod_hash(x, q=64):  # zla funkcja
    w = 1 << q
    return (hash(x) % w) / w

def fib_hash(x, q=64):
    w = 1 << q
    A = math.floor(w/1.6180339)
    return (A/w * hash(x)) % 1

def hash1(x, q=32):
    w = (1 << q)
    x = ((x >> 16) ^ x) * 0x45d9f3b % w
    x = ((x >> 16) ^ x) * 0x45d9f3b % w
    x = (x >> 16) ^ x
    return x / w % 1

def hash2(x, q=32):
    x ^= (hash(x) << 13)
    x ^= (x >> 17)    
    x ^= (x << 5) 
    return x / (1 << q) % 1

def shift_hash(x, q=32):
    return x >> (32-10)

"""
Hash functions for HyperLogLog - return value from range [0, 2**b)
"""
def hyper_rand_hash(x, q=32):
    return random.Random(x).randint(0, 2**q)

def hyper_mul_hash(x, q=32):
    w = 1 << q
    return math.floor(1000000000000000009/w) * hash(x) % w

def hyper_mod_hash(x, q=32):
    w = 1 << q
    return hash(x) % w

def hyper_fib_hash(x, q=32):
    w = 1 << q
    A = math.floor(w/1.6180339)
    return (hash(x) * A) % w

def hyper_hash1(x, q=32):
    w = 1 << q
    x = hash(x)
    x = ((x >> 16) ^ x) * 0x45d9f3b % w
    x = ((x >> 16) ^ x) * 0x45d9f3b % w
    x = (x >> 16) ^ x % w
    return x

def hyper_hash2(x, q=32):
    x ^= (hash(x) << 13)
    x ^= (x >> 17)    
    x ^= (x << 5) 
    return x % (1 << q)
