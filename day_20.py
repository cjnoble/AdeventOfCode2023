import re
from enum import Enum
from collections import defaultdict, deque
from math import lcm

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
    def from_string(cls, name, outputs_string):
        #outputs = re.findall("([A-Za-z]+,*)", outputs_string)
        outputs = outputs_string.split(",")
        outputs = [i.strip() for i in outputs]
        return cls(name, outputs)

    def add_input(self, input_str):
        self.inputs[input_str] = Pulse.Low

    def __repr__(self):
        return f"{self.__class__.__name__} {self.name} {self.output}"
    
    def status(self):
        return f"{self.output.value}"

class FlipFlop(Module):
    prefix = "%"
    def __init__(self, name, output_modules:list):
        self.name = name
        self.output = Pulse.Low
        self.output_modules = output_modules
        self.pulse_count = {Pulse.Low: 0, Pulse.High: 0}
        self.inputs = {}
    
    def update(self, instruction):
        input = instruction.pulse
        if input == Pulse.Low:
            if self.output == Pulse.Low:
                self.output = Pulse.High
            else: # Current output is high
                self.output = Pulse.Low
        
            self.pulse_count[self.output] += len(self.output_modules)
            return [Instruction(self.name, module, self.output) for module in self.output_modules]
        elif input == Pulse.High:
            pass #do nothing
        else:
            raise Exception(f"Unknown instruction {instruction}")

class Conjunction (Module):
    prefix = "&"
    def __init__(self, name, output_modules:list):
        #self.inputs = {input_module: Pulse.Low for input_module in input_modules}
        self.name = name
        self.inputs = {}
        self.output = Pulse.Low
        self.output_modules = output_modules
        self.pulse_count = {Pulse.Low: 0, Pulse.High: 0}
    
    def update(self, instruction):
        '''
        input_module: str, input:Pulse
        '''
        input_module = instruction.input
        input = instruction.pulse

        self.inputs[input_module] = input
        if Pulse.Low in self.inputs.values():
            self.output = Pulse.High
        else:
            self.output = Pulse.Low
        
        self.pulse_count[self.output] += len(self.output_modules)
        return [Instruction(self.name, module, self.output) for module in self.output_modules]

    @classmethod
    def from_string(cls, name, string):
        outputs = re.findall("([A-Za-z]+,*)", string)
        return cls(name, outputs)

class Broadcaster(Module):
    def __init__(self, name, output_modules:list):
        self.name = name
        self.inputs = {}
        self.output = Pulse.Low
        self.output_modules = output_modules
        self.pulse_count = {Pulse.Low: 0, Pulse.High: 0}

    def update(self, instruction):
        #input:Pulse):
        self.output = instruction.pulse
        self.pulse_count[self.output] += len(self.output_modules)
        return [Instruction(self.name, module, self.output) for module in self.output_modules]

class Button(Module):
    def __init__(self, name, output_modules:list):
        self.name = name
        self.inputs = {}
        self.output = Pulse.Low
        self.output_modules = output_modules
        self.pulse_count = {Pulse.Low: 0, Pulse.High: 0}

    def update(self, instruction):
        self.output = Pulse.Low
        self.pulse_count[self.output] += 1
        return [Instruction(self.name, module, self.output) for module in self.output_modules]

class Output(Module):
    def __init__(self, name):
        self.name = name
        self.inputs = {}
        self.output = Pulse.High
        self.output_modules = []
        self.pulse_count = {Pulse.Low: 0, Pulse.High: 0}

    def update(self, instruction):
        if instruction.pulse == Pulse.Low:
            self.output = Pulse.Low

def parse_inputs(data):

    modules = {}

    for row in data:
        name, outputs = row.split("->")
        name = name.strip()
        if name[0] == "&":
            modules[name[1:]] = Conjunction.from_string(name[1:], outputs)
        elif name[0] == "%":
            modules[name[1:]] = FlipFlop.from_string(name[1:], outputs)
        elif name == "broadcaster":
            modules[name] = Broadcaster.from_string(name,outputs)
        elif name == "output":
            modules[name] = Output(name)

    return modules


