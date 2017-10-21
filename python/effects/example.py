import random
from animation_framework.framework import Effect, Scene

class SolidBackground(Effect):
    """Always return a singular color. Can be bound top/bottom and
    left-right (wrap-around not supported yet)
    """

    def __init__(self, color=(255, 0, 0), start_col=0, end_col=None, start_row=0, end_row=None):
        Effect.__init__(self)
        self.color = color
        self.slice = (slice(start_row, end_row), slice(start_col, end_col))
        print "Created with color", self.color

    def next_frame(self, pixels, t):
        pixels[self.slice] = self.color

SCENES = [
    Scene(
        "solidwhite",
        effects=[SolidBackground(color=(30, 30, 30))]
    )
]