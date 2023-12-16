import re
from enum import Enum
from collections import deque

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data

class Direction(Enum):
    L = 1
    R = 2
    U = 3
    D = 4


class Light(object):

    def __init__(self, x, y, direction:Direction) -> None:
        self.x = x
        self.y = y
        self.direction = direction

    def __eq__(self, other):
        return other and self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
      return hash((self.x, self.y, self.direction.value))
    
    @property
    def coords(self):
        return (self.x, self.y)
    
    def is_valid(self, max_x, max_y, visited):
        if self in visited:
            return False
        elif self.x < max_x and self.y < max_y and self.x >= 0 and self.y >= 0:
            return True
        return False


def test_beam(data, inital=Light(0, 0, Direction.R)):
    energised = set()
    visited = set()
    previous_size = -1
    cur_points = deque([inital])
    max_x = len(data[0])
    max_y = len(data)

    while True:
        new_points_deque = deque()
        while cur_points:
            current = cur_points.popleft()
            energised.add(current.coords)
            visited.add(current)

            tile = data[current.y][current.x]

            if tile == "\\":
                if current.direction == Direction.R:
                    newpoint = Light(current.x, current.y+1, Direction.D)
                elif current.direction == Direction.L:
                    newpoint = Light(current.x, current.y-1, Direction.U)
                elif current.direction == Direction.U:
                    newpoint = Light(current.x-1, current.y, Direction.L)
                elif current.direction == Direction.D:
                    newpoint = Light(current.x+1, current.y, Direction.R)
                else:
                    pass

                if newpoint.is_valid(max_x, max_y, visited):
                    new_points_deque.append(newpoint)

            elif tile == r"/":
                if current.direction == Direction.L:
                    newpoint = Light(current.x, current.y+1, Direction.D)
                elif current.direction == Direction.R:
                    newpoint = Light(current.x, current.y-1, Direction.U)
                elif current.direction == Direction.D:
                    newpoint = Light(current.x-1, current.y, Direction.L)
                elif current.direction == Direction.U:
                    newpoint = Light(current.x+1, current.y, Direction.R)
                else:
                    pass

                if newpoint.is_valid(max_x, max_y, visited):
                    new_points_deque.append(newpoint)

            elif tile == "-" and (current.direction == Direction.U or current.direction == Direction.D):
                new_points = [Light(current.x+1, current.y, Direction.R) , Light(current.x-1, current.y, Direction.L)]

                for newpoint in new_points:
                    if newpoint.is_valid(max_x, max_y, visited):
                        new_points_deque.append(newpoint) 

            elif tile == "|"and (current.direction == Direction.R or current.direction == Direction.L):
                new_points = [Light(current.x, current.y+1, Direction.D) , Light(current.x, current.y-1, Direction.U)]

                for newpoint in new_points:
                    if newpoint.is_valid(max_x, max_y, visited):
                        new_points_deque.append(newpoint) 
            else:
                if current.direction == Direction.R:
                    newpoint = Light(current.x+1, current.y, Direction.R)
                elif current.direction == Direction.L:
                    newpoint = Light(current.x-1, current.y, Direction.L)
                elif current.direction == Direction.U:
                    newpoint = Light(current.x, current.y-1, Direction.U)
                elif current.direction == Direction.D:
                    newpoint = Light(current.x, current.y+1, Direction.D)
                else:
                    pass

                if newpoint.is_valid(max_x, max_y, visited):
                    new_points_deque.append(newpoint)

        if len(visited) == previous_size or len(new_points_deque) == 0:
            break
        previous_size = len(visited)
        cur_points = new_points_deque

    return len(energised)

def part_1(data):
    return test_beam(data)

def part_2(data):
    max_x = len(data[0])
    max_y = len(data)

    max_enrgised_xD = max([test_beam(data, Light(x, 0, Direction.D)) for x in range(max_x)])
    max_enrgised_xU = max([test_beam(data, Light(x, max_y-1, Direction.U)) for x in range(max_x)])
    max_enrgised_yL = max([test_beam(data, Light(0, y, Direction.R)) for y in range(max_y)])
    max_enrgised_yR = max([test_beam(data, Light(max_x-1, y, Direction.L)) for y in range(max_y)])

    return max(max_enrgised_xD, max_enrgised_xU, max_enrgised_yL, max_enrgised_yR)

if __name__ == "__main__":

    DAY = "16"
    data = read_text_file(f"{DAY}.txt")
    print(part_1(data))
    print(part_2(data))