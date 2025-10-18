from dataclasses import dataclass
from typing import Optional

# TODO: day number should be a constant, a util script should be able to run any day, sample definitely and real input if the file is present.

@dataclass
class ExtractedMap:
    seeds: list[int]
    maps: list[list[(int, int, int)]]

def get_colon_indexes(lines: list[str]) -> list[int]:
    return [index for index in range(len(lines)) if ':' in lines[index]][1:]
def from_to(colon_indexes: list[int]) -> list[(int, int)]:
    fromtos = []
    index = 0
    while index < len(colon_indexes) - 1:
        fromtos += [(colon_indexes[index], colon_indexes[index + 1] - 2)]
        
        index += 1
    return fromtos
    
def extract_from_file(filename: str) -> ExtractedMap:
    with open(filename, "r") as f:
        lines = list(map(lambda s: s.strip(), f.readlines()))
        colon_indexes = list(map(lambda x: x + 1, get_colon_indexes(lines))) + [len(lines) + 2]
        fromtos = from_to(colon_indexes)
        
        maps = []
        for (start, end) in fromtos:
            map_lines = lines[start:end]
            m = []
            for line in map_lines:
                [a, b, c] = map(lambda x: int(x), line.split())
                m.append((a, b, c))
            maps.append(m)
        
        seeds = list(map(lambda x: int(x), lines[0].split(':')[1].strip().split()))

        return ExtractedMap(seeds, maps)

def check_in_range(source: int, range_: tuple[int, int, int]) -> Optional[int]:
    (dest_start, source_start, range_len) = range_
    if source_start <= source < source_start + range_len:
        return dest_start + (source - source_start)
    else: return None
    
def map_value(source: int, themap: list[tuple[int, int, int]]) -> int:
    for range_ in themap:
        contains = check_in_range(source, range_)
        if contains is not None:
            return contains
    return source

def pass_through_pipeline(source: int, pipeline: list[list[tuple[int, int, int]]]) -> int:
    current = source
    for themap in pipeline:
        current = map_value(current, themap)
    
    return current

def seeds_to_locations(exmap: ExtractedMap) -> list[int]:
    return [pass_through_pipeline(seed, exmap.maps) for seed in exmap.seeds]

def day2():
    print("Day 2 result: KEKW")

def day1():
    import os
    maps = extract_from_file("inputs/input-sample-01.txt")
    print(f"[SAMPLE] Day 1 result: `{min(seeds_to_locations(maps))}`")
    if os.path.exists("inputs/input-real-01.txt"):
        real_maps = extract_from_file("inputs/input-real-01.txt")
        print(f"[REAL] Day 1 result: `{min(seeds_to_locations(real_maps))}`")

if __name__ == "__main__":
    day1()
    day2()