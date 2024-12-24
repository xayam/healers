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
for j in range(2):
    for i in range(0, 513):
        # if i % 32 != 0:
        #     continue
        images.append(Image.new(mode="RGBA", size=(width, height),
                                color=(255, 255, 255)))
        draw = ImageDraw.Draw(images[-1])
        filename = f"frames4animation/{j}{str(i).rjust(3, '0')}.png"
        for x in range(0, 512, 64):
            for y in range(0, 512, 64):
                draw.rectangle(xy=[(x, y), (x + 64, y + 64)],
                               fill=(64 + x//4, 64 + y//4, 64 + x//4),
                               outline="black", width=1)
                draw.text(xy=(x + 15, y + 15),
                          text=str(y//64 * 8 + x//64).rjust(2, "0"),
                          font=font, fill ="black")
        draw.line(xy=[(512, i), (512 - i, 512)],
                  fill="red", width=2)
        draw.line(xy=[(512, i), (i, 0)],
                  fill="red", width=2)
        draw.line(xy=[(0, 512 - i), (512 - i, 512)],
                  fill="red", width=2)
        draw.line(xy=[(0, 512 - i), (i, 0)],
                  fill="red", width=2)
        if j == 0:
            dists1 = square1line.get_distances(
                x=256, y=i - 256 + 0.01
            )
            dists2 = square1line.get_distances(
                x=256 - i + 0.01, y=256
            )
            dists3 = square1line.get_distances(
                x=0.01, y=256 - i
            )
            dists4 = square1line.get_distances(
                x=i - 256, y=0.01
            )
        else:
            dists2 = square1line.get_distances(
                x=256, y=i - 256 + 0.01
            )
            dists3 = square1line.get_distances(
                x=256 - i + 0.01, y=256
            )
            dists4 = square1line.get_distances(
                x=0.01, y=256 - i
            )
            dists1 = square1line.get_distances(
                x=i - 256, y=0.01
            )
        if dists1 is None or dists2 is None or dists3 is None or dists4 is None:
            _ = images.pop()
            continue
        dists1 = square1line.dim1_to_dim2(dists1)
        dists2 = square1line.dim1_to_dim2(dists2)
        dists3 = square1line.dim1_to_dim2(dists3)
        dists4 = square1line.dim1_to_dim2(dists4)
        k = 0
        for i1 in range(len(dists1)):
            distances1 = square1line.get_distances(
                x=dists1[i1][0], y=dists2[i1][0], grid=square1line.grid[64]
            )
            if distances1 is None:
                continue
            distances1 = square1line.dim1_to_dim2(distances1)
            distances1 = square1line.dim2_to_dim1(distances1)

            # print("distances1")
            distances2 = square1line.get_distances(
                x=dists3[i1][0], y=dists4[i1][0], grid=square1line.grid[64]
            )
            if distances2 is None:
                continue
            distances2 = square1line.dim1_to_dim2(distances2)
            distances2 = square1line.dim2_to_dim1(distances2)
            # print(distances1)
            for index in range(len(distances1)):
                k += 1
                utils_progress(f"{filename} | {j}/{i}/512 | {k}/{2 ** 15}")
                _rb = index % 256
                _g = index // 256
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
    append_images=images[1:], duration=15, loop=0
)
