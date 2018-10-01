import pytest
from ..utils import Point as P, distance, cross, distance_from_line
import math


def test_point():
    p1 = P(3, 2)
    assert p1.x == 3
    assert p1.y == 2
    assert abs(p1.length - math.sqrt(13)) < 0.0001

    p2 = P(9, -2)
    assert p2.y == -2
    assert abs(p2.length - math.sqrt(85)) < 0.0001

    p3 = P(3, 2)
    assert p1 == p3
    assert p1 != p2
    assert p2 != p3

    assert p1 - p2 == P(-6, 4)
    assert p2 - p3 == P(6, -4)
    assert p1 - p3 == P(0, 0)
    assert (p1 - p3).length == 0


def test_distance():
    p1 = P(3, 4)
    p2 = P(7, 7)
    assert p1.length == 5.0 == distance(p1, p2)
    assert (p2 - p1).length == 5.0 == (p1 - p2).length


def test_distance_from_line():
    d1 = P(0, 0)
    d2 = P(6, 4)
    distance_from_line(d1, d2, P(3, 2)) == 0
    distance_from_line(d1, d2, P(5, -1)) == P(3, 2).length

