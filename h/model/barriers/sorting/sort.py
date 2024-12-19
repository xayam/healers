
def run(a, r):
    result = [[r[0], r[1], r[2]]]
    for k in range(len(a)):
        c = a[k]
        if c == 0:
            s0 = result[-1][0]
            s1 = result[-1][1]
            s2 = result[-1][2]
        elif c == 1:
            s0 = result[-1][1]
            s1 = result[-1][0]
            s2 = result[-1][2]
        else:
            s0 = result[-1][2]
            s1 = result[-1][0]
            s2 = result[-1][1]
        result.append([s0, s2, s1])
    return result




n = 3
a = [2] * (2 ** n)
i = 2 ** n - 1
while True:

    for x in range(2):
        for y in range(2):
            for z in range(2):
                result = run(a=a, r=[x, y, z])
                print(result)
    break
