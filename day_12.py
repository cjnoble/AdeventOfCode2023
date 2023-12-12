import re
import threading
import concurrent.futures
from functools import cache
from datetime import datetime

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data

def gen_allowable_combinations(string:str, allowable):

    springs_given = string.count("#")
    max_springs = sum(allowable)
    possible_springs = max_springs - springs_given

    if "?" not in string:
        return [string]
    
    combos = [""]

    for char_i, char in enumerate(string):
        if char == "?":
            upcoming = string[char_i+1:]
            new_combos_1 = [cur + "#" for cur in combos if cur.count("#") + upcoming.count("#") < max_springs]
            new_combos_2 = [cur + "." for cur in combos]

            new_combos_1 = [combo for combo in new_combos_1 if test_string_incomplete(combo, allowable)]
            new_combos_2 = [combo for combo in new_combos_2 if test_string_incomplete(combo, allowable)]

            combos = new_combos_1
            combos.extend(new_combos_2)

            #combos = [combo for combo in combos if test_string_incomplete(combo, allowable)]
            #print(combos)

        else:
            combos = [cur + char for cur in combos]

            if char == ".":
                valid = []
                for combo in combos:
                    if test_string(combo, allowable):
                        valid.append(combo)
                #print(valid)
                combos = valid
            else:
                combos = [combo for combo in combos if test_string_incomplete(combo, allowable)]
            
            #combos = [combo for combo in combos ]

    return combos

@cache
def num_allowable_combinations(string:str, allowable):

    springs_given = string.count("#")
    max_springs = sum(allowable)
    possible_springs = max_springs - springs_given

    if "?" not in string:
        return 1 if test_string(string, allowable) else 0
    
    combos = [""]
    extra = 0

    for char_i, char in enumerate(string):
        if char == "?":
            upcoming = string[char_i+1:]
            new_combos_1 = [cur + "#" for cur in combos if cur.count("#") + upcoming.count("#") < max_springs]
            new_combos_2 = [cur + "." for cur in combos]

            new_combos_1 = [combo for combo in new_combos_1 if test_string_incomplete(combo, allowable)]
            new_combos_2 = [combo for combo in new_combos_2 if test_string_incomplete(combo, allowable)]

            #combos = new_combos_1
            #combos.extend(new_combos_2)

            #combos = [combo for combo in combos if test_string_incomplete(combo, allowable)]
            #print(combos)

            if len(upcoming) > 0:
                combos = new_combos_1
                extra += sum([num_allowable_combinations(string[char_i+1:], get_remaining_allowable(combo, allowable)) for combo in new_combos_2])
            else:
                combos = new_combos_1
                combos.extend(new_combos_2)
                combos = [combo for combo in combos if test_string(combo, allowable)]
            #print(combos)

        else:
            combos = [cur + char for cur in combos]

            if char == ".":
                combos = [combo for combo in combos if test_string_incomplete(combo, allowable)]
                return sum([num_allowable_combinations(string[char_i+1:], get_remaining_allowable(combo, allowable)) for combo in combos]) + extra

            else:
                combos = [combo for combo in combos if test_string_incomplete(combo, allowable)]
            
        if char_i == len(string) - 1:
            combos = [combo for combo in combos if test_string(combo, allowable)]

    return len(combos) + extra

def possible_combinations(string):

    if "?" not in string:
        return [string]
    
    combos = [""]


    for char in string:
        

        if char == "?":

            new_combos_1 = [cur + "#" for cur in combos]
            new_combos_2 = [cur + "." for cur in combos]

            combos = new_combos_1
            combos.extend(new_combos_2)

        else:
            combos = [cur + char for cur in combos]

    return combos

def test_string_full(string, allowable):

    springs = re.findall("[#]+",string)

    if len(springs) != len(allowable):
        return False

    return test_string(string, allowable)


def test_string(string, allowable):
    springs = re.findall("[#]+",string)

    if len(springs) != len(allowable):
        return False

    for spring, num, in zip(springs, allowable):
        if len(spring) != num:
            return False
    
    return True


