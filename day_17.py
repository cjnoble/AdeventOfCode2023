import re
from enum import Enum
from collections import deque
from math import inf

class Dir(Enum):
    LR = 1
    UD = 2


class Node(object):
    def __init__(self, x, y, heat_loss, dir:Dir, parent=None) -> None:
        self.x = x
        self.y = y
        self.heat_loss = heat_loss
        self.dir = dir

        self.g = inf
        
        self.parent = parent
        self.start_node = False

    @property
    def f(self):
        return self.g

    def set_as_first_node(self, data):
        self.start_node = True
        self.g = 0
        # self.update_h(data)

    def update_g(self, node, data):

        if self.y == node.y:
            total_heat_loss = sum(data[self.y][x] for x in range(node.x, self.x, 1 if node.x < self.x else -1)) - data[node.y][node.x]
        else:
            total_heat_loss = sum(data[y][self.x] for y in range(node.y, self.y, 1 if node.y < self.y else -1)) - data[node.y][node.x]

        if (total_heat_loss:= node.g + total_heat_loss + self.heat_loss) < self.g:
            self.g = total_heat_loss


    def __repr__(self) -> str:
        return f"{self.x} {self.y} {self.dir} {self.f}"


    def get_successors(self, nodes):

        successors = []

        if self.start_node or self.dir == Dir.LR:
            successors.extend([(self.x, self.y+y, Dir.UD) for y in [-3, -2, -1, 1, 2, 3]])
        if self.start_node or self.dir == Dir.UD:
            successors.extend([(self.x+x, self.y, Dir.LR) for x in [-3, -2, -1, 1, 2, 3]])

        return [nodes[key] for key in successors if key in nodes]

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.dir))
    
    def __eq__(self, other) -> int:
        if self is other:
            return True
        else:
            return False
    
    def __neq__(self, other) -> int:
        return not self == other
    
    def dist(self, other):
        return abs((self.x - other.x) + (self.y - other.y))


class UltraNode(Node):
    def get_successors(self, nodes):

        successors = []

        if self.start_node or self.dir == Dir.LR:
            successors.extend([(self.x, self.y+y, Dir.UD) for y in range(-10, 11, 1) if abs(y)>3])
        if self.start_node or self.dir == Dir.UD:
            successors.extend([(self.x+x, self.y, Dir.LR) for x in range(-10, 11, 1) if abs(x)>3])

        return [nodes[key] for key in successors if key in nodes]


def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    data = [[int(i) for i in row] for row in data]

    return data


# def get_successors(data, node:Node):
#     max_x = len(data[0])
#     max_y = len(data)

#     if node.dir == Dir.LR:
#         successors = [Node(node.x, node.y+y, data[node.y+y][node.x], Dir.UD, parent=node) for y in [-3, -2, -1, 1, 2, 3] if node.y + y < max_y and node.y + y >=0]
#     else:
#         successors = [Node(node.x+x, node.y, data[node.y][node.x+x], Dir.LR, parent=node) for x in [-3, -2, -1, 1, 2, 3] if node.x + x < max_x and node.x + x >=0]

#     return successors



def part_1(data):

    max_x = len(data[0])
    max_y = len(data)

    nodes = {(x, y, dir): Node(x, y, data[y][x], dir) for x in range(max_x) for y in range(max_y) for dir in [Dir.LR, Dir.UD]}

    return run(nodes, max_x, max_y)


def plot(nodes, max_x, max_y):
    print("\n")
    for y in range(max_y):
        print([f"{min(nodes[(x, y, Dir.LR)].f, nodes[(x, y, Dir.UD)].f):03.0f}" for x in range(max_x)])

def part_2(data):

    max_x = len(data[0])
    max_y = len(data)

    nodes = {(x, y, dir): UltraNode(x, y, data[y][x], dir) for x in range(max_x) for y in range(max_y) for dir in [Dir.LR, Dir.UD]}

    return run(nodes, max_x, max_y)

def run(nodes, max_x, max_y):
    shortest_path_list = set() 

    nodes[(0, 0, Dir.LR)].set_as_first_node(data)

    all_nodes_set = set(nodes.values())

    while len(shortest_path_list) < (2*max_x*max_y):

        #plot(nodes, max_x, max_y)

        next_node = min(all_nodes_set, key= lambda x: x.f)
        all_nodes_set.remove(next_node)
        #print(next_node)
    
        shortest_path_list.add(next_node)

        successors = next_node.get_successors(nodes)
        for successor in successors:
            successor.update_g(next_node, data)

        if len(shortest_path_list)%100 == 0:
            print(f"{len(shortest_path_list)} / {2*max_x*max_y}")

    return min(nodes[(max_x-1, max_y-1, Dir.LR)].f, nodes[(max_x-1, max_y-1, Dir.UD)].f)

if __name__ == "__main__":

    DAY = "17"
    data = read_text_file(f"{DAY}.txt")
    #print(part_1(data))
    print(part_2(data))