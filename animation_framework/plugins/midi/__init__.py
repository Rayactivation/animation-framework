from __future__ import absolute_import
import animation_framework.plugins.midi.midi_utils

def configure_parser(parser, *args, **kwargs):
    parser.add_argument('--midi-port', dest='midi_port', default=None, action='store')
    parser.add_argument('--midi-port-virtual', dest='midi_port_virtual', default=None, action='store')
    parser.add_argument('--midi-backend', dest='midi_backend', default='mido.backends.rtmidi_python', action='store')

def register_listeners(config, *args, **kwargs):
    midi_utils.listen_for_midi(config.midi_backend, config.midi_port, config.midi_port_virtual)
