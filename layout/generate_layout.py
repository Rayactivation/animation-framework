import os, sys
import argparse
import json

NUM_LIGHTS_IN_LONG_STRIP = 126
IN_LINE_SPACING=1.0/30

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
    default=12,
    action='store',
    type=int)


options = parser.parse_args()

filename = options.output_file if options.output_file else 'new_layout_{}.json'.format(options.num_long_strips)

lights = [
    {
        #TODO: use properties... "address" : "${server.1}",
        "address" : "10.0.0.32",
        "point": [i*IN_LINE_SPACING, s*1, 0], # Force spacing into a bad grid for now
        "strip" : s,
        "strip_index" : i
    }
    for s in range(options.num_long_strips) for i in range(NUM_LIGHTS_IN_LONG_STRIP) 
]

with open(filename, 'w') as f:
    f.write(json.dumps(lights, indent=True))