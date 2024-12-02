from init import *

pos = 2
positions = []
orbital = [[0], [0]]
summa = 0
volume = 0

# for planet, coeff in COEFFS.items():
for i in range(1, 12 + 1):
    positions.append(pos)
    orbital.append(positions[:])
    orbitals = sum(map(sum, orbital))
    summa += orbitals
    n = 2 * i
    border = 2 * (n ** 2 + (n - 2) * n + (n - 2) ** 2)
    volume += border
    print(
        "№" + str(i).rjust(2, " "),
        "n: " + str(n).rjust(2, " "),
        "pos: " + str(pos).rjust(2, " "),
        "orbital: " + str(orbitals - sum(map(sum, orbital[:-1]))).rjust(3, " "),
        "orbitals: " + str(orbitals).rjust(4, " "),
        "border: " + str(border).rjust(4, " "),
        "summa: " + str(summa).rjust(4, " "),
        "volume: " + str(volume).rjust(5, " "),
        sep="; "
    )
    pos += 4

#    2 - ???
#   10 - ???
#   28 - ???
#   60 - ???
#  110 - ???
#  182 - ???
#  280 - ???
#  408 - ???
#  570 - ???
#  770 - ???
# 1012 - ???
# 1300 - ???
