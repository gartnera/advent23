import sys
import typing as T
from functools import reduce
from pprint import pprint

with open(sys.argv[1]) as f:
    lines = f.readlines()

# pad with "." to make range finalization easier
lines = [line.strip()+"." for line in lines]

part_number_sum = 0

def should_print(row_idx: int) -> bool:
    return row_idx == 19
    #return row_idx < 3
    return row_idx > len(lines) - 2

for row_idx, row_val in enumerate(lines):
    min_idx=None
    max_idx=None
    for col_idx, col_val in enumerate(row_val):
        if col_val.isdigit():
            if min_idx is None:
                min_idx = col_idx
            max_idx = col_idx
            continue

        if min_idx is None:
            continue

        assert min_idx is not None
        assert max_idx is not None

        # we have a range (need to add one since upper bound is exclusive)
        val = row_val[min_idx:max_idx+1]

        rel_rows = lines[max(0, row_idx - 1):min(len(lines), row_idx + 2)]
        # annoying you can't 2d slice like numpy
        rel_area = [row[max(min_idx - 1, 0):min(max_idx + 2, len(row_val))] for row in rel_rows]
        if should_print(row_idx):
            pprint(rel_area)
        # no .flat() like js...
        rel_area_flat = [b for a in rel_area for b in a]
        # this is getting progressibly more dense...
        ok = reduce(lambda res, val : res or (not val.isdigit() and val != "."), rel_area_flat, False)

        if should_print(row_idx):
            print(f"got val {val} (ok: {ok}) from row {row_idx} {min_idx}:{max_idx}\n")

        if ok:
            part_number_sum += int(val)

        # reset
        min_idx = None
        max_idx = None

print(part_number_sum)