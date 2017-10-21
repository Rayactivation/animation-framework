import mido
import OSC

mido.set_backend('mido.backends.rtmidi_python')

client = OSC.OSCClient()

with mido.open_input() as midi_in:
    for msg in midi_in:
        if msg.type in ['note_on'] and msg.velocity > 0:
            print msg
