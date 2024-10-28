import re
from collections import deque
from functools import cache

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


class Gardens(object):
    def __init__(self, data) -> None:
        self.data = data

    def find_start(self):

        for y, row in enumerate(self.data):
            for x, val in enumerate(row):
                if val == "S":
                    return x, y
                
        raise Exception("Start not found")

    def get_adjacent_points(self, point):

        x, y = point

        points = []

        if x-1 >= 0:
            points.append((x-1, y))
        if x+1 < len(self.data[y]):
            points.append((x+1, y))
        if y+1 < len(self.data):
            points.append((x, y+1))
        if y-1 >= 0:
            points.append((x, y-1))

        return points


    @cache
    def get_valid_next_points(self, point):
        next_points = []
        for next_point in self.get_adjacent_points(point):
            if self.data[next_point[1]][next_point[0]] != "#":
                next_points.append(next_point)
        return next_points


def visit_gardens(data, step_limit):
    data = Gardens(data)

    x_start, y_start = data.find_start()

    visited = set()
    queue = set()
    queue.add((x_start, y_start))

    for step in range(step_limit):
        new_queue = set()

        for point in queue:
            visited.add(point)

            new_queue.update(data.get_valid_next_points(point))

        queue = new_queue

    print(queue)

    return len(queue)

def part_1(data, step_limit):

    return visit_gardens(data, step_limit)

def part_2(data, step_limit):

    return visit_gardens(data, step_limit)


if __name__ == "__main__":

    DAY = "21"
    data = read_text_file(f"{DAY}.txt")
    print(part_1(data, 64))
    print(part_2(data, 26501365))