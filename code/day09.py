from __future__ import annotations

import sys
from typing import List, Tuple


def parse_points(lines: List[str]) -> List[Tuple[int, int]]:
    pts: List[Tuple[int, int]] = []
    for line in lines:
        if not line.strip():
            continue
        x_str, y_str = line.strip().split(",")
        pts.append((int(x_str), int(y_str)))
    return pts


def max_rectangle_area(points: List[Tuple[int, int]]) -> int:
    n = len(points)
    best = 0
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            if area > best:
                best = area
    return best


def on_segment(px: int, py: int, ax: int, ay: int, bx: int, by: int) -> bool:
    return min(ax, bx) <= px <= max(ax, bx) and min(ay, by) <= py <= max(ay, by)


def point_on_edge(px: int, py: int, a: Tuple[int, int], b: Tuple[int, int]) -> bool:
    ax, ay = a
    bx, by = b
    if ax == bx:
        return px == ax and on_segment(px, py, ax, ay, bx, by)
    if ay == by:
        return py == ay and on_segment(px, py, ax, ay, bx, by)
    return False


def point_in_polygon(px: int, py: int, poly: List[Tuple[int, int]]) -> bool:
    # Even-odd rule; counts boundary as inside.
    inside = False
    n = len(poly)
    for i in range(n):
        a = poly[i]
        b = poly[(i + 1) % n]
        if point_on_edge(px, py, a, b):
            return True
        x1, y1 = a
        x2, y2 = b
        if (y1 > py) != (y2 > py):
            x_int = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            if x_int >= px:
                inside = not inside
    return inside


def segments_cross_proper(v1: Tuple[int, int], v2: Tuple[int, int], h1: Tuple[int, int], h2: Tuple[int, int]) -> bool:
    # v segment vertical, h segment horizontal; returns True if they cross in interiors.
    vx = v1[0]
    vy1, vy2 = sorted((v1[1], v2[1]))
    hy = h1[1]
    hx1, hx2 = sorted((h1[0], h2[0]))
    if hx1 < vx < hx2 and vy1 < hy < vy2:
        return True
    return False


def rectangle_inside(poly: List[Tuple[int, int]], rect_corners: List[Tuple[int, int]]) -> bool:
    # Check corners inside/on boundary.
    for x, y in rect_corners:
        if not point_in_polygon(x, y, poly):
            return False

    # Build rectangle edges (axis-aligned).
    [x1, y1], [x2, y2], [x3, y3], [x4, y4] = rect_corners
    rect_edges = [
        ((x1, y1), (x2, y2)),
        ((x2, y2), (x3, y3)),
        ((x3, y3), (x4, y4)),
        ((x4, y4), (x1, y1)),
    ]

    # Precompute polygon edges.
    p_edges = [
        (poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))
    ]

    for ra, rb in rect_edges:
        if ra[0] == rb[0]:
            # vertical edge
            for pa, pb in p_edges:
                if pa[0] == pb[0]:
                    continue  # parallel
                if segments_cross_proper(ra, rb, pa, pb):
                    return False
        else:
            # horizontal edge
            for pa, pb in p_edges:
                if pa[1] == pb[1]:
                    continue  # parallel
                if segments_cross_proper(pa, pb, ra, rb):
                    return False

    return True


def max_rectangle_area_rg(points: List[Tuple[int, int]]) -> int:
    # Build polygon from point order (wrap) representing red/green boundary.
    poly = points
    best = 0
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            if area <= best:
                continue
            if x1 == x2 and y1 == y2:
                continue
            rect = [
                (x1, y1),
                (x2, y1),
                (x2, y2),
                (x1, y2),
            ]
            if rectangle_inside(poly, rect):
                best = area
    return best


def main() -> None:
    lines = sys.stdin.read().splitlines()
    points = parse_points(lines)
    if "--part2" in sys.argv:
        print(max_rectangle_area_rg(points))
    else:
        print(max_rectangle_area(points))


if __name__ == "__main__":
    main()
