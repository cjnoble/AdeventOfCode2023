import re

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


def calibration_value(line):

    digits = re.findall("\d" ,line)
    return int(digits[0] + digits[-1])


def is_digit(d):

    if d in [str(i) for i in range(1, 10)]:
        return True
    return False

def calibration_value_simple(line):

    digits = []

    for letter in line:
        if check_digit(letter):
            digits.append(letter)

    return int(digits[0] + digits[-1])

def check_digit(digit):

    digit_lookup = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}

    return digit_lookup[digit] if digit in digit_lookup.keys() else digit


def calibration_value_2(line):

    allowed_digits = ["\d", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    allowed_digits = "|".join(allowed_digits)
    digits = re.findall(f"(?=({allowed_digits}))", line)
    return int(check_digit(digits[0]) + check_digit(digits[-1]))

def part_1(data):

    return sum([calibration_value(line) for line in data])

def part_2(data):

    return sum([calibration_value_2(line) for line in data])

if __name__ == "__main__":

    data = read_text_file("01.txt")
    print(part_1(data))
    print(part_2(data))