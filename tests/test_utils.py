import pytest
from ..utils import distance, cross, distance_from_line, \
    tiles_on_route, BitMask
from roguelike.lights import Tile, LightSource
import math


def test_distance():
    p1 = (3, 4)
    p2 = (7, 7)
    assert 5.0 == distance(p1, p2)


def test_distance_from_line():
    d1 = (0, 0)
    d2 = (6, 4)
    distance_from_line(d1, d2, (3, 2)) == 0
    distance_from_line(d1, d2, (5, -1)) == distance((3, 2))


def test_tiles_on_route():
    assert tiles_on_route((0, 0), (3, 0)) == [(1, 0), (2, 0), (3, 0)]
    assert tiles_on_route((1, 2), (1, -3)) == [(1, 1), (1, 0), (1, -1),
                                                 (1, -2), (1, -3)]
    assert tiles_on_route((1, 0), (5, 3)) == [(2, 0), (2, 1), (3, 1),
                                                (3, 2), (4, 2), (4, 3), (5, 3)]
    assert tiles_on_route((-3, 3), (0, 0)) == [(-2, 2), (-1, 1), (0, 0)]


def test_bitmask():
    mask1 = BitMask(3, 3, True)
    mask2 = BitMask(3, 3, False)
    assert (mask1 | mask2).data == [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    assert (mask1 & mask2).data == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


def test_light_source():
    tile = Tile(None, 4, 3)
    light = LightSource(owner=tile, lrange=3, is_lit=1)
    print(light.get_mask(7, 7))
