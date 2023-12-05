import sys
import typing as T
from functools import reduce
import multiprocessing as mp

def str_numbers_to_int(s: str) -> T.List[int]:
    s = s.strip()
    return [int(x) for x in s.split(" ") if x]

with open(sys.argv[1]) as f:
    lines = f.readlines()

seeds = str_numbers_to_int(lines[0].split(": ")[-1].strip())

lines = lines[1:]
# extra newline for better alignment
lines.append("\n")

raw_map_groups: T.List[T.List[str]] = []

last_empty_line_idx = 0
for idx, line in enumerate(lines):
    line = line.strip()
    if not line:
        if idx == last_empty_line_idx:
            continue
        group = [group_line.strip() for group_line in lines[last_empty_line_idx+1: idx]]
        raw_map_groups.append(group)
        last_empty_line_idx = idx

mappings: T.Dict[str, T.List[T.Callable[[int], int]]] = {}

# putting this in a function because I was having trouble with variable capture in the range_mapper
def process_group(group):
    current_mappings = []
    current_group_name = ""
    for idx, line in enumerate(group):
        if idx == 0:
            current_group_name = line.split(" ")[0]
            current_mappings = []
            mappings[current_group_name] = current_mappings
            continue
        # create immediately called function to workaroud more variable capture issues
        def create_mapper():
            dst_start, src_start, range_len = str_numbers_to_int(line)

            def range_mapper(src_in: int) -> int:
                if src_in < src_start or src_in > src_start + range_len:
                    # 0 indicates no range match
                    return 0
                # now we have a range match, calculate what the destination is
                offset = src_in - src_start
                return dst_start + offset
            current_mappings.append(range_mapper)
        create_mapper()


for group in raw_map_groups:
    process_group(group)

mapping_progression = ("seed-to-soil", "soil-to-fertilizer", "fertilizer-to-water", "water-to-light", "light-to-temperature", "temperature-to-humidity", "humidity-to-location")

def process_mappings(val: int) -> int:
    res = val
    for prog in mapping_progression:
        mapping_group = mappings[prog]
        for mapping in mapping_group:
            mapping_val = mapping(res)
            if mapping_val:
                res = mapping_val
                break

    return res

seed_mappings = [process_mappings(seed) for seed in seeds]
lowest_location = reduce(min, seed_mappings)
print(f"part1: {lowest_location}")

# copy paste
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def range_valgen(range_lower, range_size):
    for val in range(range_lower, range_lower + range_size):
        if val % range_size/10 == 0:
            print(f"progress on {range_lower} -> {val}")
        res = process_mappings(val)
        assert res
        yield res


def pool_fn(args):
    print(f"starting {args[0]} of size {args[1]}")
    res = reduce(min, range_valgen(*args))
    print(f"done {args[0]} of size {args[1]}")
    return res
    

pool = mp.Pool(processes=10)
each_lowest_res = pool.map_async(pool_fn, chunks(seeds, 2))
each_lowest = each_lowest_res.get(timeout=99999)
print("pool reduce done")

lowest_location_p2 = reduce(min, each_lowest)
print(f"part2: {lowest_location_p2}")