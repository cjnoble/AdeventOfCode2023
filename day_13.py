import re
from itertools import tee

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


def line_equal(line_1, line_2):

    for l1, l2 in zip(line_1, line_2):
        if l1 != l2:
            return False
    return True


def line_equal_smudged(line_1, line_2):

    smudges = 0

    for l1, l2 in zip(line_1, line_2):
        if l1 != l2:
            smudges += 1
        if smudges > 1:
            return False
    if smudges == 1:
        return True
    else:
        return False

def get_mirror_row(pattern):


    x1 = 0 #Check for any mirror including the first line
    for x2 in range(x1+1, len(pattern)):
        while x2 > x1:
            if line_equal(pattern[x1], pattern[x2]):
                if x1+1 == x2:
                    # This means we found the mirror
                    return x2
                x1 += 1
                x2 -= 1
            else:
                break

    #Now check for any pattern including the last line
    for x1 in range(len(pattern)):
        x2 = len(pattern) -1
        while x2 > x1:
            if line_equal(pattern[x1], pattern[x2]):
                if x1+1 == x2:
                    # This means we found the mirror
                    return x2
                x1 += 1
                x2 -= 1
            else:
                break
    return None


def smudge_check(pattern, x1, x2):
    smudges = 0
    while x2 > x1:
        equal = line_equal(pattern[x1], pattern[x2])
        equal_if_smudged = line_equal_smudged(pattern[x1], pattern[x2])

        if (not equal) and (equal_if_smudged):
        #if equal_if_smudged:
            smudges += 1

        if equal or equal_if_smudged:
            if x1+1 == x2 and smudges == 1:
                # This means we found the mirror
                return x2
            if smudges > 1:
                break
            x1 += 1
            x2 -= 1
        else:
            break
    return None

def get_mirror_row_smudged(pattern):

    x1 = 0 #Check for any mirror including the first line
    for x2 in range(x1+1, len(pattern)):
        check = smudge_check(pattern, x1, x2)
        if check:
            return check

    #Now check for any pattern including the last line
    for x1 in range(len(pattern)):
        x2 = len(pattern) -1
        check = smudge_check(pattern, x1, x2)
        if check:
            return check

    return None

def get_mirror_column(pattern):
    
    return get_mirror_row([column for column in zip(*pattern)])

def get_mirror_column_smudged(pattern):
    
    return get_mirror_row_smudged([column for column in zip(*pattern)])

def part_1(data):

    patterns = get_patterns(data)
    #print(patterns)

    total = 0

    for i, pattern in enumerate(patterns):
        mirror_row = get_mirror_row(pattern)
        #mirror_row = None

        mirror_column = get_mirror_column(pattern)

        if mirror_row:
            total += mirror_row*100
        elif mirror_column:
            total += mirror_column
        else:
            
            for row in pattern:
                print(row)

            raise Exception(f"No mirrors found for pattern {i}")

    return total

def part_2(data):

    patterns = get_patterns(data)
    #print(patterns)

    total = 0

    for i, pattern in enumerate(patterns):
        mirror_row = get_mirror_row_smudged(pattern)
        #mirror_row = None

        mirror_column = get_mirror_column_smudged(pattern)

        if mirror_row:
            total += mirror_row*100
        elif mirror_column:
            total += mirror_column
        else:
            
            for row in pattern:
                print(row)

            raise Exception(f"No mirrors found for pattern {i}")

    return total


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def get_patterns(data: list):

    patterns = [""]
    patterns.extend(data)
    patterns.append("")

    blank_lines = [i for i, line in enumerate(patterns) if line == ""]

    patterns = [patterns[i+1: j] for i, j in pairwise(blank_lines)]

    return patterns


if __name__ == "__main__":

    DAY = "13"
    data = read_text_file(f"{DAY}.txt")
    print(part_1(data))
    print(part_2(data))