import re
from itertools import tee

class Range(object):
    def __init__(self, start, end) -> None:
        self.start = start
        self.end = end

class Seed(Range):
    def split(self, index):
        if index > self.start and index < self.end:
            return Seed(self.start, index), Seed(index, self.end) 
        else:
            return [self]

    def offset(self, off):
        self.start += off
        self.end += off

    def map_offset(self, maps):

        for map in maps:
            if self.start >= map.start and self.end <= map.end:
                self.offset(map.offset)
                break
            elif self.start < map.start and self.end > map.end:
                raise Exception("We fucked it up")

    def map(self, map):

        ranges = [self]

        for index in [map.start, map.end]:
            ranges = [r for range in ranges for r in range.split(index)]

        return ranges
    
    def __gt__(self, other):
        if self.start > other.start:
            return True
        else:
            return False
        
    def __lt__(self, other):
        if self.start < other.start:
            return True
        else:
            return False
        
    def __repr__(self) -> str:
        return f"Seed {self.start} {self.end}"
    

class Map(Range):
    def __init__(self, start, end, offset) -> None:
        self.offset = offset
        return super().__init__(start, end)


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


def pairs(iterable):

    iterable = iter(iterable)

    while True:

        try:
            a = next(iterable)
            b = next(iterable)
            yield a, b

        except StopIteration:
            break


def seed_solve(seeds, data):
    headings = [
        "seed-to-soil map:",
        "soil-to-fertilizer map:",
        "fertilizer-to-water map:",
        "water-to-light map:",
        "light-to-temperature map:",
        "temperature-to-humidity map:",
        "humidity-to-location map:"
    ]

    indexes = [data.index(heading) for heading in headings]
    indexes.append(len(data))

    source = seeds

    # for i,j in pairwise(indexes):
    #     lookup = {}
    #     for row in data[i+1: j-1]:
    #         destination_start, source_start, length = [int(i) for i in row.split()]

    #         lookup.update({source: destination for source, destination in zip(range(source_start, source_start + length) , range(destination_start, destination_start + length))})

    #     source = [lookup[s] if s in lookup.keys() else s for s in source]

    for i,j in pairwise(indexes):
  
        for s_index, s in enumerate(source):
            for row in data[i+1: j-1]:
                destination_start, source_start, length = [int(i) for i in row.split()]

                if s >= source_start and s < source_start + length:
                    source[s_index] += (destination_start - source_start)

    return source

def single_seed_solve(seed, data, current_min = 0):
    headings = [
        "seed-to-soil map:",
        "soil-to-fertilizer map:",
        "fertilizer-to-water map:",
        "water-to-light map:",
        "light-to-temperature map:",
        "temperature-to-humidity map:",
        "humidity-to-location map:"
    ]

    indexes = [data.index(heading) for heading in headings]
    indexes.append(len(data))

    source = seed

    for i,j in pairwise(indexes):
  
        for row in data[i+1: j-1]:
            destination_start, source_start, length = [int(i) for i in row.split()]

            if seed >= source_start and seed < source_start + length:
                source += (destination_start - source_start)

    if source > current_min:
        return current_min
    else:
        return source


def part_1(data):

    seeds = data[0]

    seeds = [int(s) for s in re.findall("\d+", seeds)]

    source = seed_solve(seeds, data)
                    
    return min(source)


def part_2_bruteforce(data):

    seeds = data[0]

    seeds = [int(s) for s in re.findall("\d+", seeds)]

    current_min = float("inf")

    for start, num in pairs(seeds):
        print(f"On set {start}, {num}")
        for seed in range(start, start + num):

            current_min = single_seed_solve(seed, data, current_min)
                    
    return current_min


def part_2(data):

    seeds = [int(s) for s in re.findall("\d+", data[0])]

    headings = [
        "seed-to-soil map:",
        "soil-to-fertilizer map:",
        "fertilizer-to-water map:",
        "water-to-light map:",
        "light-to-temperature map:",
        "temperature-to-humidity map:",
        "humidity-to-location map:"
    ]

    indexes = [data.index(heading) for heading in headings]
    indexes.append(len(data))

    seeds = [Seed(start, start+num) for start, num in pairs(seeds)]

    for i,j in pairwise(indexes):
        maps = []
        for row in data[i+1: j-1]:
            destination_start, source_start, length = [int(s) for s in row.split()]
            offset = destination_start - source_start
            source_end = source_start + length #end = up to but not including
            maps.append(Map(source_start, source_end, offset))
        
        pass

        for map in maps:
            seeds = [s for seed in seeds for s in seed.map(map)]
        
        for seed in seeds:
            seed.map_offset(maps)
    
        continue

    print(seeds)
    
    return min(seeds).start

if __name__ == "__main__":

    DAY = "05"
    data = read_text_file(f"{DAY}.txt")
    print(part_1(data))
    print(part_2(data))