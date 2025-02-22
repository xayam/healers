import random

n = 11
width = n
rand = random.SystemRandom(0)
data1 = [rand.choice([0, 1]) for _ in range(width)]


def list2list(data):
    result = data[:]
    transform = {
        0: [[4, 5, 6]],
        1: [[2, 3, 4], [6, 7, 8]],
        2: [[0, 1, 2], [4, 5, 6], [8, 9, 10]],
        3: [[2, 3, 4], [6, 7, 8]],
        4: [[0, 1, 2], [4, 5, 6], [8, 9, 10]],
    }
    # transform = transform.__reversed__()
    for t in transform:
        for i in transform[t]:
            if result[i[1]] == 1:
                result[i[0]], result[i[2]] = \
                    result[i[2]], result[i[0]]
    return result


def view(data):
    result = " | ".join(map(str, data))
    return result


count1 = 0
while True:
    count1 += 1
    print(count1)
    print(view(data=data1))
    input("Press ENTER for continue...")
    data1 = list2list(data1)
