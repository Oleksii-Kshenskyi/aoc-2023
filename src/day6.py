from dataclasses import dataclass
from os import path

DAY = "06"

@dataclass
class Race:
    duration: int
    max_distance: int

def get_str_pairs(filename: str) -> list[(str, str)]:
    lines = list(map(lambda s: s.strip(), open(filename, "r").readlines()))
    splits = [line.split()[1:] for line in lines]
    pairs = []
    for (index, spl) in enumerate(splits[0]):
        pairs += [(spl, splits[1][index])]
    return pairs

def get_races(filename: str) -> list[Race]:
    races = []
    for (stime, sdistance) in get_str_pairs(filename):
        races += [Race(int(stime), int(sdistance))]
    return races

def get_race(filename: str) -> Race:
    from functools import reduce
    (stime, sdist) = reduce(lambda pair1, pair2: (pair1[0] + pair2[0], pair1[1] + pair2[1]), get_str_pairs(filename), ("", ""))
    return Race(int(stime), int(sdist))

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

# Solve quadratic equation: x^2 - T*x + D = 0
# Discriminant = T^2 - 4*D
# Roots = r1, r2 = T +- sqrt(discriminant) / 2
def solve_quadratic_range(race: Race) -> int:
    from math import sqrt, ceil, floor
    discriminant = race.duration ** 2 - 4 * race.max_distance
    root1 = (race.duration + sqrt(discriminant)) / 2
    root2 = (race.duration - sqrt(discriminant)) / 2
    
    return ceil(root1) - floor(root2) - 1
    

def part2():
    sample_filename = f"inputs/input-sample-{DAY}.txt"
    real_filename = f"inputs/input-real-{DAY}.txt"
    print(f"[SAMPLE] part 2 result: {solve_quadratic_range(get_race(sample_filename))}")
    print(f"[REAL] part 2 result: {solve_quadratic_range(get_race(real_filename))}")

def part1():
    sample_filename = f"inputs/input-sample-{DAY}.txt"
    real_filename = f"inputs/input-real-{DAY}.txt"
    print(f"[SAMPLE] part 1 result: {solve_part_1(get_races(sample_filename))}")
    if path.exists(real_filename):
        print(f"[REAL] part 1 result: {solve_part_1(get_races(real_filename))}")

if __name__ == "__main__":
    part1()
    part2()