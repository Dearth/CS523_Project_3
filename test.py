from forest.cell import *

forest = Forest(50, 50)
for c in forest: c.state = CellState.Alive
forest[0].state = CellState.OnFire

print(forest.neighbors(forest[0]))

while True:
    num_fire = len(list(filter(Cell.on_fire, forest)))
    print(num_fire)
    forest.step()
    input()
