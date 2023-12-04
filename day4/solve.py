import sys
import typing as T
from print_color import print

with open(sys.argv[1]) as f:
    lines = f.readlines()

def str_numbers_to_int(s: str) -> T.List[int]:
    s = s.strip()
    return [int(x) for x in s.split(" ") if x]

score_sum = 0

cards = []

for line in lines:
    line = line.strip()
    card_raw, numbers_raw = line.split(":")
    card = int(card_raw.split(" ")[-1])-1

    winning, have = [str_numbers_to_int(group) for group in numbers_raw.split("|")]

    cards.append((winning,have,))

for winning, have in cards:
    card_score = 0

    for val in have:
        if val in winning:
            if card_score:
                card_score *= 2
            else:
                card_score += 1
    
    color=None
    if card_score:
        color="green"

    score_sum += card_score

    #print(f"card: {card} winning: {winning} have: {have} score: {card_score}", color=color)

card_count = 0

def count_card(card, winning, have, depth=0):
    global card_count
    card_count += 1
    match_count = 0
    for val in have:
        if val in winning:
            match_count += 1

    #print(f"{' '*depth}at {card} match_count {match_count}")
    for i in range(1, match_count+1):
        copy_idx = card + i
        #print(f"{' '*depth}at {card} recursing into {copy_idx}", color="yellow")
        count_card(copy_idx, *cards[copy_idx], depth=depth+1)

# part 2 calculations
for i, [winning, have] in enumerate(cards):
    count_card(i, winning, have)

print(f"score_sum: {score_sum}")
print(f"card_count: {card_count}")