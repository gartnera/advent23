import sys
import typing as T
from functools import reduce
import multiprocessing as mp
from print_color import print
import re

def str_numbers_to_int(s: str) -> T.List[int]:
    s = s.strip()
    s = re.sub(' +', ' ', s)
    return [int(x) for x in s.split(" ") if x]

with open(sys.argv[1]) as f:
    lines = f.readlines()

times, distances = [str_numbers_to_int(line.split(":")[1]) for line in lines]

total_ways_to_win = 1
for i, [total_time, distance_record] in enumerate(zip(times,distances)):
    ways_to_win = 0
    for trial_time in range(1, total_time):
        distance = (total_time - trial_time) * trial_time
        if distance > distance_record:
            print(f"got record for {i}: {distance} > {distance_record} with {trial_time}")
            ways_to_win += 1

    print(f"ways to win for {i}: {ways_to_win}", color="green")
    total_ways_to_win *= ways_to_win

print(f"total ways to win: {total_ways_to_win}")