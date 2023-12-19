import re
from collections import deque
from copy import copy

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


class Rule(object):

    def __init__(self, name, rule_list_str) -> None:
        self.name = name
        self.rule_list_str = rule_list_str


    def check_rule(self, part):
        rules = deque(self.rule_list_str)

        while rules:
            rule = rules.popleft()

            match = re.search(r"([xmas])([<>])(\d+):([A-Za-z]+)", rule)

            if match:
                prop = match[1]
                check_type = match[2]
                lim = int(match[3])

                next = match[4]

                cur_val = getattr(part, prop)
                if check_type == "<":
                    if cur_val < lim:
                        pass
                    else:
                        continue

                elif check_type == ">":
                    if cur_val > lim:
                        pass
                    else:
                        continue

            else:
                next = rule

            if next == "A":
                part.accepted = True
                return
            elif next == "R":
                part.rejected = True
                return
            else:
                return next

class Part(object):

    def __init__(self, x, m , a, s) -> None:
        self.accepted = False
        self.rejected = False
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    @classmethod
    def from_string(cls, part_string):
        x = int(re.search("x=(\d+)", part_string)[1])
        m = int(re.search("m=(\d+)", part_string)[1])
        a = int(re.search("a=(\d+)", part_string)[1])
        s = int(re.search("s=(\d+)", part_string)[1])

        return cls(x, m, a, s)
    
    @property
    def rating(self):
        return sum([self.x, self.m, self.a, self.s])


class Possible_Part(object):
    def __init__(self, min_val = 1, max_val=4000) -> None:
        # Max val is inclusive
        self.accepted = False
        self.rejected = False
        self.next_rule = "in"
        self.min_x = min_val
        self.max_x = max_val
        self.min_m = min_val
        self.max_m = max_val
        self.min_a = min_val
        self.max_a = max_val
        self.min_s = min_val
        self.max_s = max_val

    def apply_rule(self, rules):


        rules = deque(rules)

        while rules:

            rule_str = rules.popleft()

            match = re.search(r"([xmas])([<>])(\d+):([A-Za-z]+)", rule_str)

            if match:
                prop = match[1]
                check_type = match[2]
                lim = int(match[3])

                next = match[4]

                currnt_max = getattr(self, f"max_{prop}")
                currnt_min = getattr(self, f"min_{prop}")
                
                if check_type == "<":
                    if currnt_max < lim:
                        self.get_next_rule(next)
                        return [self]
                    elif currnt_min > lim:
                        continue
                    else:
                        new_part_1 = copy(self)
                        setattr(new_part_1, f"max_{prop}", lim-1)
                        new_part_1.get_next_rule(next)
                        new_part_2 = copy(self)
                        setattr(new_part_2, f"min_{prop}", lim)
                        new_part_2 = new_part_2.apply_rule(rules)
                        return new_part_1, *new_part_2

                elif check_type == ">":
                    if currnt_max < lim:
                        self.get_next_rule(next)
                        return [self]
                    elif currnt_min > lim:
                        continue
                    else:
                        new_part_1 = copy(self)
                        setattr(new_part_1, f"min_{prop}", lim+1)
                        new_part_1.get_next_rule(next)
                        new_part_2 = copy(self)
                        setattr(new_part_2, f"max_{prop}", lim)
                        new_part_2 = new_part_2.apply_rule(rules)
                        return new_part_1, *new_part_2

            else:
                self.get_next_rule(rule_str)
                return [self]

    def get_next_rule(self, next):
        if next == "A":
            self.accepted = True
            return
        elif next == "R":
            self.rejected = True
            return
        else:
            self.next_rule = next
            return
        
    @property
    def combos(self):
        return (1 + self.max_x - self.min_x) * (1 + self.max_m - self.min_m) * (1 + self.max_a - self.min_a) * (1 + self.max_s - self.min_s)

def parse_data(data):

    rules = {}
    parts = []

    for row in data:
        match = re.search(r"([A-Za-z]+){(.*)}", row)
        if match:
            name = match[1]
            rule = match[2].split(",")
            print(match[1], match[2])
            rules[name] = Rule(name, rule)

        else:
            if len(row) > 0:
                parts.append(Part.from_string(row))

    return parts, rules


def part_1(data):

    parts, rules = parse_data(data)

    for part in parts:
        rule_str = "in"
        while part.accepted is False and part.rejected is False:

            rule = rules[rule_str]

            rule_str = rule.check_rule(part)
            print(rule_str)

    return sum([part.rating for part in parts if part.accepted])

def part_2(data):

    _, rules = parse_data(data)

    parts = deque([Possible_Part()])
    solved_parts = []

    while parts:

        part = parts.popleft()

        if part.accepted is True or part.rejected is True:
            solved_parts.append(part)
        else:

            rule_str = part.next_rule
   

            rule = rules[rule_str]

            next_parts = part.apply_rule(rule.rule_list_str)
            if sum(p.combos for p in next_parts) != part.combos:
                print("lost combos")
                raise Exception("Lost combos")
            if next_parts:
                parts.extend(next_parts)

    print(f"Starting parts combos {Possible_Part().combos}")
    print(f"Accepted combos {sum([part.combos for part in solved_parts if part.accepted])}")
    print(f"Rejected combos {sum([part.combos for part in solved_parts if part.rejected])}")
    print(f"Accepted + rejected combos {sum([part.combos for part in solved_parts if part.accepted]) + sum([part.combos for part in solved_parts if part.rejected])}")

    return sum([part.combos for part in solved_parts if part.accepted])


if __name__ == "__main__":

    DAY = "19"
    data = read_text_file(f"{DAY}.txt")
    print(part_1(data))
    print(part_2(data))