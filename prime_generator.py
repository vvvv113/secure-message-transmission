import random
from math import gcd

first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]


def get_low_level_prime(n):
    while True:
        pc = random.getrandbits(n)
        for divisor in first_primes_list:
            if pc % divisor == 0 and divisor ** 2 <= pc:
                break
        else:
            return pc


def is_miller_rabin_passed(mrc):
    max_divisions_by_two = 0
    ec = mrc - 1
    while ec % 2 == 0:
        ec >>= 1
        max_divisions_by_two += 1
    assert (2 ** max_divisions_by_two * ec == mrc - 1)

    def trial_composite(round_tester):
        if pow(round_tester, ec, mrc) == 1:
            return False
        for i in range(max_divisions_by_two):
            if pow(round_tester, 2 ** i * ec, mrc) == mrc - 1:
                return False
        return True

    number_of_rabin_trials = 20
    for i in range(number_of_rabin_trials):
        round_tester = random.randrange(2, mrc)
        if trial_composite(round_tester):
            return False
    return True


def prime_number():
    while True:
        n = 8
        prime_candidate = get_low_level_prime(n)
        if not is_miller_rabin_passed(prime_candidate):
            continue
        return prime_candidate


def prim_roots(modulo):
    prime = modulo
    for num_to_check in range(1, prime):
        candidate_prim_roots = set()
        for i in range(1, prime):
            modulus = (num_to_check ** i) % prime
            candidate_prim_roots.add(modulus)
            if len(candidate_prim_roots) == prime - 1:
                return num_to_check
