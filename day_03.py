from collections import defaultdict
from functools import reduce

class Gear (object):

    def __init__(self, coords):
        self.coords = coords
        self.numbers = []
        self.count = 0

    def add_number(self, number):
        self.numbers.append(number)
        self.count += 1

    def get_gear_ratio(self):
        return reduce(lambda x, y: x*y, self.numbers)

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


def is_valid(data, row, start, length):

    row_0 = max(row - 1, 0)
    row_1 = min(row + 1, len(data)-1)
    col_0 = max(start-1, 0)
    col_1 = min(start+length, len(data[row_0])-1)

    for row in range (row_0, row_1+1):
        for col in range (col_0, col_1+1):
            if not (data[row][col].isnumeric() or data[row][col] == "."):
                return True

    return False

def get_gears(data, row, start, length):

    gears = []

    row_0 = max(row - 1, 0)
    row_1 = min(row + 1, len(data)-1)
    col_0 = max(start-1, 0)
    col_1 = min(start+length, len(data[row_0])-1)

    for row in range (row_0, row_1+1):
        for col in range (col_0, col_1+1):
            if data[row][col] == "*":
                gears.append((row, col))

    return gears

def part_1(data):

    valid_numbers = []

    for i, row in enumerate(data):
        row_iter = iter(row)
        j = 0

        while (x := next(row_iter, None)) is not None:
            if x.isnumeric():
                number = x
                start = j
                while (y := next(row_iter, None)) is not None and y.isnumeric():
                    number += y
                    j += 1
                j += 1
                
                if is_valid(data, i, start, len(number)):
                    valid_numbers.append(int(number))

            j += 1

    print(valid_numbers)

    return sum(valid_numbers)

def part_2(data):

    gears_dict = dict()

    valid_numbers = []

    for i, row in enumerate(data):
        row_iter = iter(row)
        j = 0

        while (x := next(row_iter, None)) is not None:
            if x.isnumeric():
                number = x
                start = j
                while (y := next(row_iter, None)) is not None and y.isnumeric():
                    number += y
                    j += 1
                j += 1
                
                if is_valid(data, i, start, len(number)):
                    n = int(number)
                    valid_numbers.append(n)
                    gears = get_gears(data, i, start, len(number))
                    for gear in gears:
                        if gear not in gears_dict.keys():
                            gears_dict[gear] = Gear(gear)
                        gears_dict[gear].add_number(n)


            j += 1

    sum = 0
    for gear in gears_dict.values():
        if gear.count == 2:
            sum += gear.get_gear_ratio()

    return sum

if __name__ == "__main__":

    DAY = "03"
    data = read_text_file(f"{DAY}.txt")
    print(part_1(data))
    print(part_2(data))