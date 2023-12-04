import re

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


def n_wins (wins, numbers):

    return sum([w in numbers for w in wins])


def parse_cards(data):

    data_out = {}

    for row in data:
        score = 0
        row = row.replace("  ", " ")
        card, numbers = row.split(":")

        card = int(re.search(r"Card +(\d+)", card)[1])

        win, numbers = numbers.split("|")

        win = [int(n) for n in win.strip().split(" ")]
        numbers = [int(n) for n in numbers.strip().split(" ")]

        data_out[int(card)] = {"card": int(card), "wins": win, "numbers": numbers}

    return data_out

def part_1(data):

    sum_score = 0

    for row in data:
        score = 0
        row = row.replace("  ", " ")
        card, numbers = row.split(":")
        win, numbers = numbers.split("|")

        win = [int(n) for n in win.strip().split(" ")]
        numbers = [int(n) for n in numbers.strip().split(" ")]

        for w in win:
            if w in numbers:
                if score == 0:
                    score = 1
                else:
                    score *= 2
        
        sum_score += score

    return sum_score

def part_2(data):

    data = parse_cards(data)

    for card in data.values():
        card["n_wins"] = n_wins(card["wins"], card["numbers"])
        card["new_cards"] = [card["card"] + i + 1 for i in range(card["n_wins"])]
        card["copies"] = 1

    for card in data.values():
        for new_card in card["new_cards"]:
            data[new_card]["copies"] += 1 * card["copies"]

    s = sum([card["copies"] for card in data.values()])

    return s

if __name__ == "__main__":

    DAY = "04"
    data = read_text_file(f"{DAY}.txt")
    print(part_1(data))
    print(part_2(data))