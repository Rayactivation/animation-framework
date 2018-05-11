import os, sys
import argparse
import json

IN_LINE_SPACING=1.312

parser = argparse.ArgumentParser()
parser.add_argument(
    '-o',
    '--output_file',
    dest='output_file',
    default='block_ray_layout.json',
    action='store',
    type=str,
    help='json file to output to. Will be overwritten')
parser.add_argument(
    '--scale',
    dest='scale',
    default=20,
    action='store',
    type=float)
"""
parser.add_argument(
    '--invertX',
    dest='invertX',
    default=True,
    action='store',
    type=bool)
parser.add_argument(
    '--invertY',
    dest='invertY',
    default=True,
    action='store',
    type=bool)
"""

options = parser.parse_args()
filename = options.output_file
SCALE = options.scale

ADDRESS="10.0.0.32"

Z_BASE = 120

def generate_box(strip_offset=0):
    X_CENTER = 10*12
    Y_START = -3*12
    Y_STEP = IN_LINE_SPACING
    return [
        {
            "address": ADDRESS,
            "strip": strip+strip_offset,
            "strip_index": stripidx,
            "point": [strip*4+X_CENTER, Z_BASE, Y_START + stripidx*Y_STEP],
            "section": "body"
        }
        for strip in range(-9,9+1) for stripidx in range(126)
    ]

def generate_tail(strip_offset=0):
    X_CENTER = 10 * 12

    Y_START = -3 * 12
    Y_STEP = -IN_LINE_SPACING

    STRIP_LENGTH = 64

    lights = []
    for strip in range(-9, 9+1):
        X_START = strip * 4 + X_CENTER
        X_END = strip * 4.0 / 6 + X_CENTER
        X_STEP = (X_END - X_START) / STRIP_LENGTH
        lights += [
            {
                "address": ADDRESS,
                "strip": strip + strip_offset,
                "strip_index": stripidx,
                "point": [strip * 4 + X_CENTER + X_STEP * stripidx, Z_BASE, Y_START + stripidx * Y_STEP],
                "section": "tail"
            }
            for stripidx in range(STRIP_LENGTH)
        ]
    return lights

def generate_wing(inverse, strip_offset=0):
    INVERSE_MULT = -1 if inverse else 1

    X_START = 10*12 + INVERSE_MULT*3*12
    X_STEP = INVERSE_MULT * IN_LINE_SPACING
    MAX_LENGTH = 64 #leds
    Z_STEP = IN_LINE_SPACING/4 #1:4 height

    Y_CENTER = 4.5*12
    return [
        {
            "address": ADDRESS,
            "strip": strip+strip_offset,
            "strip_index": stripidx,
            "point": [X_START + (stripidx+1)*X_STEP, Z_BASE+stripidx*Z_STEP, Y_CENTER+strip*4],
            "section": "wing-"+("inside" if inverse else "outside")
        }
        for strip in range(-16, 16 + 1) for stripidx in range(MAX_LENGTH-abs(strip)*2)
    ]

lights = generate_box()+generate_tail(19) + generate_wing(False, 2*19) + generate_wing(True, 2*19+33)


with open(filename, 'w') as f:
    f.write(json.dumps(lights, indent=True))