class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls

    def neighbors(self, id):
        (x, y) = id
        results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        if (x + y) % 2 == 0: results.reverse()  # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results


class GridWithWeights(SquareGrid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)


def draw_map(map, path):
    for x in range(map.height):
        for y in range(map.width):
            label = " "
            pos = (x, y)
            if pos in path:
                label = "@"
            elif map.passable(pos):
                label = "."
            else:
                label = "#"
            print(label, end=" ")
        print()


# testing
from find_path import *
m = GridWithWeights(30, 15)
m.walls = [(2,2), (2,3), (2,4), (3,3), (3,4), (6,7), (7,7), (6,8), (7,8), (7,9)]

path = a_star_search(m, (0, 0), (17, 9))
draw_map(m, path)