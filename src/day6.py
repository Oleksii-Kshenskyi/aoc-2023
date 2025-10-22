from dataclasses import dataclass
from os import path

DAY = "06"

@dataclass
class Race:
    duration: int
    max_distance: int

def get_races(filename: str) -> list[Race]:
    lines = list(map(lambda s: s.strip(), open(filename, "r").readlines()))
    splits = [line.split()[1:] for line in lines]
    races = []
    for (index, spl) in enumerate(splits[0]):
        races += [Race(int(spl), int(splits[1][index]))]
    return races

def solve_race(race: Race) -> list[int]:
    valid_solutions = []
    for i in range(1, race.duration + 1):
        (buildup_duration, flatspeed_duration) = (i, race.duration - i)
        acceleration = 1
        speed = buildup_duration * acceleration
        distance = flatspeed_duration * speed
        if distance > race.max_distance:
            valid_solutions += [i]
    return valid_solutions

def solve_part_1(races: list[Race]) -> int:
    import math
    return math.prod([len(solve_race(race)) for race in races])


def part2():
    print("part 2 result: KEKW")

def part1():
    sample_filename = f"inputs/input-sample-{DAY}.txt"
    real_filename = f"inputs/input-real-{DAY}.txt"
    print(f"[SAMPLE] part 1 result: {solve_part_1(get_races(sample_filename))}")
    if path.exists(real_filename):
        print(f"[REAL] part 1 result: {solve_part_1(get_races(real_filename))}")

if __name__ == "__main__":
    part1()
    part2()