import random, math
from animation_framework.model import Effect, Scene, MultiEffect
from animation_framework.state import STATE

class SolidBackground(Effect):
    """Always return a singular color. Can be bound top/bottom and
    left-right (wrap-around not supported yet)
    """

    def __init__(self, color=(255, 0, 0), start_col=0, end_col=None, start_row=0, end_row=None):
        Effect.__init__(self)
        self.color = color
        self.slice = (slice(start_row, end_row), slice(start_col, end_col))
        print "Created with color", self.color


def printpixel(idx, pixel):
    print idx, pixel

def compute_pixel(pixels, idx, pix, cos_rad, sin_rad):
    point = pix['point']
    z_normalized = point[1]-120
    x_rotated = cos_rad*point[0] - sin_rad*point[2]
    y_rotated = sin_rad*point[0] + cos_rad*point[2]
    pixels[idx] = (abs(x_rotated), abs(y_rotated), z_normalized*10)

class Gradient(Effect):
    def __init__(self):
        super(Gradient, self).__init__()
        curmaxz=0
        for pix in STATE.layout.pixels:
            curmaxz = max(pix['point'][1], curmaxz)
        print "Max Z", curmaxz

    def next_frame(self, pixels, t):
        #map(printpixel, pixels)
        cos_rad = math.cos(t)
        sin_rad = math.sin(t)
        map(lambda (idx, pix): compute_pixel(pixels, idx, pix, cos_rad, sin_rad), enumerate(STATE.layout.pixels))

#    def is_completed(self, t):
 #       return random.randint(0,1)

SCENES = [
    Scene(
        name= "GradientExample",
        effects=[
            Gradient()
        ]
    )
]