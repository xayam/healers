import math

DIAMETER_SUN = 1_392_700_000
DISTANCE_AE = 149_597_871_000
DISTANCE = 0
DIAMETR = 1
COEFFS = {
    "Меркурий": [0.38, 0.382],
    "Венера": [0.72, 0.949],
    "Земля": [1.0, 1.0],
    "Марс": [1.52, 0.53],
    # "Церера": [2.76, 0.074],
    "Юпитер": [5.2, 11.2],
    "Сатурн": [9.54, 9.41],
    "Уран": [19.22, 3.98],
    "Нептун": [30.06, 3.81],
    "Плутон": [39.2, 0.186],
    "Хаумеа": [43.0, 0.11],
    "Макемаке": [45.4, 0.116],
    "Эрида": [67.8, 0.182],
}
LENGTH_ORBIT = {}
DISTANCE_TO_SUN = {}
for planet, _ in COEFFS.items():
    DISTANCE_TO_SUN[planet] = \
        DISTANCE_AE * COEFFS[planet][DISTANCE] + DIAMETER_SUN // 2
    LENGTH_ORBIT[planet] = 2 * math.pi * DISTANCE_TO_SUN[planet]

length_of_the_orbit = {}

earth_orbit = 3
