import sys

from PIL import Image, ImageDraw, ImageFont

from h.model.barriers.square.square1line import Square1Line
from h.model.utils import utils_progress

square1line = Square1Line()
width = 1025
height = 513
angles = [(0, 0), (0, height-1), (width-1, height-1), (width-1, 0)]
font = ImageFont.truetype(font="arial.ttf", size=32)
images = []
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
    for i in range(0, height):
        if i % 32 != 0:
            continue
        images.append(Image.new(mode="RGBA", size=(width, height),
                                color=(255, 255, 255)))
        draw = ImageDraw.Draw(images[-1])
        filename = f"frames4animation/{j}{str(i).rjust(3, '0')}.png"
        square = [
            [(512, i), (512 - i, 512)],
            [(0, 512 - i), (512 - i, 512)],
            [(0, 512 - i), (i, 0)],
            [(512, i), (i, 0)]
        ]
        for x in range(0, 512, 64):
            for y in range(0, 512, 64):
                draw.rectangle(xy=[(x, y), (x + 64, y + 64)],
                               fill=(64 + x//4, 64 + y//4, 64 + x//4),
                               outline="black", width=1)
                draw.text(xy=(x + 15, y + 15),
                          text=str(y//64 * 8 + x//64).rjust(2, "0"),
                          font=font, fill ="black")
        draw.line(xy=square[0],
                  fill=borders[j][0], width=2)
        draw.line(xy=square[3],
                  fill=borders[j][1], width=2)
        draw.line(xy=square[1],
                  fill=borders[j][2], width=2)
        draw.line(xy=square[2],
                  fill=borders[j][3], width=2)
        dists = []
        for z in range(4):
            dists.append(square1line.get_distances(
                x1=square[coordinates[z][0]][0][0],
                y1=square[coordinates[z][1]][0][1],
                x2=square[coordinates[z][2]][1][0],
                y2=square[coordinates[z][3]][1][1]
            ))
        if None in dists:
            _ = images.pop()
            continue
        for z in range(4):
            dists[z] = square1line.dim1_to_dim2(dists[z])
        k = 0
        for i1 in range(len(dists[0])):
            distances1 = square1line.get_distances(
                x1=0.0, y1=0.0, x2=dists[0][i1][0], y2=dists[1][i1][0],
                grid=square1line.grid[64]
            )
            if distances1 is None:
                continue
            distances1 = square1line.dim1_to_dim2(distances1)
            distances1 = square1line.dim2_to_dim1(distances1)
            distances2 = square1line.get_distances(
                x1=0.0, y1=0.0, x2=dists[2][i1][0], y2=dists[3][i1][0],
                grid=square1line.grid[64]
            )
            if distances2 is None:
                continue
            distances2 = square1line.dim1_to_dim2(distances2)
            distances2 = square1line.dim2_to_dim1(distances2)
            for index in range(len(distances1)):
                k += 1
                utils_progress(f"{filename} | {j}/{i}/512 | {k}/{2 ** 15}")
                _rb = index // 256
                _g = index % 256
                _xx = round(512 + round(256 * (2 * distances1[index] + 1)))
                _yy = round(round(256 * (2 * distances2[index] + 1)))
                draw.point(
                    xy=(_xx, _yy),
                    fill=(_rb, _g, _rb),
                )
        images[-1].save(filename, format="PNG")
images[0].save(
    "square4animation.gif",
    save_all=True,
    append_images=images[1:], duration=515, loop=0
)
