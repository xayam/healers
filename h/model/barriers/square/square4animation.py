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
for i in range(1, 513):
    images.append(Image.new(mode="RGBA", size=(width, height),
                            color=(255, 255, 255)))
    draw = ImageDraw.Draw(images[-1])
    for x in range(0, 512, 64):
        for y in range(0, 512, 64):
            draw.rectangle(xy=[(x, y), (x + 64, y + 64)],
                           fill=(64 + x//4, 64 + y//4, 64 + x//4),
                           outline="black", width=1)
            draw.text(xy=(x + 15, y + 15),
                      text=str(y//64 * 8 + x//64).rjust(2, "0"),
                      font=font, fill ="black")
    draw.line(xy=[(512, i), (1, 512 - i)],
              fill="red", width=2)
    dists1 = square1line.get_distances(
        x=256, y=i - 256 + 0.01
    )
    draw.line(xy=[(512, i), (1, 512 - i)],
              fill="red", width=2)
    dists2 = square1line.get_distances(
        x=256 - i + 0.01, y=256
    )
    draw.line(xy=[(512, i), (1, 512 - i)],
              fill="red", width=2)
    dists3 = square1line.get_distances(
        x=0.01, y=256 - i
    )
    draw.line(xy=[(512, i), (1, 512 - i)],
              fill="red", width=2)
    dists4 = square1line.get_distances(
        x=i - 256, y=0.01
    )
    dists1 = square1line.dim1_to_dim2(dists1)
    dists2 = square1line.dim1_to_dim2(dists2)
    dists3 = square1line.dim1_to_dim2(dists3)
    dists4 = square1line.dim1_to_dim2(dists4)

    for i1 in range(len(dists1)):
        distances1 = square1line.get_distances(
            x=dists1[i1][0], y=dists2[i1][0], grid=square1line.grid[64]
        )
        if distances1 is None:
            continue
        distances1 = square1line.dim1_to_dim2(distances1)
        for i2 in range(len(dists3)):
            distances2 = square1line.get_distances(
                x=dists3[i2][0], y=dists4[i2][0], grid=square1line.grid[64]
            )
            if distances2 is None:
                continue
            distances2 = square1line.dim1_to_dim2(distances2)
            for i3 in range(len(distances1)):
                distances = square1line.get_distances(
                    x=distances1[i3][0], y=distances2[i3][0],
                    grid=square1line.grid[64]
                )
                if distances is None:
                    continue
                for xx, aa, bb in distances:
                    c = round((2 * xx + 1) / 2 * 256) - 1
                    x = round(64 * (aa + 3.5))
                    y = round(64 * (bb + 3.5))
                    draw.point(
                        xy=(x, y),
                        fill=(c, c, c),
                    )
    filename = f"square4animation/{str(i).rjust(3, '0')}.png"
    utils_progress(filename)
    images[-1].save("test.png", format="PNG")
    break
    if i % 32 != 0:
        _ = images.pop()
images[0].save(
    "square4animation.gif",
    save_all=True,
    append_images=images[1:], duration=3000, loop=0
)
