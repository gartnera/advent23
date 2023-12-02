import sys
import typing as T
from functools import reduce

with open(sys.argv[1]) as f:
    lines = f.readlines()

power_sum = 0

for game in lines:
    game = game.strip()
    start_idx = game.index(":")
    id = game[game.index(" ")+1:start_idx]
    
    game = game[start_idx+2:]

    color_max: T.Dict[str, int] = {}

    for draw in game.split(";"):
        draw = draw.strip()
        for cube in draw.split(","):
            cube = cube.strip()
            number, color = cube.split(" ")
            number = int(number)
            if number > color_max.get(color, 0):
                color_max[color] = number

    power = reduce(lambda a,b: a*b, color_max.values())
    print(f"Game {id} power: {power}")
    power_sum += power
    
print(power_sum)