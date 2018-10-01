import pytest
from ..utils import Point as P, distance, cross, distance_from_line, \
    tiles_on_route
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


def test_tiles_on_route():
    assert tiles_on_route(P(0, 0), P(3, 0)) == [P(1, 0), P(2, 0), P(3, 0)]
    assert tiles_on_route(P(1, 2), P(1, -3)) == [P(1, 1), P(1, 0), P(1, -1),
                                                 P(1, -2), P(1, -3)]
    assert tiles_on_route(P(1, 0), P(5, 3)) == [P(2, 0), P(2, 1), P(3, 1),
                                                P(3, 2), P(4, 2), P(4, 3), P(5, 3)]
    assert tiles_on_route(P(-3, 3), P(0, 0)) == [P(-2, 2), P(-1, 1), P(0, 0)]