def set_up(data):
    button = Button("button", ["broadcaster"])
    modules = parse_inputs(data)
    modules["button"] = button

    #print(modules)

    for name, module in list(modules.items()):
        #print(f"{name}, {module}, {module.output_modules}")
        for output in module.output_modules:
            
            if output not in modules:
                modules[output] = Output(output)

            output_module = modules[output]
                
            output_module.add_input(name)

    return modules

class Instruction(object):

    def __init__(self, input, output, pulse):
        self.input = input
        self.output = output
        self.pulse = pulse

    def __repr__(self):
        return f"{self.input}, {self.output}, {self.pulse}"


def part_1(data, button_presses):

    # Inital setup
    modules = set_up(data)

    for button_counter in range(button_presses):

        instructions = deque()
        instructions.append(Instruction("", "button", None))

        while True:
            #print(instructions)
            new_instructions = deque()
            while instructions:
                instruction = instructions.popleft()
                output_module = modules[instruction.output]

                next_instructions = output_module.update(instruction)
                #print(next_instructions)
                if next_instructions:
                    new_instructions.extend(next_instructions)
            if new_instructions:
                instructions = new_instructions
            else:
                break

    low_pulse_count = sum([m.pulse_count[Pulse.Low] for m in modules.values()])
    high_pulse_count = sum([m.pulse_count[Pulse.High] for m in modules.values()])
    print(f"Low pulses sent {low_pulse_count}, High pulses sent {high_pulse_count}")
    return low_pulse_count * high_pulse_count

def trace_inputs(module_name, modules):

    inputs = modules[module_name].inputs
    for input in inputs:
        print(input)

    return [trace_inputs(input, modules) for input in inputs]


def part_2(data):
# Inital setup
    modules = set_up(data)
    button_presses = 2**13

    test = "rx"

    inputs = modules[test].inputs
    for input in inputs:
        print(modules[input])
        r_inputs = modules[input].inputs
        for r_input in r_inputs:
            print(modules[r_input])

    r_input_cycles = defaultdict(lambda: dict())

    #trace_inputs(test, modules)

    for module_type in [FlipFlop, Conjunction, Broadcaster, Button, Output]:
        print(module_type.__name__, len([module for module in modules.values() if isinstance(module, module_type)]))

    print_modul_status(modules)

    for button_counter in range(1, button_presses + 1):

        instructions = deque()
        instructions.append(Instruction("", "button", None))

        while True:
            #print(instructions)
            new_instructions = deque()
            while instructions:
                instruction = instructions.popleft()
                output_module = modules[instruction.output]

                next_instructions = output_module.update(instruction)
                #print(next_instructions)
                if next_instructions:
                    new_instructions.extend(next_instructions)
            if new_instructions:
                instructions = new_instructions
            else:
                break
        #print_modul_status(modules)
            if modules["rx"].output == Pulse.Low:
                print(f"Pulse sent after {button_counter}")
                break

            for r_input in r_inputs:
                if r_input not in r_input_cycles or max(r_input_cycles[r_input].keys()) < modules[r_input].pulse_count[Pulse.High]:
                    print(modules[r_input].pulse_count[Pulse.High], modules[r_input].output)
                    r_input_cycles[r_input][modules[r_input].pulse_count[Pulse.High]] = button_counter

    print(r_input_cycles)
    return lcm(*[r[1] for r in r_input_cycles.values()])

def print_modul_status(modules):
    print([module.status() for module in modules.values() if isinstance(module, FlipFlop)])        

if __name__ == "__main__":

    DAY = "20"
    data = read_text_file(f"{DAY}.txt")
    print(part_1(data, 1000))
    print(part_2(data))