from __future__ import annotations

import sys
import operator
from functools import reduce


def parse_grid(lines: list[str], rtl: bool = False) -> list[tuple[str, list[int]]]:
	"""Parse the worksheet into (op, numbers) pairs for each column group.

	When rtl is True, interpret each column (right-to-left) as a separate number
	with its most significant digit at the top and least at the bottom.
	"""

	if not lines:
		return []

	width = max(len(line) for line in lines)
	grid = [line.ljust(width) for line in lines]

	# Identify contiguous column ranges that contain non-space characters.
	ranges = []
	in_range = False
	start = 0
	for c in range(width):
		col_has_char = any(row[c] != " " for row in grid)
		if col_has_char and not in_range:
			start = c
			in_range = True
		elif not col_has_char and in_range:
			ranges.append((start, c - 1))
			in_range = False
	if in_range:
		ranges.append((start, width - 1))

	problems: list[tuple[str, list[int]]] = []
	for start, end in ranges:
		chunk = [row[start : end + 1] for row in grid]
		op_line = chunk[-1]
		op_char = next((ch for ch in op_line if ch in "+*"), None)
		if op_char is None:
			continue  # skip malformed chunk

		numbers: list[int] = []
		if rtl:
			for col in range(end, start - 1, -1):
				digits = "".join(row[col] for row in grid[:-1] if row[col].isdigit())
				if digits:
					numbers.append(int(digits))
		else:
			for line in chunk[:-1]:
				digits = "".join(ch for ch in line if ch.isdigit())
				if digits:
					numbers.append(int(digits))

		problems.append((op_char, numbers))

	return problems


def evaluate(problems: list[tuple[str, list[int]]]) -> int:
	total = 0
	for op_char, numbers in problems:
		if not numbers:
			continue
		if op_char == "+":
			total += sum(numbers)
		else:
			total += reduce(operator.mul, numbers, 1)
	return total


def main() -> None:
	lines = sys.stdin.read().splitlines()
	rtl = "--part2" in sys.argv
	problems = parse_grid(lines, rtl=rtl)
	total = evaluate(problems)
	print(total)


if __name__ == "__main__":
	main()
