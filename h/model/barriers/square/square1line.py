import numpy as np
import matplotlib.pyplot as plt

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
        size = int(len(data) ** 0.5)
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

    def get_distances(
            self,
            x1, y1, x2, y2, grid=None,
            plot=False, plot_name=None
    ):
        grid = self.grid[8] if grid is None else grid
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
        except ZeroDivisionError:
            print(f"ZeroDivisionError | x1={x1} | y1={y1} | x2={x2} | y2={y2}")
            return None
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
        result = []
        for a in range(len(x)):
            result.append(
                [x[a], grid[a][0], grid[a][1]]
            )
        if plot:
            result = sorted(result, key=lambda k: k[0])
            plt.figure(figsize=(20, 20))
            plt.scatter(x, y)
            plt.savefig(plot_name)
            # plt.show()
        return result


def main():
    square1line = Square1Line()
    square1line.get_distances(
        x1=0.0, y1=0.0,
        x2=8, y2=1,
        grid=None,
        plot=True,
        plot_name="square1line_81.png"
    )
    square1line.get_distances(
        x1=0.0, y1=0.0,
        x2=8, y2=7,
        grid=None,
        plot=True,
        plot_name="square1line_87.png"
    )
    square1line.get_distances(
        x1=0.0, y1=0.0,
        x2=8, y2=0.5,
        grid=None,
        plot=True,
        plot_name="square1line_805.png"
    )


if __name__ == "__main__":
    main()
