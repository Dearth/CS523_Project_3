from enum import Enum


class Forest:
    # [], index
    def __init__(self, rows=50, cols=50):
        self.cells = [Cell() for _ in range(rows * cols)]

    def step(self):
        filter(Cell.on_fire, self.cells)

    def is_dead(self):
        return not any(map(Cell.is_alive, self.cells))

    def index


class Cell:
    def __init__(self):
        self.state = CellState.Dead

    def lightning(self):
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


