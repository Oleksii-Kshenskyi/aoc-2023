from dataclasses import dataclass

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
        

def day2():
    print("Day 2 result: KEKW")

def day1():
    ex = extract_from_file("inputs/input-sample-01.txt")
    print(f"Day 1 result: `{ex}`")

if __name__ == "__main__":
    day1()
    day2()