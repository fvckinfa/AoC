from __future__ import annotations
import sys
from bisect import bisect_left, bisect_right
from typing import List, Tuple

def parse_ranges(text: str) -> List[Tuple[int, int]]:
    text = text.strip()
    if not text:
        return []
    parts = text.split(",")
    out = []
    for p in parts:
        a, b = p.split("-")
        out.append((int(a), int(b)))
    return out

def gen_invalid_numbers(max_digits: int, exactly_twice: bool) -> List[int]:
    """
    Generate all numbers with <= max_digits digits that are made of a digit-sequence
    repeated exactly twice (part1) or at least twice (part2).
    No leading zeros allowed (pattern can't start with 0).
    """
    vals = set()

    if exactly_twice:
        # length L = 2*p
        for p in range(1, max_digits // 2 + 1):
            start = 10 ** (p - 1)
            end = 10 ** p - 1
            for x in range(start, end + 1):
                s = str(x)
                vals.add(int(s + s))
    else:
        # length L = p*k, k>=2
        for p in range(1, max_digits // 2 + 1):
            start = 10 ** (p - 1)
            end = 10 ** p - 1
            max_k = max_digits // p
            for x in range(start, end + 1):
                s = str(x)
                for k in range(2, max_k + 1):
                    vals.add(int(s * k))

    return sorted(vals)

def sum_in_ranges(sorted_vals: List[int], ranges: List[Tuple[int, int]]) -> int:
    # prefix sums for O(log n) range sum
    pref = [0]
    acc = 0
    for v in sorted_vals:
        acc += v
        pref.append(acc)

    total = 0
    for a, b in ranges:
        lo = bisect_left(sorted_vals, a)
        hi = bisect_right(sorted_vals, b)
        total += pref[hi] - pref[lo]
    return total

def main() -> None:
    text = sys.stdin.read().strip()
    ranges = parse_ranges(text)
    if not ranges:
        print("No ranges found on stdin.")
        return

    max_b = max(b for _, b in ranges)
    max_digits = len(str(max_b))

    invalid_part1 = gen_invalid_numbers(max_digits=max_digits, exactly_twice=True)
    invalid_part2 = gen_invalid_numbers(max_digits=max_digits, exactly_twice=False)

    ans1 = sum_in_ranges(invalid_part1, ranges)
    ans2 = sum_in_ranges(invalid_part2, ranges)

    print(ans1)
    print(ans2)

if __name__ == "__main__":
    main()
