import typing as T
import sys

def str_numbers_to_int(s: str) -> T.List[int]:
    s = s.strip()
    return [int(x) for x in s.split(" ") if x]

def load(filepath: str) -> T.Tuple[T.List[int]]:
    with open(filepath) as f:
        lines = f.readlines()

    return [str_numbers_to_int(line.strip()) for line in lines]

def solve_line(line: T.List[int]) -> int:
    history = [line]
    while True:
        prev_line = history[-1]
        new_line = [prev_line[i+1] - prev_line[i] for i in range(len(prev_line)-1)]
        history.append(new_line)
        if not any(new_line):
            break
    rhistory = list(reversed(history))
    end = 0
    for i, line in enumerate(rhistory[:-1]):
        end = end + rhistory[i+1][-1]

    begin = 0
    for i, line in enumerate(rhistory[:-1]):
        begin = rhistory[i+1][0] - begin
        # print(begin)

    #print(history, end, begin)

    return end, begin


def solve(lines: T.List[T.List[int]]) -> int:
    res = [solve_line(line) for line in lines]
    return sum(x[0] for x in res), sum(x[1] for x in res)

if __name__ == "__main__":
    lines = load(sys.argv[1])
    end_sum, begin_sum = solve(lines)
    print(f"end_sum: {end_sum}")
    print(f"begin_sum: {begin_sum}")
