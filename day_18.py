import re
from collections import namedtuple, deque
from random import randint
from PIL import Image
from itertools import tee

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


class Point(object):

    def __init__(self, x, y, colour=None) -> None:
        self.x = x
        self.y = y
        self.colour = colour

    @classmethod
    def from_direction(cls, direction, previous):

        'direction.Dist'

        if direction.Direct == "U":
            return [cls(previous.x, previous.y - i) for i in range (1, direction.Dist+1)]
        elif direction.Direct == "D":
            return [cls(previous.x, previous.y + i) for i in range (1, direction.Dist+1)]
        elif direction.Direct == "L":
            return [cls(previous.x - i, previous.y) for i in range (1, direction.Dist+1)]
        else:
            return [cls(previous.x + i, previous.y) for i in range (1, direction.Dist+1)]

    def next_vertex_from_direction(self, direction):

        'direction.Dist'
        dist = direction.Dist

        if direction.Direct == "U":
            return Point(self.x, self.y - dist)
        elif direction.Direct == "D":
            return Point(self.x, self.y + dist)
        elif direction.Direct == "L":
            return Point(self.x - dist, self.y)
        else:
            return Point(self.x + dist, self.y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}): {self.colour}"

    def __hash__(self) -> int:
        
        return hash((self.x, self.y))

    def __eq__(self, other: object) -> bool:
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False
        
    def __neq__(self, other):
        return not self == other
    
    def get_connected_points(self, points, interior_point):

        possible_points = [Point(self.x + x, self.y + y) for x in [-1, 0, 1] for y in [-1, 0, 1]]
        possible_points = [p for p in possible_points if p.x != self.x or p.y != self.y]

        if self not in points:
            return possible_points
        else:
            return [p for p in possible_points if p in points]


def parse_input(data):

    direction = namedtuple("direction", ["Direct", "Dist", "Colour"])
    directions = []

    for line in data:

        match = re.search(r"([URLD]) (\d+) \((#[0-9a-fA-F]+)\)", line) # 
        print(match[1], match[2], match[3])
        directions.append(direction(match[1], int(match[2]), match[3]))

    return directions

def parse_input_2(data):

    direction = namedtuple("direction", ["Direct", "Dist"])
    directions = []

    directions_dict = {"0":  "R", "1": "D", "2": "L", "3": "U"}

    for line in data:

        match = re.search(r"\((#[0-9a-fA-F]+)\)", line) # 
        
        directions.append(direction(directions_dict[match[1][-1]], int("0x" + match[1][1:6], 0)))

    return directions

def part_1(data):

    directions = parse_input(data)

    points = [Point(0, 0, None)]

    for i, direction in enumerate(directions):
        previous = points[-1]

        points.extend(Point.from_direction(direction, previous))
        #print(direction)
        #vis_points(points)

    perimeter = len(set(points))

    print(perimeter)

    max_x = max(points, key=lambda p: p.x).x
    max_y = max(points, key=lambda p: p.y).y
    min_x = min(points, key=lambda p: p.x).x
    min_y = min(points, key=lambda p: p.y).y

    start_point = Point((min_x + max_x)//2, (min_y + max_y)//2) ## We assume this is inside...
    print(start_point)
    area, visited = flood_fill(points, start_point)
    vis_points_image(visited, points)

    return area

def flood_fill(points, start_point:Point):

    max_x = max(points, key=lambda p: p.x).x
    max_y = max(points, key=lambda p: p.y).y
    min_x = min(points, key=lambda p: p.x).x
    min_y = min(points, key=lambda p: p.y).y

    queue = deque([start_point])
    visited = set([start_point])
    area = 1

    while queue:
        next = queue.popleft()
        visited.add(next)
        if next.x == -1:
            print("")
        
        for point in next.get_connected_points(points, start_point):

            if point.x > max_x or point.x < min_x or point.y > max_y or point.y < min_y:
                raise Exception("Exceeded possible point range: something has gone wrong") 

            if point not in queue and point not in visited:
                area += 1
                queue.append(point)

    [visited.add(p) for p in points]
    vis_points(visited)
    

    return area, visited

def vis_points(points):

    max_x = max(points, key=lambda p: p.x).x
    max_y = max(points, key=lambda p: p.y).y
    min_x = min(points, key=lambda p: p.x).x
    min_y = min(points, key=lambda p: p.y).y

    data_vis = [["." for i in range(min_x, max_x+1)] for j in range(min_y, max_y+1)]
    for point in points:
        try:
            data_vis[point.y-min_y][point.x-min_x] = "#"
        except IndexError as e:
            print(point)
            raise e


    for row in data_vis:
        print(row)

def vis_points_image(points, perimeter_points):

    max_x = max(points, key=lambda p: p.x).x
    max_y = max(points, key=lambda p: p.y).y
    min_x = min(points, key=lambda p: p.x).x
    min_y = min(points, key=lambda p: p.y).y

    pixel = [(0, 255, 0) if x==0 and y==0 else (0, 0, 255) if Point(x, y) in perimeter_points else (255,0,0) if Point(x, y) in points else (0, 0, 0) for y in range(min_y, max_y+1) for x in range(min_x, max_x+1) ]

    img = Image.new('RGB',((max_x + 1) - min_x, (max_y + 1) - min_y))

    img.putdata(pixel) 
    img.show()

def get_missing_area(directions):
    directions.append(directions[0])

    area = 0

    for direction_1, direction_2 in pairwise(directions):
        area += (0.5 * (direction_1.Dist + 0.5 if is_anticlockwise(direction_1, direction_2) else direction_1.Dist-0.5))
    
    return area

def is_anticlockwise(direct_1, direct_2):

    anticlockwise = {"L": "U", "U": "R", "R": "D", "D": "L"}

    if  anticlockwise[direct_1.Direct] == direct_2.Direct:
        return True
    return False

def part_2(data):

    directions = parse_input_2(data)
    

    points = [Point(0, 0, None)]
    area = 0

    for direction in directions:
        previous = points[-1]

        next = previous.next_vertex_from_direction(direction)
        points.append(next)

        area += (next.x*previous.y - next.y*previous.x)

    area = abs(area/2)

    area += get_missing_area(directions)

    return area

if __name__ == "__main__":

    DAY = "18"
    data = read_text_file(f"{DAY}.txt")
    #print(part_1(data))
    print(part_2(data))