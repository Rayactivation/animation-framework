#!/usr/bin/env python

from __future__ import division
import argparse
import json
import logging
from multiprocessing import Process
import os
import sys

import animation_framework.framework as AF
from animation_framework.layout import Layout
from animation_framework import opc
from animation_framework import osc_utils
from animation_framework import keyboard_utils
#from animation_framework import midi_utils
from animation_framework.state import STATE
from animation_framework import utils

logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------
# command line
def get_command_line_parser(add_help=True):
    root_dir = find_root()

    parser = argparse.ArgumentParser(add_help=add_help)
    parser.add_argument(
        '-l',
        '--layout',
        dest='layout_file',
        # CHANGE ME
        default=os.path.join(root_dir, 'layout', 'block_ray_layout.json'),
        action='store',
        type=str,
        help='layout file')
    parser.add_argument(
        '-s',
        '--servers',
        dest='servers',
        default=os.path.join(root_dir, 'layout', 'servers_local.json'),
        action='store',
        type=str,
        help='json file for server addresses')
    parser.add_argument(
        '-n',
        '--scene',
        dest='scene',
        default=None,
        action='store',
        type=str,
        help='First scene to display')
    parser.add_argument(
        '-f', '--fps', dest='fps', default=30, action='store', type=int, help='frames per second')
    parser.add_argument('-v', '--verbose', dest='verbose', default=False, action='store_true')
    parser.add_argument('--midi-port', dest='midi_port', default=None, action='store')
    parser.add_argument('--midi-port-virtual', dest='midi_port_virtual', default=None, action='store')
    parser.add_argument('--midi-backend', dest='midi_backend', default='mido.backends.rtmidi_python', action='store')

    return parser


def parse_command_line(args=None):
    parser = get_command_line_parser()
    return parser.parse_args(args), parser

def consume_config(options, parser):
    log_level = 'DEBUG' if options.verbose else 'INFO'
    utils.configure_logging(level=log_level)

    if not options.layout_file:
        parser.print_help()
        print
        print('ERROR: you must specify a layout file using '
              '--layout or use default (../layout/hoeLayout.json)')
        print
        sys.exit(1)

    STATE.layout = Layout(parse_json_file(options.layout_file))
    STATE.servers = parse_json_file(options.servers)
    STATE.fps = options.fps
    STATE.verbose = options.verbose
    return options


def find_root(start_dirs=[], look_for=set(["layout", "animation_framework"])):
    # type: ([str], set([str])) -> str
    """
    Find the root directory of the project by looking for some common directories
    :return: the root directory
    """
    # Handle symlinks
    start_dirs = [] + [
        os.path.dirname(os.path.abspath(__file__)),
        os.path.dirname(os.path.realpath(__file__))
    ]
    for curr_dir in start_dirs:
        while curr_dir != os.path.dirname(curr_dir):
            curr_dir = os.path.dirname(curr_dir)
            if look_for.issubset(os.listdir(curr_dir)):
                print "    Found root directory of", curr_dir
                return curr_dir
    print "Could not find %s in parent dirs of %s. Root will be none" % (look_for, start_dirs)


def parse_json_file(filename):
    with open(filename) as f:
        return json.load(f)


def create_opc_client(server, verbose=False):
    client = opc.Client(server_ip_port=server, verbose=False)
    if client.can_connect():
        print '    connected to %s' % server
    else:
        # can't connect, but keep running in case the server appears later
        print '    WARNING: could not connect to %s' % server
    print
    return client


def init_animation_framework(osc_server, opc_client, first_scene=None):
    # type: (OSCServer, Client, [OSCClient], str) -> AnimationFramework
    mgr = AF.AnimationFramework(
        osc_server=osc_server, opc_client=opc_client, first_scene=first_scene)
    return mgr


def build_opc_client(verbose):
    if 'opc_server' in STATE.servers['remote']:
        return create_opc_client(server=STATE.servers["remote"]["opc_server"], verbose=verbose)
    else:
        clients = {}
        opc_servers = STATE.servers['remote']['opc_servers']
        if 'layout' in opc_servers:
            for server_ip_port in opc_servers['layout']:
                cl = create_opc_client(server_ip_port, verbose=verbose)
                clients[cl] = STATE.layout.address[cl.ip]  # pylint: disable=no-member
        if 'all' in opc_servers:
            client = create_opc_client(opc_servers['all'][0], verbose)
            clients[client] = range(STATE.layout.n_pixels)
        return opc.MultiClient(clients)




def launch(options=None, parser=None):
    config,parser = (options, parser) if options and parser else parse_command_line()
    print config, parser
    consume_config(config, parser)

    osc_server = osc_utils.create_osc_server(
        host=STATE.servers["hosting"]["osc_server"]["host"],
        port=int(STATE.servers["hosting"]["osc_server"]["port"]))
    opc_client = build_opc_client(config.verbose)

    framework = init_animation_framework(osc_server, opc_client, config.scene)

    keyboard_utils.launch_keyboard_thread(framework)

    #midi_utils.listen_for_midi(config.midi_backend, config.midi_port,config.midi_port_virtual)

    try:
        framework.serve_forever()
    except KeyboardInterrupt:
        print "Received interrupt. Stopping..."
    finally:
        framework.shutdown()
        opc_client.disconnect()
    # TODO: This was deadlocking
    # osc_server.shutdown()


if __name__ == '__main__':
    launch()
