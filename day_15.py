import re
from collections import deque, defaultdict


class Lense(object):
    def __init__(self, label, focal_length=0) -> None:
        self.label = label
        self.focal_length = focal_length


class Box(object):

    def __init__(self) -> None:
        self.slots = deque()
        self.contents = dict()

    def get_focusing_power(self, box_index):
        power = 0
        for slot, label in enumerate(self.slots):
            lense = self.contents[label]
            power += (1 + box_index)*(1 + slot)*lense.focal_length
        return power
    
    def in_box(self, lense):
        if lense.label in self.contents:
            return True
        return False
    
    def get_index(self, lense):
        return self.slots.index(lense.label)
    
    def add(self, lense):
        if self.in_box(lense):
            slot = self.get_index(lense)
            self.slots.remove(lense.label)
            self.slots.insert(slot, lense.label)
        else:
            self.slots.append(lense.label)
        self.contents[lense.label] = lense

    def remove(self, lense):
        if self.in_box(lense):
            slot = self.get_index(lense)
            self.slots.remove(lense.label)
            del self.contents[lense.label]
      

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data

def hash(string):

    cur_val = 0

    for char in string:
        cur_val += ord(char)
        cur_val *= 17
        cur_val = cur_val%256

    return cur_val


def part_1(data):

    data = data[0].split(",")

    return sum([hash(string) for string in data])

def part_2(data):

    data = data[0].split(",")
    boxes = defaultdict(lambda: Box())

    for instruction in data:
        match = re.search(("([A-Za-z]+)([=-])(\d*)"), instruction)
        if match is None:
            raise Exception(f"No match found for string {instruction}")
        label = match[1]
        operator = match[2]
        box = hash(label)
        if operator == "-":
            boxes[box].remove(Lense(label))
        elif operator == "=":
            focal_length = int(match[3])
            boxes[box].add(Lense(label, focal_length))

        else:
            raise Exception(f"Unknown instruct{operator}")

    total = sum([boxes[box].get_focusing_power(box) for box in range(256)])

    return total

if __name__ == "__main__":

    DAY = "15"
    data = read_text_file(f"{DAY}.txt")
    print(part_1(data))
    print(part_2(data))