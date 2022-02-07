import random
import time as t

import matplotlib.pyplot as plt
import numpy as np


def power(a, n):
    return (1 if n == 0
            else power(a * a, n // 2) if n % 2 == 0
    else a * power(a, n - 1))


list_argumenst_n = np.array([10099, 11099, 12099, 13099, 14099, 15099, 16099, 17099, 18099, 19099, 20099])

coord_x = []
coord_y = []
for i in range(len(list_argumenst_n)):
    a = 999999999999999999999
    n = list_argumenst_n[i]
    coord_x.append(n)
    start_time = t.time()
    print(power(a, n))
    res = t.time() - start_time
    coord_y.append(res)
print(coord_y)

plt.plot(list_argumenst_n, coord_y, 'r--o')
plt.grid()
plt.show()
coord_x.clear()
coord_y.clear()


def factorize(n):
    Ans = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            Ans.append(d)
            n //= d
        else:
            d += 1
    if n > 1:
        Ans.append(n)
    return Ans


rand = random.randint(0, 99999999999)
n = rand
for i in range(10):
    n = int(str(n)+str(random.randint(0, 9)))
    coord_x.append(len(str(n)))
    start = t.time()
    print(f'n = {n}, factorize = {factorize(n)} len = {len(str(n))}')
    end = t.time() - start
    coord_y.append(end)

plt.plot(coord_x, coord_y, 'r--o')
plt.grid()
plt.show()
