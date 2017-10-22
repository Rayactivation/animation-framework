import collections

import numpy as np

_GROUPBY = ["address", "strip", "strip_index"]

ROWS = 126
COLUMNS = 12


class Layout(object):

    def __init__(self, pixels, rows=ROWS, columns=COLUMNS):
        self.pixels = pixels
        self.n_pixels = len(pixels)
        self.rows = rows
        self.columns = columns
        self.shape = (rows, columns)
        self.grid = np.zeros((rows, columns), np.int)

        for attr in _GROUPBY:
            setattr(self, attr, collections.defaultdict(list))

        for i, pixel in enumerate(self.pixels):
            self.grid[pixel['strip_index'], pixel['strip']] = i
            for attr in _GROUPBY:
                getattr(self, attr)[pixel[attr]].append(i)

        # reset the defaultdicts to normal dictionaries
        for attr in _GROUPBY:
            setattr(self, attr, {k: v for k, v in getattr(self, attr).items()})

    def colmod(self, i):
        return divmod(i, self.columns)[1]
