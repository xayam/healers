class CPU32:

    def __init__(self):
        pass


summa = 0
for n in range(1, 25):
    summa += n ** 3
    print(summa, n ** 3)
