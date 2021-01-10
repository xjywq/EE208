import os

from bitarray import bitarray
import numpy as np

from .config import *


def square_dist(x, y):
    """ normal distance function """
    diff = np.array(x) - np.array(y)
    return np.dot(diff, diff)


def hamming_dist(x, y):
    """ hamming distance function """
    diff = bitarray(x) ^ bitarray(y)
    return diff.count()
