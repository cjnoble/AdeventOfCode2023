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


class Module(object):
    @classmethod
    def from_string(cls, outputs_string):
        #outputs = re.findall("([A-Za-z]+,*)", outputs_string)
        outputs = outputs_string.split(",")
        outputs = [i.strip() for i in outputs]
        return cls(outputs)
    
class FlipFlop(Module):
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

class Conjunction (Module):
    prefix = "&"
    def __init__(self, output_modules:list):
        #self.inputs = {input_module: Pulse.Low for input_module in input_modules}
        self.inputs = {}
        self.output = Pulse.Low
        self.output_modules = output_modules
        self.pulse_count = {Pulse.Low: 0, Pulse.High: 0}
    

    def add_input(self, input_str):
        self.inputs[input_str] = Pulse.Low

    def update(self, input_module: str, input:Pulse):
        self.inputs[input_module] = input
        if Pulse.Low in self.inputs.values():
            self.output = Pulse.High
        else:
            self.output = Pulse.Low
        
        self.pulse_count[self.output] += 1

class Broadcaster(Module):
    def __init__(self, output_modules:list):
        self.output = Pulse.Low
        self.output_modules = output_modules
        self.pulse_count = {Pulse.Low: 0, Pulse.High: 0}

    def update(self, input:Pulse):
        self.output = input
        self.pulse_count[self.output] += 1

class Button(Module):
    def __init__(self, output_modules:list):
        self.output = Pulse.Low
        self.output_modules = output_modules
        self.pulse_count = {Pulse.Low: 0, Pulse.High: 0}

    def update(self):
        self.output = Pulse.Low
        self.pulse_count[self.output] += 1

class Output(Module):
    def update(self):
        pass

def parse_inputs(data):

    modules = {}

    for row in data:
        name, outputs = row.split("->")
        name = name.strip()
        if name[0] == "&":
            modules[name[1:]] = Conjunction.from_string(outputs)
        elif name[0] == "%":
            modules[name[1:]] = FlipFlop.from_string(outputs)
        elif name == "broadcaster":
            modules[name] = Broadcaster.from_string(outputs)
        elif name == "output":
            modules[name] = Output()

    return modules

def part_1(data, button_presses):

    # Inital setup
    button = Button(["broadcaster"])
    modules = parse_inputs(data)
    modules["button"] = button

    print(modules)

    for name, module in modules.items():
        print(f"{name}, {module}, {module.output_modules}")
        for output in module.output_modules:
            
            output_module = modules[output]
            if isinstance(output_module, Conjunction):
                output_module.add_input(name)

    return

def part_2(data):

    return

if __name__ == "__main__":

    DAY = "20"
    data = read_text_file(f"{DAY}.txt")
    print(part_1(data))
    print(part_2(data))