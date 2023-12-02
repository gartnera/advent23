import sys

with open('input.txt') as f:
    lines = f.readlines()

sum = 0
numbers = []

phrases = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

phrase_keys = phrases.keys()

def phase_to_number(s: str) -> int:
    for phrase in phrase_keys:
        if s.startswith(phrase):
            return phrases[phrase]
    return 0


for line in lines:
    line = line.strip()
    first = None
    last = None
    for idx, c in enumerate(line):
        if number := phase_to_number(line[idx:]):
            digit = str(number)
        elif c.isdigit():
            digit = c
        else:
            continue
        if not first:
            first = digit
        last = digit
    number = int(first+last)
    print(f"given {line} got {number}")
    sum += number

print(f"sum: {sum}")