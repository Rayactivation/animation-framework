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
            

    """
    def colmod(self, i):
        return divmod(i, self.columns)[1]
    """

    def annotate(config, framework):
        print "Registering listeners..."
        for ep in pkg_resources.iter_entry_points('simple_af.plugins.listeners'):
            print "Registering", ep
            listener = ep.load()(config, framework)
