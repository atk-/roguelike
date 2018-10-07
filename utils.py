import math
from collections import namedtuple
from functools import partial


def distance(p1, p2=(0, 0)):
    """Compute Euclidian distance between two points."""
    return math.sqrt(distance2(p1, p2))


def distance2(p1, p2=(0, 0)):
    return (p2[0] - p1[0]) * (p2[0] - p1[0]) + \
        (p2[1] - p1[1]) * (p2[1] - p1[1])


def cross(p1, p2):
    """Compute cross product between two vectors."""
    return p1[0] * p2[1] - p2[0] * p1[1]


def distance_from_line(d1, d2, p):
    """Compute the perpendicular distance of a point from a line."""
    if d1 == d2:
        return distance2(d1, p)
    return abs(cross((d2[0] - d1[0], d2[1] - d1[1]),
                     (d1[0] - p[0], d1[1] - p[1]))) / distance2(d1, d2)


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

    if p1[0] == p2[0]:
        tiles = [(p1[0], y) for y in qrange(p1[1], p2[1])]
    elif p1[1] == p2[1]:
        tiles = [(x, p1[1]) for x in qrange(p1[0], p2[0])]
    else:
        tiles = []
        a = math.atan2((p2[1] - p1[1]), (p2[0] - p1[0])) / math.pi * 2
        deltas = DELTAS[math.floor(a)]
        x, y = p1
        dfunc = partial(distance_from_line, p1, p2)
        p = p1
        while not p == p2:
            # TODO what is the tiebreak with diagonals?
            candidates = [(p[0] + d[0], p[1] + d[1]) for d in deltas]
            dists = [dfunc(c) for c in candidates]
            if dists.count(min(dists)) == 1:
                p = candidates[dists.index(min(dists))]
            else:
                p = (p[0] + deltas[0][0] + deltas[1][0],
                     p[1] + deltas[0][1] + deltas[1][1])
            tiles.append(p)

    if p1 in tiles:
        tiles.remove(p1)
    return tiles


class BitMask:
    def __init__(self, width=0, height=0, defvalue=None, data=None):
        self.width = width or len(data)
        self.height = height or len(data[0])
        if data:
            self.data = data
        else:
            self.data = [[defvalue] * width for i in range(height)]

    def __or__(self, other):
        assert other.width == self.width
        assert other.height == self.height
        for i, (r1, r2) in enumerate(zip(self.data, other.data)):
            self.data[i] = [p or q for p, q in zip(r1, r2)]

        return self

    def __and__(self, other):
        assert other.width == self.width
        assert other.height == self.height
        for i, (r1, r2) in enumerate(zip(self.data, other.data)):
            self.data[i] = [p and q for p, q in zip(r1, r2)]

        return self

    def __getitem__(self, z):
        if isinstance(z, int):
            return self.data[z]
        else:
            return self.data[z[0]][z[1]]

    def __str__(self):
        return '\n'.join(
            [''.join(
                ['#' if c else '.' for c in row]
            ) for row in self.data]
        )

    def apply(self, world):
        assert len(world) == len(self.data)
        assert len(world[0]) == len(self.data[0])
        return [''.join([ch.chr if bit else ' ' for ch, bit in zip(wrow, lrow)])
                for wrow, lrow in zip(world, self.data)]

    @classmethod
    def from_data(cls, data):
        return cls(data=data)

    @classmethod
    def ones(cls, width, height):
        return cls(width, height, defvalue=1)

    @classmethod
    def zeros(cls, width, height):
        return cls(width, height, defvalue=0)

    @classmethod
    def empty(cls, width, height):
        return cls(width, height, defvalue=None)
