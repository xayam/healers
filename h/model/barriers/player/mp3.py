import time

import pydub
import numpy as np
import winsound


def read(f, normalized=False):
    """MP3 to numpy array"""
    a = pydub.AudioSegment.from_mp3(f)
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return a.frame_rate, np.float32(y) / 2 ** 15
    else:
        return a.frame_rate, y


def write(f, sr, x, normalized=False):
    """numpy array to MP3"""
    channels = 2 if (x.ndim == 2 and x.shape[1] == 2) else 1
    if normalized:  # normalized array - each item should be a float in [-1, 1)
        y = np.int16(x * 2 ** 15)
    else:
        y = np.int16(x)
    song = pydub.AudioSegment(y.tobytes(), frame_rate=sr, sample_width=2,
                              channels=channels)
    song.export(f, format="mp3", bitrate="320k")


# m = read("test.mp3")
# print(m[1][100000])
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from scipy.signal import spectrogram

# Загружаем аудиофайл
audio = AudioSegment.from_mp3("mp3.mp3")

# Получаем массив сэмплов
samples = np.array(audio.get_array_of_samples())
# audio.get_array_of_samples().export("mashup.mp3", format="mp3", bitrate="192k")
# Если аудиофайл стерео, то берем только один канал (например, левый)
if audio.channels == 2:
    samples = samples[0::2]  # Левый канал

# Нормализуем сэмплы
normalized_samples = samples / np.max(np.abs(samples))

# Параметры
frame_rate = audio.frame_rate

# Вычисляем спектрограмму
frequencies, times, Sxx = spectrogram(
    normalized_samples, fs=frame_rate, nperseg=2**32
)

# Построение спектрограммы
# plt.figure(figsize=(12, 6))
# plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='gouraud')
# plt.colorbar(label='Интенсивность (дБ)')
# plt.title('Спектрограмма')
# plt.ylabel('Частота (Гц)')
# plt.xlabel('Время (с)')
# plt.ylim(0, 2000)  # Ограничиваем частоты для лучшей видимости
# plt.show()
print(len(frequencies))
for f in range(len(frequencies)):
    if f < 37: continue
    winsound.Beep(f, 2)