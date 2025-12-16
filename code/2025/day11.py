from collections import defaultdict
import sys


def build_graph(lines):
    graph = defaultdict(list)
    for line in lines:
        if not line.strip():
            continue
        parts = line.replace(":", "").split()
        node, outs = parts[0], parts[1:]
        graph[node] = outs
    return graph


def count_paths_between(graph, start, target, memo):
    if start == target:
        return 1
    key = (start, target)
    if key in memo:
        return memo[key]
    total = 0
    for nei in graph.get(start, []):
        total += count_paths_between(graph, nei, target, memo)
    memo[key] = total
    return total


def solve_part1(lines):
    graph = build_graph(lines)
    return count_paths_between(graph, "you", "out", {})


def solve_part2(lines):
    graph = build_graph(lines)
    memo = {}
    # Paths that hit dac then fft
    path_dac_fft = (
        count_paths_between(graph, "svr", "dac", memo)
        * count_paths_between(graph, "dac", "fft", memo)
        * count_paths_between(graph, "fft", "out", memo)
    )
    # Paths that hit fft then dac
    path_fft_dac = (
        count_paths_between(graph, "svr", "fft", memo)
        * count_paths_between(graph, "fft", "dac", memo)
        * count_paths_between(graph, "dac", "out", memo)
    )
    return path_dac_fft + path_fft_dac


def main():
    lines = sys.stdin.read().splitlines()
    if "--part2" in sys.argv:
        print(solve_part2(lines))
    else:
        print(solve_part1(lines))


if __name__ == "__main__":
    main()
