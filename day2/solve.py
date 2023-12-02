import sys
import typing as T

with open(sys.argv[1]) as f:
    lines = f.readlines()

constraint = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

id_sum = 0

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

    ok = True
    for key, value in constraint.items():
        if color_max[key] > value:
            print(f"Game {id} fails constraint because {key} {color_max[key]} > {value}")
            ok = False

    if ok:
        id_sum += int(id)

print(id_sum)