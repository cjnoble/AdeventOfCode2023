import re
from functools import cache
from copy import deepcopy
from collections import deque

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return [[i for i in row] for row in data]



def update(data, current_x, current_y, new_x, new_y):
    if data[new_y][new_x] == "#" or (data[new_y][new_x] == "O" and new_x!=current_x and new_y != current_y):
        raise Exception("Invalid position")
     
    data[current_y][current_x] = "."
    data[new_y][new_x] = "O"

    

def look_north(data, current_x, current_y):

    for target_y in range(current_y, 0, -1):
        if data[target_y - 1][current_x] != ".":
            return current_x, target_y
        
    return current_x, 0


def pprint_gird(data):
    print("\n")
    for row in data:
        print(row)

def tilt_north(data):
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == "O":
                new_x, new_y = look_north(data, x, y)
                update(data, x, y, new_x, new_y)


def get_load(data:list):
    data = deepcopy(data)
    load = 0
    data.reverse()
    for i, row in enumerate(data):
        for s in row:
            if s == "O":
                load += i+1

    return load


def rotate_grid(data):

    '''
    clockwise rotation
    '''

    # Transpose then flip the order
    data = [list(r) for r in zip(*data)]
    for r in data:
        r.reverse()

    return data


def part_1(data):

    tilt_north(data)
    load = get_load(data)

    return load

def part_2(data):

    seen_grids = {}

    CYCLES = 1000000000
    for i in range(CYCLES):
        data = one_cycle(data)
        load = get_load(data)

        if load in seen_grids.keys():
            for j, prev_grid in seen_grids[load]:

                if grid_compare(data, prev_grid):
                    # We found a loop
                    loop_length = i - j
                    print(i, loop_length)

                    if (CYCLES - i - 1)%loop_length == 0:
                        return load

        else:
             seen_grids[load] = deque()

        #seen_loads[load] = i
        seen_grids[load].appendleft((i, deepcopy(data)))
        if i%10000 == 0:
            print(f"On cycle {i}: current load {get_load(data)}")
    
    return get_load(data)

#@cache
def one_cycle(data):
    for i in range(4):
        tilt_north(data)
        data = rotate_grid(data)
    return data

def grid_compare(data, compare_data):

    for row1, row2 in zip(data, compare_data):
        for x1, x2 in zip(row1, row2):
            if x1 != x2:
                return False
    return True



if __name__ == "__main__":

    DAY = "14"
    data = read_text_file(f"{DAY}.txt")
    print(part_1(data))
    print(part_2(data))