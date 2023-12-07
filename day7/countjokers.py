import sys

with open(sys.argv[1]) as f:
    lines = f.readlines()

res_max = 0
for line in lines:
    line_ctr = sum([1 for c in line if c == 'J'])
    res_max = max(line_ctr, res_max)

print(res_max)