import re
from abc import ABC, abstractmethod
from enum import Enum
from collections import Counter
from copy import deepcopy

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


class Pipe(ABC):
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        super().__init__()

    @abstractmethod
    def get_connecting_pipes(self, data):
        pass

    @classmethod
    def new_pipe(cls, x, y, symbol):

        for pipe in [Vertical, Horizontal, L, Seven, J, F, Start]:
            if symbol == pipe.symbol:
                return pipe(x, y)

        raise Exception("Unknown pipe type")
    
    @classmethod
    def is_pipe_symbol(cls, symbol):

        if symbol in [pipe.symbol for pipe in [Vertical, Horizontal, L, Seven, J, F, Start]]:
            return True
        else:
            return False
        
    @classmethod
    def get_pipes(cls, coordinates, data):

        coordinates = [(c[0], c[1]) for c in coordinates if c[0]>=0 and c[1]>=0 ]

        return [cls.new_pipe(coordinate[0], coordinate[1], data[coordinate[1]][coordinate[0]]) for coordinate in coordinates if cls.is_pipe_symbol(data[coordinate[1]][coordinate[0]])]

class Vertical(Pipe):
    symbol = "|"

    def get_connecting_pipes(self, data):

        coordinates = [(self.x, self.y-1), (self.x, self.y+1)]

        return self.get_pipes(coordinates, data)



class Horizontal(Pipe):
    symbol = "-"

    def get_connecting_pipes(self, data):
        coordinates = [(self.x-1, self.y), (self.x+1, self.y)]
        return self.get_pipes(coordinates, data)

class L(Pipe):
    symbol = "L"

    def get_connecting_pipes(self, data):
        coordinates = [(self.x, self.y-1), (self.x+1, self.y)]
        return self.get_pipes(coordinates, data)
    
    def close_bend(self, start_bend:Pipe):
        if isinstance(start_bend, (J, Seven, F, L)):
            return True
        else:
            return False
        
    def s_bend(self, start_bend:Pipe):
        if isinstance(start_bend, Seven):
            return True
        else:
            return False


class J(Pipe):
    symbol = "J"

    def get_connecting_pipes(self, data):
        coordinates = [(self.x, self.y-1), (self.x-1, self.y)]
        return self.get_pipes(coordinates, data)
    
    def close_bend(self, start_bend:Pipe):
        if isinstance(start_bend, (J, Seven, F, L)):
            return True
        else:
            return False
        
    def s_bend(self, start_bend:Pipe):
        if isinstance(start_bend, F):
            return True
        else:
            return False


class Seven(Pipe):
    symbol = "7"

    def get_connecting_pipes(self, data):
        coordinates = [(self.x, self.y+1), (self.x-1, self.y)]
        return self.get_pipes(coordinates, data)
    
    def close_bend(self, start_bend:Pipe):
        if isinstance(start_bend, (J, Seven, F, L)):
            return True
        else:
            return False
        
    def s_bend(self, start_bend:Pipe):
        if isinstance(start_bend, L):
            return True
        else:
            return False

class F(Pipe):
    symbol = "F"

    def get_connecting_pipes(self, data):
        coordinates = [(self.x, self.y+1), (self.x+1, self.y)]
        return self.get_pipes(coordinates, data)

    def close_bend(self, start_bend:Pipe):
        if isinstance(start_bend, (J, Seven, F, L)):
            return True
        else:
            return False
        
    def s_bend(self, start_bend:Pipe):
        if isinstance(start_bend, J):
            return True
        else:
            return False

class Start(Pipe):
    symbol = "S"

    def get_connecting_pipes(self, data):

        coordinates = [(self.x, self.y-1), (self.x-1, self.y), (self.x, self.y+1), (self.x+1, self.y)]

        possible_pipes = self.get_pipes(coordinates, data)

        pipes = [pipe for pipe in possible_pipes if self.symbol in [p.symbol for p in pipe.get_connecting_pipes(data)]]

        return pipes
    
    def get_pipe_type(self, data):

        pipes = self.get_connecting_pipes(data)

        assert len(pipes) == 2

        count = Counter([pipe.symbol for pipe in pipes])

        if count["|"] == 2:
            return Vertical(self.x, self.y)
        elif count["-"] == 2:
            return Horizontal(self.x, self.y)
        else:
            H = pipes[0] if pipes[0].symbol=="-" else pipes[1]
            V = pipes[0] if pipes[0].symbol=="|" else pipes[1]
            if H.x > self.x:
                # can only be F or L
                if V.y > self.y:
                    return F(self.x, self.y)
                else:
                    return L(self.x, self.y)
                
            else:
                # can only be J or 7 
                if V.y > self.y:
                    return Seven(self.x, self.y)
                else:
                    return J(self.x, self.Y)

    

# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.


class Dir(Enum):
    Vert = 0
    Hor = 1

def check_enclosed(x, y, pipes, extent_x, extent_y):

    if ((check_line(range(0, x), [y], pipes, Dir.Hor) and
        check_line(range(x+1, extent_x), [y], pipes, Dir.Hor)) or
        (check_line([x], range(0, y), pipes, Dir.Vert) and
        check_line([x], range(y+1, extent_y), pipes, Dir.Vert))):

        print(f"Enclosed point at ({x}, {y})")
        return True

    return False

def check_line(x_range, y_range, pipes, dir):

    enclosing_pipes = []
    count = 0
    start_bend = False
    bend_type = None

    for xi in x_range:
        for yi in y_range:
            if (xi, yi) in pipes.keys():
                #enclosing_pipes.append(pipes[(xi, yi)])
                pipe = pipes[(xi, yi)]
                             
                if dir == Dir.Hor and isinstance(pipe, Vertical):
                    count += 1
                elif dir == Dir.Vert and isinstance(pipe, Horizontal):
                    count += 1

                elif isinstance(pipe, (L, J, F, Seven)):
                    if not start_bend:
                        start_bend = True
                        bend_type = pipe

                    else:
                        if pipe.close_bend(bend_type):
                            start_bend = False
                            if pipe.s_bend(bend_type):
                                count += 1


    if count%2 == 1:
        return True

    return False

def part_1(data):

    # find the start

    visited = {}

    for y, row in enumerate(data):
        for x, s in enumerate(row):
            if s=="S":
                start = Start(x, y)
                visited[(x, y)] = start

    to_check = [start.get_pipe_type(data)]
    print(to_check)
    new = []
    step = 0

    while True:
        for pipe in to_check:
            pipes = pipe.get_connecting_pipes(data)

            for pipe in pipes:
                if (pipe.x, pipe.y) not in visited.keys():
                    visited[(pipe.x, pipe.y)] = pipe
                    new.append(pipe)

        if len(new) == 0:
            break
        else:
            step += 1
            to_check = new
            new = []

    return step, visited


def part_2(data):

    length, pipes = part_1(data)

    enclosed = 0

    extents_y = len(data)
    extents_x = len(data[0])
    
    vis_data = deepcopy(data)

    for y, row in enumerate(data):
        for x, s in enumerate(row):
            if (x, y) not in pipes.keys():
                if check_enclosed(x, y, pipes, extents_x, extents_y):
                    enclosed += 1
                    vis_data[y] =  vis_data[y][:x] + "I" + vis_data[y][x + 1:]

    for row in vis_data:
        print(row)

    return enclosed

if __name__ == "__main__":

    DAY = "10"
    data = read_text_file(f"{DAY}.txt")
    print(part_1(data)[0])
    print(part_2(data))