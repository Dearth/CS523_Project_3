from forest.cell import *

forest = Forest(250, 250, display=True)

for _ in range(5000):
    forest.step()

print("Done")
