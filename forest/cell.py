from enum import Enum


class Forest(list):
    def __init__(self, rows=50, cols=50):
        super().__init__(Cell(i) for i in range(rows * cols))
        self.rows = rows
        self.cols = cols

    def index_2d(self, i):
        return i // self.cols, i % self.cols

    def index_linear(self, r, c):
        return self[r * self.cols + c]

    def neighbors(self, cell):
        r, c = self.index_2d(cell.index)
        return [self.index_linear(r + dr, c + dc)
                for dr in range(-1, 2, 1) for dc in range(-1, 2, 1)
                if (dr != 0 or dc != 0) and
                0 <= r + dr < self.rows and
                0 <= c + dc < self.cols]

    def step(self):
        # TODO: the filter was originally taking into account the new_cell.catch_fire() calls
        for fire in list(filter(Cell.on_fire, self)):
            for new_cell in self.neighbors(fire):
                new_cell.catch_fire()

    def is_dead(self):
        return not any(map(Cell.is_alive, self))


class Cell:
    def __init__(self, i):
        self.state = CellState.Dead
        self.index = i

    def catch_fire(self):
        if self.is_alive():
            self.state = CellState.OnFire

    def step(self):
        if self.on_fire():
            self.state = CellState.Dead

    def is_alive(self):
        return self.state != CellState.Dead

    def on_fire(self):
        return self.state == CellState.OnFire


class CellState(Enum):
    Dead = 0
    Alive = 1
    OnFire = 2
