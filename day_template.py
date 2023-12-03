import re

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


def part_1(data):

    return

def part_2(data):

    return

if __name__ == "__main__":

    DAY = "02"
    data = read_text_file(f"{DAY}.txt")
    print(part_1(data))
    print(part_2(data))