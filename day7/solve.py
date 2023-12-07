import sys
import typing as T
from functools import reduce, cmp_to_key
from itertools import groupby
from print_color import print
from pprint import pprint
from enum import Enum

JOKER = 1

class HandType(Enum):
    def __sub__(self, other):
        return self.value - other.value
    FIVE = 7
    FOUR = 6
    FULL = 5
    THREE = 4
    TWOPAIR = 3
    PAIR = 2
    HIGH = 1

def int_hand_repr(hand: str) -> T.List[int]:
    res = []
    for c in hand:
        match c:
            case "A":
                res.append(14)
            case "K":
                res.append(13)
            case "Q":
                res.append(12)
            case "T":
                res.append(10)
            # this is the joker, lower than the 2
            case "J":
                res.append(JOKER)
            case _:
                res.append(int(c))
    return res

def rank_groups(groups: T.List[int]) -> HandType:
    has_three = False
    pair_ctr = 0
    for group in groups:
        group_len = len(group)
        # four or five of a kind
        if group_len == 5:
            return HandType.FIVE
        if group_len >= 4:
            return HandType.FOUR
        if group_len == 3:
            has_three = True
        if group_len == 2:
            pair_ctr += 1
    
    if has_three and pair_ctr > 0:
        return HandType.FULL
    
    if has_three:
        return HandType.THREE
    
    if pair_ctr == 2:
        return HandType.TWOPAIR
    
    if pair_ctr == 1:
        return HandType.PAIR
    
    return HandType.HIGH


def boost_groups(groups: T.List[T.List[int]], joker_ctr: int):
    biggest_group = groups[0]
    biggest_group_val = groups[0][0]

    for _ in range(joker_ctr):
        biggest_group.append(biggest_group_val)

    print(groups)

                        
def basic_hand_rank(hand: T.List[int]) -> int:
    sorted_hand = sorted(hand)

    groups = []
    joker_ctr = 0
    for k, g in groupby(sorted_hand):
        g_list = list(g)
        if k == JOKER:
            joker_ctr = len(g_list)
        else:
            groups.append(g_list)

    if joker_ctr == 5:
        return HandType.FIVE

    groups = sorted(groups, key=len, reverse=True)

    boost_groups(groups, joker_ctr)

    return rank_groups(groups)

    

def sort_hands(x, y):
    x_hand, x_hand_repr, x_hand_rank, _ = x
    y_hand, y_hand_repr, y_hand_rank, _ = y

    cmp_res = x_hand_rank - y_hand_rank
    if cmp_res:
        return cmp_res
    else:
        for x, y in zip(x_hand_repr, y_hand_repr):
            inner_cmp_res = x - y
            if inner_cmp_res:
                return inner_cmp_res
            
def calc_total_winnings(path: str) -> int:
    with open(path) as f:
        lines = f.readlines()

    pairs: T.List[T.Tuple[str, int]] = []

    for line in lines:
        line = line.strip()
        parts = line.split(" ")
        hand, bid = parts[0], int(parts[1])
        hand_r = (int_hand_repr(hand))
        pairs.append((hand, hand_r, basic_hand_rank(hand_r), bid,))

    pairs = sorted(pairs, key=cmp_to_key(sort_hands))

    pprint(pairs)
    print(f"num pairs: {len(pairs)}")
    total_winnings = sum(map(lambda x: (x[0]) * x[1][3], enumerate(pairs, 1)))
    return total_winnings
            
if __name__ == "__main__":
    total_winnings = calc_total_winnings(sys.argv[1])
    print(total_winnings)