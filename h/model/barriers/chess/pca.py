import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, decomposition

np.random.seed(0)

X = [
    [x, y]
    for x in range(1, 9)
    for y in range(1, 9)
    if x != 0 and y != 0
]
print(X)
# fig = plt.figure(1, figsize=(4, 3))
# plt.clf()
# plt.cla()
pca = decomposition.PCA(
    n_components=1,
    svd_solver="arpack",
    # whiten=True,
    random_state=0,
)
pca.fit(X)
X = pca.transform(X)
X = [x[0] for x in X]
X = [x / max([abs(max(X)), abs(min(X))]) for x in X]
# X = sorted(X)

print(X)
plt.scatter(range(8 ** 2), X)
plt.show()