from dataclasses import dataclass
from os import path

DAY = "07"

CARD_POWERS = {
    "2": 0,
    "3": 1,
    "4": 2,
    "5": 3,
    "6": 4,
    "7": 5,
    "8": 6,
    "9": 7,
    "T": 8,
    "J": 9,
    "Q": 10,
    "K": 11,
    "A": 12,
}
CARD_POWERS_V2 = {
    "J": 0,
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
    "9": 8,
    "T": 9,
    "Q": 10,
    "K": 11,
    "A": 12,
}

def sort(l: list) -> list:
    l.sort()
    return l

from itertools import pairwise
from collections import Counter
HAND_POWERS = {
    # FIVE OF A KIND
    6: lambda hand: all([a == b for (a, b) in pairwise(hand)]),
    # FOUR OF A KIND
    5: lambda hand: max(Counter(hand).values()) == 4,
    # FULL HOUSE
    4: lambda hand: sort(list(Counter(hand).values())) == [2, 3],
    # THREE OF A KIND
    3: lambda hand: max(Counter(hand).values()) == 3,
    # TWO PAIR
    2: lambda hand: sort(list(Counter(hand).values())) == [1, 2, 2],
    # ONE PAIR
    1: lambda hand: max(Counter(hand).values()) == 2,
    # HIGH CARD
    0: lambda _: True,
}

def eq(condition: bool) -> int:
    if condition: return 1
    else: return -1

from typing import Optional
@dataclass
class Hand:
    cards: str
    bid: int
    power_map: dict[str, int]
    jokered_cards: Optional[str]
    
def hands_from_file(filename: str, power_map: dict[str, int], injoker: bool) -> list[Hand]:
    pairs = list(map(lambda ln: ln.strip().split(), open(filename, "r").readlines()))
    return [Hand(pair[0], int(pair[1]), power_map, inject_jokers(pair[0]) if injoker else None) for pair in pairs]

# Returns list of pairs (hand, hand type) for each hand
def identify_hands(hands: list[Hand]) -> list[(Hand, int)]:
    ranks = []
    for hand in hands:
        used_hand = hand.jokered_cards if hand.jokered_cards else hand.cards
        for (hand_type, hand_check) in HAND_POWERS.items():
            if hand_check(used_hand):
                ranks += [(hand, hand_type)]
                break
    return ranks

# -1 if a < b
# 0 if a == b
# 1 if a > b

# Compare strength of every card starting from the first one,
# On the first differing pair, consider the hand with the stronger card in the differing pair bigger.
# Return 1 if a is bigger, -1 if a is smaller. No equality possible.
def cmp_until_stronger(a: Hand, b: Hand) -> int:
    assert a.power_map == b.power_map # sanity check that both hands use the same power map
    for i in range(0, len(a.cards)):
        if a.power_map[a.cards[i]] > a.power_map[b.cards[i]]:
            return 1
        elif a.power_map[a.cards[i]] < a.power_map[b.cards[i]]:
            return -1
    raise ValueError(f"UNREACHABLE: hands {a} and {b} completely EQUAL?")

def compare_hands(a: tuple[Hand, int], b: tuple[Hand, int]) -> int:
    # if hand types are different, we can immediately determine the winner
    if a[1] < b[1]:
        return -1
    elif a[1] > b[1]:
        return 1
    # if hand types are the same, we have to compare individual cards until one is stronger
    return cmp_until_stronger(a[0], b[0])

# Turns list of hands with determined types into sorted list of hands, strongest first, weakest last
def sort_hands(hands: list[(Hand, int)]) -> list[Hand]:
    from functools import cmp_to_key
    srt = list(sorted(hands, key=cmp_to_key(compare_hands), reverse=True))
    
    return list(map(lambda pair: pair[0], srt))

# calculates sum of (hand rank * hand bid) for every hand
def reduce_hands(hands: list[Hand]) -> int:
    from functools import reduce
    highest_rank = len(hands)
    allpower = 0
    hs = []
    for (index, hand) in enumerate(hands):
        allpower += hand.bid * (highest_rank - index)
        hs.append((highest_rank - index, hand.bid))
        
    return allpower

# Returns same hand, but injects the jokers into it according to the Joker rules of pt. 2
def inject_jokers(old_hand: str) -> str:
    import copy; new_hand = copy.deepcopy(old_hand)
    c = Counter(new_hand)
    if "J" in c and c["J"] == len(old_hand): return old_hand

    if "J" in c:
        noj = new_hand.replace("J", "")
        turn_to = Counter(noj).most_common()[0][0]
        new_hand = new_hand.replace("J", turn_to)
    return new_hand

def pipe(filename: str, power_map: dict[str, int], injoker: bool) -> int:
    return reduce_hands(sort_hands(identify_hands(hands_from_file(filename, power_map, injoker))))

def part2():
    sample_filename = f"inputs/input-sample-{DAY}.txt"
    real_filename = f"inputs/input-real-{DAY}.txt"
    print(f"[SAMPLE] part 2 result: {pipe(sample_filename, CARD_POWERS_V2, True)}")
    if path.exists(real_filename):
        print(f"[REAL] part 2 result: {pipe(real_filename, CARD_POWERS_V2, True)}")


def part1():
    sample_filename = f"inputs/input-sample-{DAY}.txt"
    real_filename = f"inputs/input-real-{DAY}.txt"
    print(f"[SAMPLE] part 1 result: {pipe(sample_filename, CARD_POWERS, False)}")
    if path.exists(real_filename):
        print(f"[REAL] part 1 result: {pipe(real_filename, CARD_POWERS, False)}")

if __name__ == "__main__":
    part1()
    part2()