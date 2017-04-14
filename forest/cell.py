from itertools import product

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.animation import FuncAnimation

DEAD = np.uint8(0)
ALIVE = np.uint8(1)
ON_FIRE = np.uint8(2)


class Forest:
    def __init__(self, rows=250, cols=250, p1=0.3, p2=0, display=False):
        self.cells = np.zeros((rows, cols), dtype=np.uint8)
        self.rows = rows
        self.cols = cols
        self.p = p1 + p2
        self.deltas = np.array([x + y * self.rows for (x, y) in product(range(-1, 2), range(-1, 2))])

        if not display: return

        # This code follows the examples at http://scipython.com/blog/the-forest-fire-model/
        colors_list = ['brown', 'green', 'red', 'orange']
        cmap = colors.ListedColormap(colors_list)
        bounds = [0, 1, 2, 3]
        norm = colors.BoundaryNorm(bounds, cmap.N)

        def step_and_redraw(*_):
            self.step()
            self.image.set_array(self.cells)
            return self.image,

        fig = plt.figure()
        self.image = plt.imshow(self.cells, cmap=cmap, norm=norm, animated=True)
        animation = FuncAnimation(fig, step_and_redraw, interval=100, blit=True)
        plt.show()

    def step(self):
        dead = self.cells == DEAD
        self.cells[dead] = np.random.rand(np.sum(dead)) < self.p

        flat = self.cells.flat
        (x0,) = np.where(flat == ON_FIRE)
        xs = np.repeat(x0, 9).reshape(-1, 9) + self.deltas
        xs = xs[np.logical_and(xs >= 0, xs < self.rows * self.cols)]

        flat[xs] = (flat[xs] & ALIVE) << 1

        alive = self.cells == ALIVE
        self.cells[alive] = ALIVE + (np.random.rand(np.sum(alive)) < 0.001)

    def is_dead(self):
        return np.sum(self.cells == ALIVE) == 0
