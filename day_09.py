import re
from functools import reduce
from itertools import tee

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def all_zeros(data):

    return reduce(lambda x, y: x and y, [True if i == 0 else False for i in data])

def predict_next(data):

    if all_zeros(data):
        return 0
    
    next_row = [s1 - s0 for s0, s1 in pairwise(data)]

    return data[-1] + predict_next(next_row)

def predict_previous(data):

    if all_zeros(data):
        return 0
    
    next_row = [s1 - s0 for s0, s1 in pairwise(data)]

    return data[0] - predict_previous(next_row)

def part_1(data):

    s = 0

    for row in data:
        row = [int(r) for r in row.split()]
        s +=  predict_next(row)

    return s

def part_2(data):

    s = 0

    for row in data:
        row = [int(r) for r in row.split()]
        s +=  predict_previous(row)

    return s

if __name__ == "__main__":

    DAY = "09"
    data = read_text_file(f"{DAY}.txt")
    print(part_1(data))
    print(part_2(data))