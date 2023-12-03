import sys
import typing as T
from functools import reduce
from pprint import pprint
import numpy as np

with open(sys.argv[1]) as f:
    lines = f.readlines()

# pad with "." to make range finalization easier
lines = [line.strip()+"." for line in lines]

gear_values = np.zeros((len(lines), len(lines[0])), dtype=int)

part_number_sum = 0
gear_sum = 0

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
        val_int = int(val)

        local_row_begin = max(0, row_idx - 1)
        local_row_end = min(len(lines), row_idx + 2)
        rel_rows = lines[local_row_begin:local_row_end]
        local_col_begin = max(min_idx - 1, 0)
        local_col_end = min(max_idx + 2, len(row_val))
        rel_area = [row[local_col_begin:local_col_end] for row in rel_rows]

        # no .flat() like js...
        rel_area_flat = [b for a in rel_area for b in a]
        for local_row_idx, local_row in enumerate(rel_area):
            for local_col_idx, val in enumerate(local_row):
                if val != "*":
                    continue
                #pprint(rel_area)
                global_row_idx = local_row_begin + local_row_idx
                global_col_idx = local_col_begin + local_col_idx
                #print(global_row_idx, global_col_idx)
                existing_val = int(gear_values[global_row_idx, global_col_idx])
                print(f"val: {val} row_idx: {global_row_idx} col_idx: {global_col_idx} {existing_val}")
                if existing_val:
                    gear_sum += (existing_val * val_int)
                    print(f"sum {gear_sum}")
                else:
                    gear_values[global_row_idx, global_col_idx] = val_int
                    print(f"store {val_int}")

        if should_print(row_idx):
            pprint(rel_area)

        # this is getting progressibly more dense...
        ok = reduce(lambda res, val : res or (not val.isdigit() and val != "."), rel_area_flat, False)

        if should_print(row_idx):
            print(f"got val {val} (ok: {ok}) from row {row_idx} {min_idx}:{max_idx}\n")

        if ok:
            part_number_sum += val_int

        # reset
        min_idx = None
        max_idx = None

print(gear_values)
print(f"part_number_sum: {part_number_sum}")
print(f"gear_sum: {gear_sum}")