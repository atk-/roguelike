from utils import Point as P
import random
from math import sqrt
from collections import namedtuple

P = namedtuple('Point', ['x', 'y'])

strs = ['foo', 'bar', 'xyz', 'zyx', 'åäö', 'qwe', 'zzz', 'rty', '123']

z = [str(a + b + c) for a in strs for b in strs for c in strs]
print(len(z))
