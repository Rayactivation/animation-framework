import mido
from threading import Thread
from collections import namedtuple

from animation_framework import osc_utils

bass=36

tom_1 = 48
tom_2 = 47
floor_tom = 43

cymble_crash_bell = 55
cymble_crash_crash = 49
cymble_crash_hit = 59

cymble_ride_bell = 53
cymble_ride_crash = 52
cymble_ride_hit = 51

snare_hit = 38
snare_cross = 37 
snare_rim = 40

closed_hit_high_hat = 42
closed_crash_high_hat = 86
open_hit_high_hat = 46
open_crash_high_hat = 85
high_hat_close=44

def listen_for_midi():
    mido.set_backend(name='mido.backends.rtmidi_python', load=True)

    midi_thread = Thread(target=_forward_midi, name="MidoListeningThread")
    midi_thread.setDaemon(True)
    midi_thread.start()

def _forward_midi():
    osc_client = osc_utils.get_osc_client()
    with mido.open_input() as midi_in:
        for msg in midi_in:
            if msg.type in ['note_on'] and msg.velocity > 0:
                osc_utils.send_simple_message(osc_client, path="/input/midi", data=[msg.type, msg.note, msg.velocity])

DrumHit = namedtuple("DrumHit", ["note", "velocity"])
