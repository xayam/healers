import numpy as np
import matplotlib.pyplot as plt
SIZE = 16
def primfacs(n):
   i = 2
   primfac = []
   while i * i <= n:
       while n % i == 0:
           primfac.append(i)
           n = n / i
       i = i + 1
   if n > 1:
       primfac.append(round(n))
   return primfac
data = [[0, 0, 0], [1, 1, 1]]
for n in range(2, SIZE):
    factor = primfacs(n)
    if len(factor) in [1, 2, 3]:
        tail = [1] * (3 - len(factor))
        data.append(tail + factor)
data = np.asarray(data)
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(projection='3d')
ax.plot(data[:, 0], data[:, 1], data[:, 2])
plt.show()
