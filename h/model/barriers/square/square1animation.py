from PIL import Image, ImageDraw, ImageFont

from h.model.barriers.square.square1line import Square1Line

width = 1024
height = 512

square1line = Square1Line()
font = ImageFont.truetype(font="arial.ttf", size=32)
frames = []
for j in range(2):
    for i in range(0, height):
        frame = Image.new(
            mode="RGBA",
            size=(width, height),
            color=(255, 255, 255)
        )
        frames.append(frame)
        canvas = ImageDraw.Draw(frames[-1])
        filename = f"frames1animation/{j}{str(i).rjust(3, '0')}.png"
        square = [
            [(height, i), (0, height - i)],
            [(height - i, height), (i, 1)]
        ]
        coordinates = [
            [256.0, i - 256.0],
            [256.0 - i, 256.0]
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
        canvas.line(
            xy=square[j],
            fill="red",
            width=2
        )
        distance = square1line.get_distances(
            x1=0.0,
            y1=0.0,
            x2=coordinates[j][0],
            y2=coordinates[j][1]
        )
        if distance is None:
            _ = frames.pop()
            continue
        for x, a, b in distance:
            x = height + round((2 * x + 1) / 2 * height)
            r = round(64 * (a + 3.5))
            g = round(64 * (b + 3.5))
            canvas.line(
                xy=[(x, 0), (x, height)],
                fill=(64 + r//4, 64 + g//4, 64 + r//4),
                width=2
            )
        print(filename)
        frames[-1].save(
            fp=filename,
            format="PNG"
        )
frames[0].save(
    fp="square1animation.gif",
    save_all=True,
    append_images=frames[1:],
    duration=15,
    loop=0
)
