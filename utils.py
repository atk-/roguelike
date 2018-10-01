import math
from collections import namedtuple
from functools import partial


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, xy):
        return Point(self.x + xy[0], self.y + xy[1])

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    @property
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def distance(p1, p2):
    """Compute Euclidian distance between two points."""
    return (p2 - p1).length
    #return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))


def cross(p1, p2):
    """Compute cross product between two vectors."""
    return p1.x * p2.y - p2.x * p1.y
    #return x1 * y2 - x2 * y1


def distance_from_line(d1, d2, p):
    """Compute the perpendicular distance of a point from a line."""
    if d1 == d2:
        return distance(d1, p)
    return abs(cross(d2 - d1, d1 - p) / (d1 - d2).length)


def qrange(a, b, step=1):
    if b < a:
        return range(a, b-1, -step)
    return range(a, b+1)


def tiles_on_route(p1, p2):
    DELTAS = {
        -2: [(-1, 0), (0, -1)],
        -1: [(0, -1), (1, 0)],
        0: [(1, 0), (0, 1)],
        1: [(0, 1), (-1, 0)],
    }

    if p1.x == p2.x:
        tiles = [Point(p1.x, y) for y in qrange(p1.y, p2.y)]
    elif p1.y == p2.y:
        tiles = [Point(x, p1.y) for x in qrange(p1.x, p2.x)]
    else:
        tiles = []
        k = (p2 - p1).y / (p2 - p1).x
        a = math.atan2((p2 - p1).y, (p2 - p1).x) / math.pi * 2
        deltas = DELTAS[math.floor(a)]
        x, y = p1.x, p1.y
        dfunc = partial(distance_from_line, p1, p2)
        p = p1
        while not p == p2:
            # TODO what is the tiebreak with diagonals?
            candidates = [p + d for d in deltas]
            dists = [dfunc(c) for c in candidates]
            if dists.count(min(dists)) == 1:
                p = candidates[dists.index(min(dists))]
            else:
                p += deltas[0]
                p += deltas[1]
            tiles.append(p)

    if p1 in tiles:
        tiles.remove(p1)
    return tiles

