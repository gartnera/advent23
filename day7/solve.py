import sys
import typing as T
from functools import reduce, cmp_to_key
from itertools import groupby
from print_color import print
from pprint import pprint

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
            case "J":
                res.append(11)
            case "T":
                res.append(10)
            case _:
                res.append(int(c))
    return res

def basic_hand_rank(hand: T.List[int]) -> int:
    sorted_hand = sorted(hand)
    groups = [list(g) for k,g in groupby(sorted_hand)]

    has_three = False
    pair_ctr = 0
    for group in groups:
        group_len = len(group)
        # four or five of a kind
        if group_len >= 4:
            return group_len + 60
        if group_len == 3:
            has_three = True
        if group_len == 2:
            pair_ctr += 1
    
    if has_three and pair_ctr > 0:
        return 50
    
    if has_three:
        return 40
    
    if pair_ctr == 2:
        return 30
    
    if pair_ctr == 1:
        return 20
    
    return 10

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