import curses
import random
import math
from curses import wrapper
from functools import partial
from utils import distance, distance_from_line, cross
from utils import Point as P

DIRS = {
    'h': (-1, 0),
    'j': (0, 1),
    'k': (0, -1),
    'l': (1, 0),
    'y': (-1, -1),
    'u': (1, -1),
    'b': (-1, 1),
    'n': (1, 1),
}

WIDTH = 80
HEIGHT = 23

STDSCR = None


def msg(message):
    if STDSCR:
        if message:
            STDSCR.addstr(0, 0, message)
        else:
            STDSCR.addstr(0, 0, ' ' * WIDTH)
        STDSCR.refresh()


class Layers:
    NONE = 0
    FLOOR = 1
    OBSTACLE = 2
    WATER = 4
    AERIAL = 8


class World:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.objects = {}
        self.grid = [[Tile(self, y, x) for x in range(WIDTH)] for y in range(HEIGHT)]

        self.ambient = 0
        self.populate_world()

    def line_of_sight(self, p_from, p_to):
        xmin, xmax = sorted([p_from.x, p_to.x])
        ymin, ymax = sorted([p_from.y, p_to.y])
        dfunc = partial(distance_from_line, p_from, p_to)
        tiles = []
        for y in range(ymin, ymax + 1):
            for x in range(xmin, xmax + 1):
                if dfunc(P(x, y)) < 0.5 and not (P(x, y) == p_to):
                    tiles.append(self[y, x])

        for t in tiles:
            if t.layers & Layers.OBSTACLE:
                return False

        return True

    def populate_world(self):
        for i in range(10):
            self.random_tile(Tile.is_empty).add(Lamp(self))
        for i in range(30):
            self.random_tile(Tile.is_empty).add(Tree(self))

    @property
    def player(self):
        for x in self.objects:
            if isinstance(x, Player):
                return x

    def add(self, obj):
        self.objects[obj] = True

    def to_string(self):
        ret = []
        for i, row in enumerate(self.grid, 2):
            rowstr = ''.join([x.chr if x.is_visible_for(self.player) else ' ' for x in row])
            ret.append(rowstr)
        return ret

    def paint(self, scr):
        for i, rowstr in enumerate(self.to_string(), 2):
            scr.addstr(i, 0, rowstr)
        #scr.refresh()

    def random_spot(self):
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        return (y, x)

    def random_tile(self, *funcs):
        while True:
            y, x = self.random_spot()
            tile = self.grid[y][x]
            if not funcs or all([f(tile) for f in funcs]):
                return tile

    def __getitem__(self, z):
        if isinstance(z, int):
            return self.grid[z]
        elif isinstance(z, tuple) and len(z) == 2:
            return self.grid[z[0]][z[1]]

    def handle_control(self, key):
        pass

    def move_obj(self, obj, y, x):
        if self.grid[y][x].layers & Layers.OBSTACLE:
            return False
        self[obj.y][obj.x].remove(obj)
        obj.move(y, x)
        self[y][x].add(obj)
        return True


class Entity:
    feature_char = ' '
    layers = Layers.NONE

    def __init__(self, world, y=None, x=None):
        self.world = world
        self.x = x
        self.y = y

    @property
    def chr(self):
        return self.feature_char

    @property
    def pos(self):
        return P(self.x, self.y)


class LightSource:
    lights = []

    def __init__(self, owner=None, lrange=0, **kwargs):
        self._owner = owner
        self._range = lrange
        self._is_lit = kwargs.get('is_lit', False)

        self.__class__.lights.append(self)

    @property
    def position(self):
        if self.owner:
            return self.owner.y, self.owner.x
        return None

    @property
    def range(self):
        return self._range

    @property
    def owner(self):
        return self._owner

    @property
    def lit(self):
        return self._is_lit

    @lit.setter
    def lit(self, value):
        self._is_lit = value


class Tile:
    feature_char = '.'

    def __init__(self, world, y, x):
        self.features = []
        self.x = x
        self.y = y
        self.world = world

    @property
    def is_illuminated(self):
        if self.world.ambient:
            return True
        for light in LightSource.lights:
            if light.owner and light.lit and self.distance(light.owner) <= light._range:
                return True

    def is_visible_for(self, obj):
        return self.world.line_of_sight(obj.pos, self.pos)

    def is_empty(self):
        return self.features == []

    def has(self, cls):
        return cls in map(type, self.features)

    def get(self, cls):
        for c in self.features:
            if isinstance(c, cls):
                return c
        return None

    def distance(self, other):
        return distance(self.pos, other.pos)

    @property
    def pos(self):
        return P(self.x, self.y)

    @property
    def chr(self):
        if self.is_illuminated:
            if self.features:
                return self.features[-1].chr
            else:
                return self.feature_char
        else:
            return ' '

    def add(self, *objs):
        for obj in objs:
            obj.x = self.x
            obj.y = self.y
            self.world.add(obj)
        self.features.extend(objs)

    def remove(self, *objs):
        for obj in objs:
            if obj in self.features:
                self.features.remove(obj)

    @property
    def layers(self):
        ret = 0
        for x in self.features:
            ret |= x.layers
        return ret

class Player(Entity):
    feature_char = '@'

    def __init__(self, world, y=None, x=None):
        super().__init__(world, y, x)
        self.light = LightSource(self, 12)
        self.light.lit = True
        self.world = world
        self.x = x
        self.y = y

    def handle_control(self, key):
        if chr(key) in DIRS:
            dx, dy = DIRS[chr(key)]
            newx = self.x + dx
            newy = self.y + dy

            if not self.world.move_obj(self, newy, newx):
                if self.world[newy, newx].has(Lamp):
                    self.world[newy, newx].get(Lamp).light.lit = False
                    msg("Ouch! You wreck the lamp! It gets dark.")
                else:
                    msg("Ouch!")

    def move(self, y, x):
        self.y = y
        self.x = x


class Tree(Entity):
    feature_char = '#'
    layers = Layers.OBSTACLE

    def __init__(self, world, y=None, x=None):
        super().__init__(world, y, x)


class Lamp(Entity):
    feature_char = '¤'
    layers = Layers.OBSTACLE

    def __init__(self, world, y=None, x=None):
        super().__init__(world, y, x)
        self.light = LightSource(self, 7)
        self.light.lit = True


def main(stdscr):
    global STDSCR
    STDSCR = stdscr
    curses.curs_set(0)
    stdscr.clear()
    X = 33
    Y = 11

    world = World()
    player = Player(world, Y, X)
    world[Y][X].add(player)

    while True:
        world.paint(stdscr)
        key = stdscr.getch()
        if key == 27:
            stdscr.nodelay(True)
            _ = stdscr.getch()
            break
        else:
            msg(None)
            world.handle_control(key)
            player.handle_control(key)

"""
X = 33
Y = 11
world = World()
player = Player(world, Y, X)
world[Y][X].add(player)
z = world.to_string()
for x in z:
    print(x)
"""

wrapper(main)
