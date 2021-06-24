#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from math import sqrt
import random


def ext_euclid(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    if b == 0:
        return 1, 0, a
    else:
        while (r != 0):
            q = old_r // r
            old_r, r = r, old_r - q * r
            old_s, s = s, old_s - q * s
            old_t, t = t, old_t - q * t
    return old_s, old_t, old_r


def inv(a, p):  # 欧几里得算法求逆元,求a模p的逆 a逆
    _a, _, _ = ext_euclid(a, p)
    return ((_a % p) + p) % p


class EIGamal_Signiture():
    def __init__(self):
        self.N = None
        self.p = None
        self.g = None
        self.x = None
        self.y = None

    def check_p_len(self, p, N):  # check whether p is N-bit.
        if len(bytes.fromhex(p))*8 != int(N):
            raise 'The bit lengh of p is not correct.'
        return

    def isPrime(self, n):
        if n > 1:
            if n == 2:
                return True
            if n % 2 == 0:
                raise 'p is not a prime number.'
            for x in range(3, int(sqrt(n) + 1), 2):
                if n % x == 0:
                    raise 'p is not a prime number.'
            return True
        raise 'p is not a prime number.'

    def generate_keys(self):
        x = random.randint(1, self.p-2)
        y = (self.g**x) % self.p
        self.x, self.y = x, y
        return y

    def Parameter_generation(self):
        N = input('Please enter the key\'s bit length N:')
        p = input(
            'Please enter the hexadecimal string of N bits (excluding the preceding 0x):')
        self.isPrime(int(p, 16))
        self.check_p_len(p, N)
        self.N = N
        self.p = int(p, 16)
        while True:
            g = random.randint(2, self.p-1)
            if (self.p-1) % g != 1:
                break
        self.g = g
        return int(p, 16), g

    def signing(self, m):
        while True:
            while True:
                k = random.randint(2, self.p-2)
                if (self.p-1) % k != 0:
                    break
            k_1 = inv(k, self.p-1)
            r = self.g**k % self.p
            s = ((hash(m)-(self.x)*r)*k_1) % (self.p-1)
            if s != 0:
                break
        return r, s

    def verifing(self, r, s, m):
        if 0 < r < self.p and 0 < s < self.p - 1:
            v1 = pow(self.g, hash(m), self.p)
            v2 = pow(self.y, r)*pow(r, s) % self.p
            if v1 == v2:
                return True
            else:
                return False
        else:
            return False


if __name__ == '__main__':
    message = 'the file'  # 若hash(message)为负数便不能成功,orz
    EIG = EIGamal_Signiture()
    p, g = EIG.Parameter_generation()
    y = EIG.generate_keys()
    print('p=%d g=%d y=%d' % (p, g, y))
    r, s = EIG.signing(message)
    print('r=%d s=%d' % (r, s))
    if EIG.verifing(r, s, message):
        print('Authentication successful')
    else:
        print('Authentication failed')
