import collections

import numpy as np

_GROUPBY = ["address", "strip", "strip_index", "section"]

class Layout(object):

    def __init__(self, pixels):
        self.pixels = pixels
        self.n_pixels = len(pixels)
        self.grid = np.zeros(self.n_pixels, np.int)

        for attr in _GROUPBY:
            setattr(self, attr, collections.defaultdict(list))

        for i, pixel in enumerate(self.pixels):
            #self.grid[pixel['strip_index'], pixel['strip']] = i
            for attr in _GROUPBY:
                getattr(self, attr)[pixel[attr]].append(i)

        # reset the defaultdicts to normal dictionaries
        for attr in _GROUPBY:
            setattr(self, attr, {k: v for k, v in getattr(self, attr).items()})


        X_MAX=-1000
        X_MIN=1000
        Y_MAX=-1000
        Y_MIN=1000
        for idx, pixel in enumerate(pixels):
            if(pixel['section']=='boom' or pixel['section']=='pole'):
                continue
            for point in pixel['points']:
                X_MAX=max(point[0], X_MAX)
                X_MIN = min(point[0], X_MIN)
                Y_MAX = max(point[2], Y_MAX)
                Y_MIN = min(point[2], Y_MIN)

        Z_NORMAL = 12*13
        for pixel in pixels:
            pixel['points_normalized'] = [ [250*point[0]/X_MAX,point[1]-Z_NORMAL,250*point[2]/Y_MAX] for point in pixel['points']]

    """
    def colmod(self, i):
        return divmod(i, self.columns)[1]
    """