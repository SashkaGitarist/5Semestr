import math

MAX = 10**5


def sieve_for_primes_to(n):
    size = n//2
    sieve = [1]*size
    limit = int(n**0.5)
    for i in range(1,limit):
        if sieve[i]:
            val = 2*i+1
            tmp = ((size-1) - i)//val
            sieve[i+val::val] = [0]*tmp
    return [2] + [i*2+1 for i, v in enumerate(sieve) if v and i>0]


PRIMES = sieve_for_primes_to(MAX)

Prime_arr = list()


def phi(n):
    original_n = n
    prime_factors = []
    prime_index = 0
    while n > 1: # As long as there are more factors to be found
        p = PRIMES[prime_index]
        if (n % p == 0): # is this prime a factor?
            prime_factors.append(p)
            Prime_arr.append(p)
            while math.ceil(n / p) == math.floor(n / p):
                n = n // p

        prime_index += 1

    for v in prime_factors:
        original_n *= 1 - (1/v)

    return int(original_n)


tt = 3102001
print("Саня:", phi(tt))
print(Prime_arr)

res = (1 - (1/Prime_arr[0])) * (1 - (1/Prime_arr[1])) * (1 - (1/Prime_arr[2])) * tt
print(res)

Prime_arr.clear()

tt = 11112001
print("\n Волера: ", phi(tt))
print(Prime_arr)
res = (1 - (1/Prime_arr[0])) * (1 - (1/Prime_arr[1])) * (1 - (1/Prime_arr[2])) * tt
print(res)

