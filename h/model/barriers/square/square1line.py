import numpy as np
# import matplotlib.pyplot as plt

np.random.seed(0)


class Square1Line:

    def __init__(self):
        self.grid = {8: [], 64: []}
        self.init()

    def init(self):
        for grid in self.grid:
            x = 0.5 - grid // 2
            for _ in range(grid):
                y = 0.5 - grid // 2
                for _ in range(grid):
                    self.grid[grid].append([x, y])
                    y += 1
                x += 1

    @staticmethod
    def dim1_to_dim2(data):
        # print(data)
        size = int(len(data) ** 0.5)
        # print(size)
        result = [[0. for _ in range(size)] for _ in range(size)]
        for distance, x, y in data:
            result[int(x + size // 2 - 0.5)][int(y + size // 2 - 0.5)] = distance
        return result

    @staticmethod
    def dim2_to_dim1(data):
        result = []
        for i in range(len(data)):
            for j in range(len(data[i])):
                result.append(data[i][j])
        result_mean = sum(result) / len(result)
        result = np.asarray(result)
        result = (result_mean - result) / (max(result) - min(result))
        return result.tolist()

    def get_distances(self, x1, y1, x2, y2, grid=None):
        grid = self.grid[8] if grid is None else grid
        if x1 == 0.0 or y1 == 0.0 or abs(x1) == abs(y1):
            return None
        if x2 == 0.0 or y2 == 0.0 or abs(x2) == abs(y2):
            return None
        try:
            X = [
                [
                    (c[1] - y1 + x1 * (y2 - y1) /
                     (x2 - x1) - c[0] * (x2 - x1) / (y2 - y1)) /
                    ((y2 - y1) / (x2 - x1) - (x2 - x1) / (y2 - y1)),
                    0
                ]
                for c in grid
            ]
        except Exception as e:
            print(f"x1={x1}, y1={y1}, x2={x2}, y2={y2}")
            raise e
        X = [
            [
                c[0],
                y1 + (y2 - y1) / (x2 - x1) * (c[0] - x1)
            ]
            for c in X
        ]
        x = [c[0] for c in X]
        y = [c[1] for c in X]
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        x = [(mean_x - c) / (max(x) - min(x)) for c in x]
        y = [(mean_y - c) / (max(y) - min(y)) for c in y]
        d = []
        for a in range(len(x)):
            sign = 1.0 if x[a] >= 0.0 else -1.0
            d.append([sign * (x[a] ** 2 + y[a] ** 2),
                      grid[a][0], grid[a][1]])
        result = d
        # result = sorted(d, key=lambda k: k[0])
        # print(result)
        # plt.scatter(x, y)
        # plt.show()
        return result
