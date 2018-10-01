import math
from collections import namedtuple

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

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
