import re
from enum import Enum
from collections import defaultdict

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data

class Pulse(Enum):
    Low = 0
    High = 1


class FlipFlop(object):
    prefix = "%"
    def __init__(self, output_modules:list):
        self.output = Pulse.Low
        self.output_modules = output_modules
        self.pulse_count = {Pulse.Low: 0, Pulse.High: 0}
    
    def update(self, input:Pulse):
        if input is Pulse.Low:
            if self.output == Pulse.Low:
                self.output = Pulse.High
            else: # Current output is high
                self.output = Pulse.Low
        
        self.pulse_count[self.output] += 1

class Conjunction (object):
    prefix = "&"
    def __init__(self, input_modules:list, output_modules:list):
        self.inputs = {input_module: Pulse.Low for input_module in input_modules}
        self.output = Pulse.Low
        self.output_modules = output_modules
        self.pulse_count = {Pulse.Low: 0, Pulse.High: 0}
    
    def update(self, input_module: str, input:Pulse):
        self.inputs[input_module] = input
        if Pulse.Low in self.inputs.values():
            self.output = Pulse.High
        else:
            self.output = Pulse.Low
        
        self.pulse_count[self.output] += 1

    @classmethod
    def from_string(cls, string):
        string = string.split("->")
        outputs = re.findall("([A-Za-z]+,*)", string[1])
        return cls(outputs)

class Broadcaster(object):
    def __init__(self, output_modules:list):
        self.output = Pulse.Low
        self.output_modules = output_modules
        self.pulse_count = {Pulse.Low: 0, Pulse.High: 0}

    def update(self, input:Pulse):
        self.output = input
        self.pulse_count[self.output] += 1


class Button(object):
    def __init__(self, output_modules:list):
        self.output = Pulse.Low
        self.output_modules = output_modules
        self.pulse_count = {Pulse.Low: 0, Pulse.High: 0}

    def update(self):
        self.output = Pulse.Low
        self.pulse_count[self.output] += 1

def part_1(data, button_presses):

    return

def part_2(data):

    return

if __name__ == "__main__":

    DAY = "20"
    data = read_text_file(f"{DAY}.txt")
    print(part_1(data))
    print(part_2(data))