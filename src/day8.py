from os import path
from enum import Enum

DAY = "08"

from functools import reduce
from math import gcd
def lcm(a: int, b: int) -> int:
    """Least common multiple of two integers."""
    if a == 0 or b == 0:
        return 0
    return abs(a // gcd(a, b) * b)
def lcm_many(values: list[int]) -> int:
    return reduce(lcm, values, 1)

def dbg(thing):
    print(f"[DBG] `{thing}`")
    return thing

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

class GhostPath:
    def __init__(self, starting_node: str, instructions: list[TurnDirection], nodes: dict[str, tuple[str, str]]):
        self.current_node = starting_node
        self.instructions = instructions
        self.nodes = nodes
        self.steps_taken = 0
        self.instruction_index = 0
        
    def has_arrived(self) -> bool:
        return self.current_node.endswith("Z")
        
    def step(self):
        match self.instructions[self.instruction_index]:
            case TurnDirection.Left: self.current_node = self.nodes[self.current_node][0]
            case TurnDirection.Right: self.current_node = self.nodes[self.current_node][1]
        self.steps_taken += 1
        self.instruction_index = (self.instruction_index + 1) % len(self.instructions)

class NavigatorV2:
    @staticmethod
    def starting_nodes(nodes: dict[str, tuple[str, str]]):
        return [node for node in nodes.keys() if node.endswith("A")]

    def __init__(self, nav: Navigator):
        self.nav = nav
        self.current_nodes = NavigatorV2.starting_nodes(nav.nodes)
        
    def calculate_steps_taken(self):
        periods = [self._find_period_for_ghost(i) for i in range(len(self.current_nodes))]
        return lcm_many(periods)

    def _find_period_for_ghost(self, starting_node_index: int) -> int:
        starting_node = self.current_nodes[starting_node_index]
        ghost_path = GhostPath(starting_node, self.nav.instructions, self.nav.nodes)
        while not ghost_path.has_arrived():            
            ghost_path.step()

        return ghost_path.steps_taken


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
    print(f"[SAMPLE] part 2 result: {NavigatorV2(parse_navigation(sample_filename)).calculate_steps_taken()}")
    if path.exists(real_filename):
        print(f"[REAL] part 2 result: {NavigatorV2(parse_navigation(real_filename)).calculate_steps_taken()}")

def part1():
    sample_filename = f"inputs/input-sample-{DAY}.txt"
    real_filename = f"inputs/input-real-{DAY}.txt"
    print(f"[SAMPLE] part 1 result: {day1_navigate(parse_navigation(sample_filename))}")
    if path.exists(real_filename):
        print(f"[REAL] part 1 result: {day1_navigate(parse_navigation(real_filename))}")

if __name__ == "__main__":
    part1()
    part2()