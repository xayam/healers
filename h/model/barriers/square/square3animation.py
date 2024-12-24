from PIL import Image, ImageDraw, ImageFont

from h.model.barriers.square.square1line import Square1Line

width = 1024
height = 512
step = 1
# step = 32

square1line = Square1Line()
font = ImageFont.truetype(
    font="arial.ttf",
    size=32
)
frames = []
borders = ["red", "green", "blue"]
indexes = [[0, 1], [1, 2], [2, 0]]
for j in range(4):
    for i in range(0, height, step):
        frame = Image.new(
            mode="RGBA",
            size=(width, height),
            color=(255, 255, 255)
        )
        frames.append(frame)
        canvas = ImageDraw.Draw(frames[-1])
        filename = f"frames3animation/{j}{str(i).rjust(3, '0')}.png"
        square = [
            [
                [(height, i), (height - i, height)],
                [(height - i, height), (0, height - i)],
                [(0, height - i), (height, i)]
            ],
            [
                [(height - i, height), (0, height - i)],
                [(0, height - i), (i, 0)],
                [(i, 0), (height - i, height)]
            ],
            [
                [(0, height - i), (i, 0)],
                [(i, 0), (height, i)],
                [(height, i), (0, height - i)],
            ],
            [
                [(i, 0), (height, i)],
                [(height, i), (height - i, height)],
                [(height - i, height), (i, 0)],
            ]
        ]
        for x in range(0, height, 64):
            for y in range(0, height, 64):
                canvas.rectangle(
                    xy=[(x, y), (x + 64, y + 64)],
                    fill=(64 + x // 4, 64 + y // 4, 64 + x // 4),
                    outline="black",
                    width=1
                )
                canvas.text(
                    xy=(x + 15, y + 15),
                    text=str(y // 64 * 8 + x // 64).rjust(2, "0"),
                    font=font,
                    fill="black"
                )
        distances = []
        for z in range(3):
            canvas.line(
                xy=square[j][z],
                fill=borders[z],
                width=2
            )
            distances.append(square1line.get_distances(
                x1=square[j][z][0][0],
                y1=square[j][z][0][1],
                x2=square[j][z][1][0],
                y2=square[j][z][1][1]
            ))
        if None in distances:
            _ = frames.pop()
            continue
        print(f"[INFO] {filename} | {j + 1}/4 | {i}/{height}")
        for z in range(len(distances)):
            distances[z] = square1line.dim1_to_dim2(distances[z])
        for index1 in range(len(distances[0])):
            distance = []
            for z in range(3):
                distance.append(square1line.get_distances(
                    x1=0.0,
                    y1=0.0,
                    x2=distances[indexes[z][0]][index1][0],
                    y2=distances[indexes[z][1]][index1][0],
                    grid=square1line.grid[64]
                ))
            if None in distance:
                continue
            for z in range(3):
                distance[z] = square1line.dim1_to_dim2(distance[z])
                distance[z] = square1line.dim2_to_dim1(distance[z])
            for index2 in range(len(distance[0])):
                t = round(256 * (2 * distance[2][index2] + 1) / 2)
                r = t % 256
                g = t // 256
                x = height + round(256 * (2 * distance[0][index2] + 1))
                y = round(256 * (2 * distance[1][index2] + 1))
                canvas.point(
                    xy=(x, y),
                    fill=(r, g, r),
                )
        frames[-1].save(
            fp=filename,
            format="PNG"
        )
frames[0].save(
    fp="square3animation.gif",
    save_all=True,
    append_images=frames[1:],
    duration=15 * step,
    loop=0
)
