from os import path
from enum import Enum

DAY = "08"

class TurnDirection(Enum):
    Left = "L"
    Right = "R"

class Navigator:
    def __init__(self, instructions: list[TurnDirection], nodes: dict[str, (str, str)]):
        self.instructions = instructions
        self.nodes = nodes
        self.instruction_index = 0
        self.steps_taken = 0
        self.current_node = "AAA"
    
    from typing import Optional
    def stepcount_if_arrived(self) -> Optional[int]:
        return self.steps_taken if self.current_node == "ZZZ" else None
    
    def step(self):
        match self.instructions[self.instruction_index]:
            case TurnDirection.Left: self.current_node = self.nodes[self.current_node][0]
            case TurnDirection.Right: self.current_node = self.nodes[self.current_node][1]
        self.instruction_index = (self.instruction_index + 1) % len(self.instructions)
        self.steps_taken += 1

def day1_navigate(nav: Navigator) -> int:
    while (steps := nav.stepcount_if_arrived()) is None:
        nav.step()
    return steps

def parse_navigation(filename: str) -> Navigator:
    lines = list(map(str.strip, open(filename, "r").readlines()))
    instructions = list(map(lambda dir: TurnDirection(dir), lines[0]))
    import re
    nodes = {}
    for node_str in lines[2:]:
        (node, left, right) = re.match(r'(\w+) = \((\w+), (\w+)\)', node_str).groups()
        nodes[node] = (left, right)
    return Navigator(instructions, nodes)
        

def part2():
    sample_filename = f"inputs/input-sample-{DAY}.txt"
    real_filename = f"inputs/input-real-{DAY}.txt"
    print(f"[SAMPLE] part 2 result: {sample_filename}")
    if path.exists(real_filename):
        print(f"[REAL] part 2 result: {real_filename}")

def part1():
    sample_filename = f"inputs/input-sample-{DAY}.txt"
    real_filename = f"inputs/input-real-{DAY}.txt"
    print(f"[SAMPLE] part 1 result: {day1_navigate(parse_navigation(sample_filename))}")
    if path.exists(real_filename):
        print(f"[REAL] part 1 result: {day1_navigate(parse_navigation(real_filename))}")

if __name__ == "__main__":
    part1()
    part2()