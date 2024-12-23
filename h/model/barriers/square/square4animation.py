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
        if j == 0:
            draw.line(xy=[(512, i), (1, 512 - i)],
                      fill="red", width=2)
            dists = square1line.get_distances(
                x=256, y=i - 256 + 0.01
            )
        else:
            draw.line(xy=[(512 - i, 512), (i, 1)],
                      fill="red", width=2)
            dists = square1line.get_distances(
                x=256 - i + 0.01, y=256
            )
        # print(dists)
        for xx, aa, bb in dists:
            _xx = 512 + round((2 * xx + 1) / 2 * 512)
            _aa = round(64 * (aa + 3.5))
            _bb = round(64 * (bb + 3.5))
            draw.line(
                xy=[(_xx, 0), (_xx, 512)],
                fill=(64 + _aa//4, 64 + _bb//4, 64 + _aa//4),
                width=2
            )
        filename = f"square4animation/{j}{str(i).rjust(3, '0')}.png"
        utils_progress(filename)
        images[-1].save(filename, format="PNG")
        if i % 32 != 0:
            _ = images.pop()
images[0].save(
    "square4animation.gif",
    save_all=True,
    append_images=images[1:], duration=3000, loop=0
)
