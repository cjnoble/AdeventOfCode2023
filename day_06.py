import re
from math import sqrt, ceil, floor

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


def part_1(data):

    time, dist = data

    time = [int(t) for t in re.findall(r"\d+", time)]
    dist = [int(d) for d in re.findall(r"\d+", dist)]

    n = 1

    for t, d in zip(time, dist):
        tmax = ceil((t + sqrt(t**2 - 4*d))/2) - 1
        tmin = floor((t - sqrt(t**2 - 4*d))/2) + 1

        print(tmax, tmin)
        n *= 1 + tmax - tmin


    return n


def part_2(data):

    time, dist = data

    time = re.findall(r"\d+", time)
    time = int("".join(time))
    dist = re.findall(r"\d+", dist)
    dist = int("".join(dist))

    n = 1

    tmax = ceil((time + sqrt(time**2 - 4*dist))/2) - 1
    tmin = floor((time - sqrt(time**2 - 4*dist))/2) + 1

    print(tmax, tmin)
    n *= 1 + tmax - tmin

    return n

if __name__ == "__main__":

    DAY = "06"
    data = read_text_file(f"{DAY}.txt")
    print(part_1(data))
    print(part_2(data))