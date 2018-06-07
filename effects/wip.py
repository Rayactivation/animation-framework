from __future__ import absolute_import

import random, math
from animation_framework.model import Effect, Scene, MultiEffect
from animation_framework.state import STATE
import animation_framework.experimental.color_utils as CU

#TODO - Move to state
#RAY_ROTATION_RATE = -2 * math.pi / 40.0
RAY_ROTATION_RATE = 1

class SolidBoom(Effect):
    """Always return a singular color. Can be bound top/bottom and
    left-right (wrap-around not supported yet)
    """

    def __init__(self,
                 color=(128, 128, 128)
                 #color=(0,0,0)
        ):
        Effect.__init__(self)
        self.color = color

    def next_frame(self, pixels, t):
        pixels[STATE.layout.section['boom']] = self.color
        pixels[STATE.layout.section['pole']] = self.color

def blue_green(pixels, idx, point, cos_rad, sin_rad):
    pixels[idx] = (
        0,
        point[1] * 3,
        100)

def purple_fade(pixels, idx, point, cos_rad, sin_rad):
    x_rotated = cos_rad*point[0] - sin_rad*point[2]
    y_rotated = sin_rad*point[0] + cos_rad*point[2]
    pixels[idx] = (
        min(255,abs(x_rotated)),
        0,
        min(255, abs(y_rotated)))


def purple_fade_z(pixels, idx, point, cos_rad, sin_rad):
    x_rotated = cos_rad*point[0] - sin_rad*point[2]
    y_rotated = sin_rad*point[0] + cos_rad*point[2]
    pixels[idx] = (
        min(255,abs(x_rotated)),
        point[1]*3,
        min(255, abs(y_rotated)))


class Gradient(Effect):
    def __init__(self, fun):
        super(Gradient, self).__init__()
        self.frames_per_period = len(STATE.layout.pixels[0]['points'])
        self.fun = fun


    def next_frame(self, pixels, t):
        cos_rad = math.cos(t*RAY_ROTATION_RATE)
        sin_rad = math.sin(t*RAY_ROTATION_RATE)
        frame = int(t*STATE.fps) % self.frames_per_period
        map(lambda (idx, pix): self.fun(pixels, idx, pix['points_normalized'][frame], cos_rad, sin_rad), enumerate(STATE.layout.pixels))



class Rainbow(Gradient):
    def __init__(self, size=1000, hue_start=0, hue_end=255, saturation=255, value=255):
        super(Rainbow, self).__init__(self.draw_rainbow)
        self.frames_per_period = len(STATE.layout.pixels[0]['points'])
        self.rainbow = CU.bi_rainbow(size+1, hue_start, hue_end, saturation, value)
        self.scale = size/(2*math.pi)
        self.size=size

    def draw_rainbow(self, pixels, idx, point, cos_rad, sin_rad):
        x_rotated = cos_rad*point[0] - sin_rad*point[2]
        y_rotated = sin_rad*point[0] + cos_rad*point[2]
        theta = math.atan2(x_rotated, y_rotated)+math.pi
        pixels[idx] = self.rainbow[self.remap(theta)]

    def remap(self, theta):
        #INVERT
        return int(self.size-self.scale*theta)

SCENES = [
    Scene(
        name= "BlueGreen",
        effects=[
            Gradient(blue_green),
            SolidBoom()
        ]
    ),
    Scene(
        name= "PurpleFade",
        effects=[
            Gradient(purple_fade),
            SolidBoom()
        ]
    ),
    Scene(
        name= "PurpleFadeZ",
        effects=[
            Gradient(purple_fade_z),
            SolidBoom()
        ]
    ),
    Scene(
        name= "Rainbow",
        effects=[
            Rainbow(),
            SolidBoom()
        ]
    )
]