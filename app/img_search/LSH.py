from collections import defaultdict
import os

import numpy as np

from .config import *
from .utils import *


class LSH:
    def __init__(self, hash_size: int, input_dim: int, hash_function=""):
        self.hash_size = hash_size
        self.input_dim = input_dim
        self.hash_function = hash_function or "hamming"
        self.dict = defaultdict()
        self.d_function = square_dist if hash_function == "dot" else hamming_dist
        self.hamming_table = np.random.randint(1, input_dim, hash_size)
        self.uniform_planes = np.random.randn(self.hash_size, self.input_dim)
        return

    def _hash(self, input_point):
        if self.hash_function == "dot":
            input_point = np.array(input_point)
            project = np.dot(self.uniform_planes, input_point)
            return "".join(['1' if i > 0 else '0' for i in project])
        else:
            hash_code = []
            for key in self.hamming_table:
                if key % 2 + 1 <= input_point[key]:
                    hash_code.append(1)
                else:
                    hash_code.append(0)
            return tuple(hash_code)

    def index(self, input_point: list, input_data=None):
        point = tuple(input_point)
        if not input_data:
            input_data = input_point
        self.dict.setdefault(self._hash(input_point), []).append((point, input_data))

    def query(self, query_point, max_results=5):
        """ return the search answer to the query and the distance """
        candidates = list()
        binary_hash = self._hash(query_point)
        candidates += self.dict.get(binary_hash, [])

        candidates = [(ix, self.d_function(query_point, ix[0]))
                      for ix in candidates]
        candidates.sort(key=lambda x: x[1])
        return candidates[:max_results]

    def load(self):
        dic, extend = np.load(LSH_INDEX_NAME + '.npy', allow_pickle=True)
        self.dict = dic
        if self.hash_function == 'hamming':
            self.hamming_table = extend
        else:
            self.uniform_planes = extend

    def save(self):
        extend = self.hamming_table if self.hash_function == 'hamming' else self.uniform_planes
        np.save(LSH_INDEX_NAME + '.npy', (self.dict, extend))
        return
