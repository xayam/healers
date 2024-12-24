from PIL import Image, ImageDraw, ImageFont

from h.model.barriers.square.square1line import Square1Line
from h.model.utils import utils_progress

width = 1024
height = 512
square1line = Square1Line()
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
            [(height, i), (height - i, height)],
            [(0, height - i), (height - i, height)],
            [(0, height - i), (i, 0)],
            [(height, i), (i, 0)]
        ]
        for x in range(0, height, 64):
            for y in range(0, height, 64):
                draw.rectangle(xy=[(x, y), (x + 64, y + 64)],
                               fill=(64 + x//4, 64 + y//4, 64 + x//4),
                               outline="black", width=1)
                draw.text(xy=(x + 15, y + 15),
                          text=str(y//64 * 8 + x//64).rjust(2, "0"),
                          font=font, fill="black")
        draw.line(xy=square[0], fill=borders[j][0], width=2)
        draw.line(xy=square[3], fill=borders[j][1], width=2)
        draw.line(xy=square[1], fill=borders[j][2], width=2)
        draw.line(xy=square[2], fill=borders[j][3], width=2)
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
        for index1 in range(len(dists[0])):
            distances1 = square1line.get_distances(
                x1=0.0, y1=0.0, x2=dists[0][index1][0], y2=dists[1][index1][0],
                grid=square1line.grid[64]
            )
            if distances1 is None:
                continue
            distances1 = square1line.dim1_to_dim2(distances1)
            distances1 = square1line.dim2_to_dim1(distances1)
            distances2 = square1line.get_distances(
                x1=0.0, y1=0.0, x2=dists[2][index1][0], y2=dists[3][index1][0],
                grid=square1line.grid[64]
            )
            if distances2 is None:
                continue
            distances2 = square1line.dim1_to_dim2(distances2)
            distances2 = square1line.dim2_to_dim1(distances2)
            for index2 in range(len(distances1)):
                k += 1
                utils_progress(f"{filename} | {j}/{i}/{height} | {k}/{2 ** 15}")
                rb = index2 // 256
                g = index2 % 256
                x = round(height + round(256 * (2 * distances1[index2] + 1)))
                y = round(round(256 * (2 * distances2[index2] + 1)))
                draw.point(
                    xy=(x, y),
                    fill=(rb, g, rb),
                )
        images[-1].save(filename, format="PNG")
images[0].save(
    "square4animation.gif",
    save_all=True,
    append_images=images[1:], duration=height, loop=0
)
