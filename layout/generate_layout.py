import os, sys
import argparse
import json

NUM_LIGHTS_IN_LONG_STRIP = 126
IN_LINE_SPACING=.15
VERTICAL_SPACING=.1

parser = argparse.ArgumentParser()
parser.add_argument(
    '-o',
    '--output_file',
    dest='output_file',
    default='',
    action='store',
    type=str,
    help='json file to output to. Will be overwritten')
parser.add_argument(
    '-s',
    '--num_long_strips',
    dest='num_long_strips',
    default=8,
    action='store',
    type=int)
parser.add_argument(
    '--scale',
    dest='scale',
    default=20,
    action='store',
    type=float)
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

options = parser.parse_args()
SCALE = options.scale

INVERT_X = -1 if options.invertX else 1
INVERT_Y = -1 if options.invertY else 1

X_STEP = IN_LINE_SPACING*INVERT_X*SCALE
Y_STEP = VERTICAL_SPACING*INVERT_Y*SCALE

#TODO: These start at 0, so appear kind of offset, which is lame...
X_START = X_STEP * NUM_LIGHTS_IN_LONG_STRIP/2 * -1
Y_START = Y_STEP * options.num_long_strips/2 * -1


filename = options.output_file if options.output_file else 'new_layout_{}.json'.format(options.num_long_strips)

lights = [
    {
        #TODO: use properties... "address" : "${server.1}",
        "address" : "10.0.0.32",
        "point": [i*X_STEP+X_START, s*Y_STEP+Y_START, 0], # Force spacing into a bad grid for now
        "strip" : s,
        "strip_index" : i
    }
    for s in range(options.num_long_strips) for i in range(NUM_LIGHTS_IN_LONG_STRIP)
]

with open(filename, 'w') as f:
    f.write(json.dumps(lights, indent=True))