def test_string_incomplete(string, allowable):
    '''
    Always return true on the last set of ### if they are at the end of the string, as it may become valid later
    '''
    springs = re.findall("[#]+",string)
    for i, (spring, num) in enumerate(zip(springs, allowable)):
        if i == len(springs) - 1 and string[-1] == "#":
            if len(spring) > num:
                return False
            return True
        elif len(spring) != num:
            return False
    
    return True

def get_remaining_allowable(string, allowable):
    '''
    Get remaining allowable on a complete string
    '''
    if string[-1] != ".":
        raise Exception("Only use if last element is a dot")
    springs = re.findall("[#]+",string)

    assert test_string_incomplete(string, allowable) == True

    return allowable[len(springs):]

def part_1(data):

    total_combos = 0

    for line in data:
        springs, record = line.split(" ")
        record = [int(i) for i in record.split(",")]

        combos = possible_combinations(springs)

        num_combos = sum([test_string_full(combo, record) for combo in combos])

        total_combos += num_combos

        print(springs, record, num_combos)

    return total_combos 

def part_1_optimum(data):

    total_combos = 0

    for number, line in enumerate(data):
        springs, record = line.split(" ")
        record = tuple(int(i) for i in record.split(","))

        #combos = possible_combinations(springs)

        num_combos = num_allowable_combinations(springs, record)
        print(f"{number}: {springs}, {record}, {num_combos}")

        total_combos += num_combos

        print(springs, record, num_combos)

    return total_combos


def part_1_compare(data):

    for number, line in enumerate(data):
        springs, record = line.split(" ")
        record = tuple(int(i) for i in record.split(","))

        combos = possible_combinations(springs)
        num_combos_m1 = sum([test_string_full(combo, record) for combo in combos])

        num_combos_m2 = num_allowable_combinations(springs, record)

        if num_combos_m2 != num_combos_m1:
            print(f"{number}: {springs}, {record}, {num_combos_m1} {num_combos_m2}")

        assert num_combos_m1 == num_combos_m2

    return

def part_2_nonconcurrent(data):

    total_combos = 0
    # executor = concurrent.futures.ProcessPoolExecutor(61)
    # futures = [executor.submit(combos_for_line, line, i) for i, line in enumerate(data)]
    # concurrent.futures.wait(futures)

    # total_combos = sum([f.result() for f in futures])

    for i, line in enumerate(data):

        num_combos = combos_for_line(line, i)
        total_combos += num_combos

    return total_combos 

def part_2(data):

    total_combos = 0
    executor = concurrent.futures.ProcessPoolExecutor(61)
    futures = [executor.submit(combos_for_line, line, i) for i, line in enumerate(data)]
    concurrent.futures.wait(futures)

    total_combos = sum([f.result() for f in futures])

    # for line in data:

    #     springs, record, num_combos = combos_for_line(line)
    #     total_combos += num_combos

    #     print(springs, record, num_combos)

    return total_combos 

def combos_for_line(line, number):
    springs, record = line.split(" ")
    record = [int(i) for i in record.split(",")]

    springs = "?".join([springs for s in range(5)])
    record = [record for r in range(5)]
    record = tuple(r for sub in record for r in sub)

    #combos = gen_allowable_combinations(springs, record)

    #num_combos = sum([test_string_full(combo, record) for combo in combos])
    num_combos = num_allowable_combinations(springs, record)
    print(f"{number}: {springs}, {record}, {num_combos}")

    return num_combos



if __name__ == "__main__":

    DAY = "12"
    data = read_text_file(f"{DAY}.txt")
    start_p1 = datetime.now()
    print(f"Answer part 1: {part_1_optimum(data)}, answer in {datetime.now() - start_p1}")
    start_p2 = datetime.now()
    print(f"Answer part 2: {part_2(data)}, answer in {datetime.now() - start_p2}")
    print(f"Total time {datetime.now() - start_p1}")