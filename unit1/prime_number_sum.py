# Python 3 script to generate the first 1000 primes that can be written
# as a sum of two primes (each <= 1,000,000), in the form "2+p=c".

MAX_N = 1_000_000

def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    import math
    for i in range(2, int(math.isqrt(n)) + 1):
        if is_prime[i]:
            step = i
            start = i * i
            is_prime[start:n+1:step] = [False] * (((n - start) // step) + 1)
    primes = [i for i, v in enumerate(is_prime) if v]
    return is_prime, primes

def first_twin_upper(limit=1000, max_n=MAX_N):
    is_prime, primes = sieve(max_n)
    results = []
    for c in primes:
        if c < 5:
            continue
        p = c - 2
        if p <= max_n and is_prime[p]:
            results.append((2, p, c))
            if len(results) >= limit:
                break
    return results

def main():
    res = first_twin_upper(1000, MAX_N)
    chunk = []
    for i, (a, b, c) in enumerate(res, start=1):
        chunk.append(f"{a}+{b}={c}")
        if i % 100 == 0:
            print(", ".join(chunk))
            chunk = []
    if chunk:
        print(", ".join(chunk))

if __name__ == "__main__":
    main()