import numpy as np
import matplotlib.pyplot as plt


SIZE = 16


def primfacs(p):
    i = 2
    primfac = []
    while i * i <= p:
        while p % i == 0:
            primfac.append(i)
            p = p / i
        i = i + 1
    if p > 1:
        primfac.append(round(p))
    return primfac


data = [[0, 0, 0], [1, 1, 1]]
for n in range(2, SIZE):
    factor = primfacs(n)
    if len(factor) in [1, 2, 3]:
        tail = [1] * (3 - len(factor))
        data.append(tail + factor)

for x, y, z in data:
    print(f"[{x}, {y}, {z}]")
print(f"SIZE={SIZE}, len(data)={len(data)}")

data = np.asarray(data)
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(projection='3d')
ax.plot(data[:, 0], data[:, 1], data[:, 2])
plt.show()
