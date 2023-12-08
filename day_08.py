import re
from itertools import cycle
from functools import reduce
from math import lcm

class Node(object):
    def __init__(self, name, left, right) -> None:
        self.name = name
        self.left = left
        self.right = right

    def is_end_node(self):
        if self.name[2] == "Z":
            return True
        return False
    
    def get_next_node(self, network, d):
        if d == "L":
            return network[self.left]
        elif d == "R":
            return network[self.right]
        else:
            raise Exception(f"Something went wrong, dir {d}")


def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


def get_end_cycles(node: Node, network, directions):

    directions = {i: d for i, d in enumerate(directions)}

    directions = cycle(directions.items())

    count = 0
    ends_visited = {}

    while True:
        id, d = next(directions)
        node = node.get_next_node(network, d)

        if node.is_end_node():

            if node.name in ends_visited.keys():
                if id in ends_visited[node.name]["visited"].keys():
                    # This means we've found a loop
                    loop_length = count - ends_visited[node.name]["visited"][id]
                    print(f"Length {loop_length}")
                    return loop_length

                ends_visited[node.name]["visited"][id] = count
            else:
                ends_visited[node.name] =  {"node" : node, "visited": {id: count}}

        count += 1


def part_1(data):

    directions, network = parse_input_data(data)

    current_node = network["AAA"]
    directions = cycle(directions)
    steps = 0

    while current_node.name != "ZZZ":
        d = next(directions)

        if d == "L":
            current_node = network[current_node.left]
        elif d == "R":
            current_node = network[current_node.right]
        else:
            raise Exception(f"Something went wrong, dir {d}")
        steps += 1

    return steps

# def part_2(data):

#     directions, network = parse_input_data(data)

#     current_nodes = [node for node in network.values() if node.name[2] == "A"]

#     directions = cycle(directions)
#     steps = 0

#     while True:
#         d = next(directions)
#         new_nodes = []

#         for node in current_nodes:

#             if d == "L":
#                 new_nodes.append(network[node.left])
#             elif d == "R":
#                 new_nodes.append(network[node.right])
#             else:
#                 raise Exception("Something went wrong")
#         steps += 1

#         if reduce(lambda x, y: x and y, [node.is_end_node() for node in new_nodes]) == True:
#             break

#         current_nodes = new_nodes
        
#     return steps

def part_2(data):

    directions, network = parse_input_data(data)

    current_nodes = [node for node in network.values() if node.name[2] == "A"]

    cycles = [get_end_cycles(node, network, directions) for node in current_nodes]
        
    steps = 0

    return lcm(*cycles)

def parse_input_data(data):

    directions = data[0]
    network = {}

    for row in data[2:]:
        node, left, right = re.findall("[A-Z\d]+", row)
        network[node] = Node(node, left, right)

    return directions, network

if __name__ == "__main__":

    DAY = "08"
    data = read_text_file(f"{DAY}.txt")
    print(part_1(data))
    print(part_2(data))