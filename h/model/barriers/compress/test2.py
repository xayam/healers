import time

time1 = time.time_ns()
summa = 0
for i in range(1, 100000):
    summa += i
time2 = time.time_ns()
print(time2 - time1)
print(summa)
