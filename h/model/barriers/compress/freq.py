import math
import random

import numpy as np
from matplotlib import pyplot as plt
from scipy.fft import irfft, rfft, rfftfreq

SAMPLE_RATE = 256
DURATION = 1

def generate_sine_wave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    y = np.sin((2 * np.pi) * frequencies)
    return x, y

_, nice_tone = generate_sine_wave(400, SAMPLE_RATE, DURATION)
_, noise_tone = generate_sine_wave(4000, SAMPLE_RATE, DURATION)
# mixed_tone = noise_tone + nice_tone
rand = random.SystemRandom(0)
r = list(range(2 * SAMPLE_RATE))
r = np.asarray(r)
mixed_tone = np.asarray(
    [
        # r[i]
        rand.choice(r)
        # np.sin(np.pi * 2 * r[i])
        for i in range(2 * SAMPLE_RATE)
    ]
)
print(list(mixed_tone))
normalized_tone = mixed_tone
# normalized_tone = np.int16((mixed_tone / mixed_tone.max()) * 32767)
N = SAMPLE_RATE * DURATION

yf = rfft(normalized_tone)
xf = rfftfreq(N, 1 / SAMPLE_RATE)

yf = np.abs(yf)
yf = 256 - 256 / yf
# yf = 2 * (np.abs(yf) / np.max(yf) - 0.5)
# yf = [2 * (i - yf[i]) for i in range(len(yf))]
# yf = np.abs(yf) / np.max(yf) * SAMPLE_RATE / 2
# yf = sorted(yf)
# print(list(yf))
plt.plot(list(range(-257, 0)), yf)
plt.show()

# yf = irfft(yf)
# yf = yf - yf[len(yf) // 2]
# yf = [np.sqrt(i ** 2 - yf[i]) for i in range(256)]
# print(list(yf))
# plt.plot(yf)
# plt.show()