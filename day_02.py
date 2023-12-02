import re

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


def getID (row):
    match = re.search(r"Game (\d+)", row)
    ID = match[1]
    return int(ID)

def parse_go_data(data, colours):

    goData = data.split(":")[-1]
    goData = goData.split(";")
    
    goData = [balls.split(",") for balls in goData]

    goData = [{re.search(rf"(\d+) ({colours})", ball)[2] :int(re.search(rf"(\d+) ({colours})", ball)[1]) for ball in balls} for balls in goData]

    return goData

def test_row(row):
    max_ball = {"red": 12, "green": 13, "blue": 14}
    colours = "|".join(max_ball.keys())

    #12 red cubes, 13 green cubes, and 14 blue cubes

    goData = parse_go_data(row, colours)

    for colour in max_ball.keys():
        for balls in goData:
            count = balls[colour] if colour in balls.keys() else 0
            if count > max_ball[colour]:
                return False
    
    return True

def power_row(row):
    colours = ["red", "green", "blue"]

    #12 red cubes, 13 green cubes, and 14 blue cubes

    goData = parse_go_data(row, "|".join(colours))

    power = 1

    for colour in colours:
        max = 0
        for balls in goData:
            count = balls[colour] if colour in balls.keys() else 0
            if count > max:
                max = count
        
        power *= max

    return power

def part_1(data):

    sum = 0

    for row in data:  
        if test_row(row):
            sum += getID(row)

    return sum

def part_2(data):

    sum = 0

    for row in data:  
        sum += power_row(row)

    return sum

if __name__ == "__main__":

    data = read_text_file("02.txt")
    print(part_1(data))
    print(part_2(data))