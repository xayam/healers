import random
import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import quad
from scipy.interpolate import CubicSpline

n = 3
size = 64
width = n * size
rand = random.SystemRandom(0)
data = [rand.choice([0, 1]) for _ in range(width)]

represent = []
curr = 0
for i in range(0, width, n):
    buffer = ""
    for j in range(n):
        buffer += str(data[i + j])
    buffer = int(buffer, 2) + 1
    if i % 2 == 1:
        buffer = - buffer
    curr += buffer
    represent.append(curr)
represent = [represent[0] - 1] + represent + [represent[-1] + 1]

# Табличные данные
X = np.array(list(range(size + 2)))
Y = np.array(represent)
print(len(X), len(Y))
# Строим сплайновую интерполяцию
cspline = CubicSpline(X, Y)

# Разложение в ряд Фурье
L = X[-1] - X[0]
N = width
k = np.arange(1, N + 1)


def integrate_cos(x, k):
    return np.cos(2 * np.pi * x * k / L) * cspline(x)


def integrate_sin(x, k):
    return np.sin(2 * np.pi * x * k / L) * cspline(x)


# a0 = (1 / L) * quad(cspline, 0, L)[0]
# ak = (2 / L) * np.array([quad(integrate_cos, 0, L, args=(ki,))[0] for ki in k])
# bk = (2 / L) * np.array([quad(integrate_sin, 0, L, args=(ki,))[0] for ki in k])


# Сумма ряда Фурье
# def fourier_series(x):
#     series = a0 + \
#              np.sum(
#                  ak.reshape(-1, 1) *
#                  np.cos(
#                      2 * np.pi * x * k.reshape(-1, 1) / L
#                  ) +
#                  bk.reshape(-1, 1) *
#                  np.sin(2 * np.pi * x * k.reshape(-1, 1) / L),
#                  axis=0
#              )
#     return series.flatten()


# Создаем данные для построения графика
x_values = np.linspace(X[0], X[-1], 1000)
y_interp = cspline(x_values)
# y_fourier = fourier_series(x_values)

# Построение графика
plt.plot(X, Y, 'r', label='Интерполированная функция')
# plt.plot(x_values, y_fourier, 'b--', label=f'Сумма ряда Фурье (N={N})')
plt.scatter(X, Y, color='black', label='Табличные данные')
plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('График интерполированной функции и ряда Фурье')
plt.grid(True)
plt.show()
