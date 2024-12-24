from PIL import Image, ImageDraw, ImageFont
from pandas.io.formats.info import frame_sub_kwargs

from h.model.barriers.square.square1line import Square1Line
from h.model.utils import utils_progress

width = 1024
height = 512
square1line = Square1Line()
font = ImageFont.truetype(
    font="arial.ttf",
    size=32
)
frames = []
borders = [
    ["red", "green", "blue", "yellow"],
    ["green", "yellow", "red", "blue"],
    ["yellow", "blue", "green", "red"],
    ["blue", "red", "yellow", "green"]
]
coordinates = [
    [0, 2, 3, 1],
    [1, 3, 0, 2],
    [3, 2, 1, 0],
    [2, 0, 3, 1]
]
for j in range(4):
    for i in range(0, height, 32):
        frame = Image.new(
            mode="RGBA",
            size=(width, height),
            color=(255, 255, 255)
        )
        frames.append(frame)
        canvas = ImageDraw.Draw(frames[-1])
        filename = f"frames4animation/{j}{str(i).rjust(3, '0')}.png"
        square = [
            [(height, i), (height - i, height)],
            [(0, height - i), (height - i, height)],
            [(0, height - i), (i, 0)],
            [(height, i), (i, 0)]
        ]
        for x in range(0, height, 64):
            for y in range(0, height, 64):
                canvas.rectangle(
                    xy=[(x, y), (x + 64, y + 64)],
                    fill=(64 + x//4, 64 + y//4, 64 + x//4),
                    outline="black",
                    width=1
                )
                canvas.text(
                    xy=(x + 15, y + 15),
                    text=str(y//64 * 8 + x//64).rjust(2, "0"),
                    font=font,
                    fill="black"
                )
        canvas.line(xy=square[0], fill=borders[j][0], width=2)
        canvas.line(xy=square[3], fill=borders[j][1], width=2)
        canvas.line(xy=square[1], fill=borders[j][2], width=2)
        canvas.line(xy=square[2], fill=borders[j][3], width=2)
        distances = []
        for z in range(4):
            distances.append(square1line.get_distances(
                x1=square[coordinates[z][0]][0][0],
                y1=square[coordinates[z][1]][0][1],
                x2=square[coordinates[z][2]][1][0],
                y2=square[coordinates[z][3]][1][1]
            ))
        if None in distances:
            _ = frames.pop()
            continue
        for z in range(4):
            distances[z] = square1line.dim1_to_dim2(distances[z])
        k = 0
        for index1 in range(len(distances[0])):
            distance1 = square1line.get_distances(
                x1=0.0,
                y1=0.0,
                x2=distances[0][index1][0],
                y2=distances[1][index1][0],
                grid=square1line.grid[64]
            )
            if distance1 is None:
                continue
            distance1 = square1line.dim1_to_dim2(distance1)
            distance1 = square1line.dim2_to_dim1(distance1)
            distance2 = square1line.get_distances(
                x1=0.0,
                y1=0.0,
                x2=distances[2][index1][0],
                y2=distances[3][index1][0],
                grid=square1line.grid[64]
            )
            if distance2 is None:
                continue
            distance2 = square1line.dim1_to_dim2(distance2)
            distance2 = square1line.dim2_to_dim1(distance2)
            for index2 in range(len(distance1)):
                k += 1
                utils_progress(f"{filename} | {j}/{i}/{height} | {k}/{2 ** 15}")
                r = index2 // 256
                g = index2 % 256
                x = round(height + round(256 * (2 * distance1[index2] + 1)))
                y = round(round(256 * (2 * distance2[index2] + 1)))
                canvas.point(
                    xy=(x, y),
                    fill=(r, g, r),
                )
        frames[-1].save(
            fp=filename,
            format="PNG"
        )
frames[0].save(
    fp="square4animation.gif",
    save_all=True,
    append_images=frames[1:],
    duration=height,
    loop=0
)
