from __future__ import annotations
import re
from functools import reduce
from copy import deepcopy

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


class Galaxy(object):

    id = 1

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.ID = self.id
        Galaxy.next_id()

    @classmethod
    def next_id(cls):
        cls.id += 1

    def dist(self, other:Galaxy):
        return abs(self.x - other.x) + abs(self.y - other.y)


    def update(self, empty_rows, empty_columns, o):

        original_x = self.x
        original_y = self.y

        for row in empty_rows:
            if row < original_y:
                self.y += (o - 1)

        for column in empty_columns:
            if column < original_x:
                self.x += (o - 1)


    def __repr__(self) -> str:
        return f"Galaxy {self.ID} ({self.x}, {self.y})"


def is_empty(row):

    return reduce(lambda x, y: x and y, [True if s=="." else False for s in row ])    


def get_galaxies(data):

    #return {(x, y): Galaxy(x, y) for y, row in enumerate(data) for x, s in enumerate(row) if s == "#"}
    return [Galaxy(x, y) for y, row in enumerate(data) for x, s in enumerate(row) if s == "#"]


def combination_pairs(a_list):

    for i, item_1 in enumerate(a_list[:-1]):
        for item_2 in a_list[i+1:]:
            yield(item_1, item_2)


def get_dist_sum(galaxies, empty_rows, empty_columns, x):
    galaxies = deepcopy(galaxies)
    for galaxy in galaxies:
        galaxy.update(empty_rows, empty_columns, x)

    dist_sum = 0
    for g1, g2 in combination_pairs(galaxies):
        dist = g1.dist(g2)
        dist_sum += dist
        #print(f"Distance is {dist} between {g1} & {g2}")

    return dist_sum


def part_1(data):

    galaxies = get_galaxies(data)
    print(galaxies)

    #get indices of empty rows and columns
    empty_rows = [i for i, row in enumerate(data) if is_empty(row)]
    empty_columns = [i for i, column in enumerate(zip(*data)) if is_empty(column)]

    print(empty_rows)
    print(empty_columns)

    x = 2
    dist_sum = get_dist_sum(galaxies, empty_rows, empty_columns, x)

    return dist_sum

def part_2(data, expansion):

    galaxies = get_galaxies(data)
    empty_rows = [i for i, row in enumerate(data) if is_empty(row)]
    empty_columns = [i for i, column in enumerate(zip(*data)) if is_empty(column)]

    c = get_dist_sum(galaxies, empty_rows, empty_columns, 0)

    m = get_dist_sum(galaxies, empty_rows, empty_columns, 1) - c

    return c + m*expansion


if __name__ == "__main__":

    DAY = "11"
    data = read_text_file(f"{DAY}.txt")
    print(part_1(data))
    EXPANSION = 1000000
    print(part_2(data, EXPANSION))