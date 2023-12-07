import re
from collections import Counter


class Hand(object):
    CARD_RANKING = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

    def __init__(self, hand, bid) -> None:
        self.hand = hand
        self.bid = bid

    @classmethod
    def from_str(cls, str):
        hand, bid = str.split(" ")
        return cls(hand, int(bid))

    def hand_type(self):
        counter = Counter(self.hand)

        counts = list(counter.values())
        counts.sort(reverse=True)

        if counts[0] == 5:
            return 6
        elif counts[0] == 4:
            return 5
        elif counts[0] == 3 and counts[1] == 2:
            return 4
        elif counts[0] == 3:
            return 3
        elif counts[0] == 2 and counts[1] == 2:
            return 2
        elif counts[0] == 2:
            return 1
        else:
            return 0

    def __gt__(self, other):

        if self.hand_type() > other.hand_type():
            return True
        elif self.hand_type() == other.hand_type():
            for l1, l2 in zip(self.hand, other.hand):
                if self.CARD_RANKING.index(l1) < self.CARD_RANKING.index(l2):
                    return True
                elif self.CARD_RANKING.index(l1) > self.CARD_RANKING.index(l2):
                    return False
            raise Exception("Identical hand")
        else:
            return False
        
    def __lt__ (self, other):
        return not self > other
    
    def __repr__(self) -> str:
        return f"{self.hand}, {self.bid}, {self.hand_type()}"
    
class WildHand(Hand):
    CARD_RANKING = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]

    def hand_type(self):
        counter = Counter(self.hand)

        wild_count = counter["J"]
        del counter["J"]

        counts = list(counter.values())
        counts.sort(reverse=True)

        if wild_count == 5 or counts[0] == 5 or counts[0] + wild_count == 5:
            return 6
        elif counts[0] == 4 or counts[0] + wild_count == 4:
            return 5
        elif (counts[0] == 3 or counts[0] + wild_count == 3) and counts[1] == 2:
            return 4
        elif counts[0] == 3 or counts[0] + wild_count == 3:
            return 3
        elif (counts[0] == 2 or counts[0] + wild_count == 2) and counts[1] == 2:
            return 2
        elif counts[0] == 2 or counts[0] + wild_count == 2:
            return 1
        else:
            return 0

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


def part_1(data):

    hands = [Hand.from_str(row) for row in data ]
    hands.sort()

    for hand in hands:
        print(hand)

    s = 0

    for i, hand in enumerate(hands):
        s += (i + 1)*hand.bid

    return s

def part_2(data):

    hands = [WildHand.from_str(row) for row in data ]
    hands.sort()

    for hand in hands:
        print(hand)

    s = 0

    for i, hand in enumerate(hands):
        s += (i + 1)*hand.bid

    return s

if __name__ == "__main__":

    DAY = "07"
    data = read_text_file(f"{DAY}.txt")
    print(part_1(data))
    print(part_2(data))