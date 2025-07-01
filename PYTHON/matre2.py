#Explanation: This is a python program that finds the prime factors of a given number using trial division and Pollard's Rho Algorithm.

import math
import random
def is_prime(n):
    """Check if a number is prime using trial division."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def trial_division(n):
    """Find small prime factors using trial division."""
    factors = []
    
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    while n % 3 == 0:
        factors.append(3)
        n //= 3

    i = 5
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        while n % (i + 2) == 0:
            factors.append(i + 2)
            n //= (i + 2)
        i += 6

    if n > 1:  # If there's a remaining prime factor
        factors.append(n)

    return factors

def pollard_rho(n):
    """Pollard's Rho Algorithm for prime factorization (faster for large numbers)."""
    if n % 2 == 0:
        return 2
    x = random.randint(1, n-1)
    y = x
    c = random.randint(1, n-1)
    d = 1

    def f(x):
        return (x * x + c) % n

    while d == 1:
        x = f(x)
        y = f(f(y))
        d = math.gcd(abs(x - y), n)
        if d == n:
            return None  # Failure

    return d

def prime_factors(n):
    """Find all prime factors using trial division and Pollard's Rho."""
    if n < 2:
        return []
    if is_prime(n):  # If already prime, return itself
        return [n]

    factors = trial_division(n)  # First try trial division for small primes

    remaining = n
    for f in factors:
        remaining //= f

    while remaining > 1 and not is_prime(remaining):
        factor = pollard_rho(remaining)
        if factor is None:
            break  # If Pollard's Rho fails, stop
        while remaining % factor == 0:
            factors.append(factor)
            remaining //= factor

    if remaining > 1:
        factors.append(remaining)  # If there's a prime left, add it

    return sorted(factors)

# Example usage:
while True:
    try:
        N = int(input("Enter an integer to find its prime factors: "))
        if N <= 1:
            print("Please enter a number greater than 1.")
            continue
        factors = prime_factors(N)
        print(f"Prime factors of {N}: {factors}")
    except ValueError:
        print("Invalid input. Please enter an integer.")
