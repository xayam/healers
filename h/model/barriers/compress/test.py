import random

from PIL import Image, ImageDraw, ImageFont

width = 9 * 8
rand = random.SystemRandom(0)

arr = [rand.choice([0, 1]) for _ in range(width)]


def n3transform(data):
    transform = {
        "000": [0, 0, 0],
        "001": [1, 0, 1],
        "010": [1, 0, 0],
        "011": [1, 1, 1],
        "100": [0, 0, 1],
        "101": [1, 1, 0],
        "110": [0, 1, 0],
        "111": [0, 1, 1],
    }
    output = data[:]
    for i in range(0, len(data), 3):
        output[i] = transform[
            str(data[i]) + str(data[i + 1]) + str(data[i + 2])
            ][0]
        output[i + 1] = transform[
            str(data[i]) + str(data[i + 1]) + str(data[i + 2])
            ][1]
        output[i + 2] = transform[
            str(data[i]) + str(data[i + 1]) + str(data[i + 2])
            ][2]
    return output
dataset = []
print(arr)
for j in range(3):
    data = n3transform(arr[:])
    print(data)
    data1, data2, data3 = [], [], []
    for i in range(0, len(data), 3):
        data1.append(data[i])
        data2.append(data[i + 1])
        data3.append(data[i + 2])
    arr = [arr[-1]] + arr[:-1]
    dataset.append(data1 + data2 + data3)
frame = Image.new(
            mode="RGBA",
            size=(width * width // 3, width * width // 3),
            color=(128, 128, 128)
        )
canvas = ImageDraw.Draw(frame)
for i in range(0, width, 3):
    for d in range(len(dataset)):
        fill = (255 * dataset[d][i],
                255 * dataset[d][i + 1],
                255 * dataset[d][i + 2])
        xy = [
            (width * i // 3, width * width // 3 // len(dataset) * d),
            (width * (i // 3 + 1), width * width // 3 // len(dataset) * (d + 1))
        ]
        canvas.rectangle(xy=xy, fill=fill)

frame.save(fp="test.png", format="PNG")
