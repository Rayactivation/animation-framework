import mido
import OSC

#mido.set_backend('mido.backends.rtmidi_python')
mido.set_backend('mido.backends.rtmidi')
#mido.set_backend('mido.backends.portmidi')

client = OSC.OSCClient()

print "Available input ports:", mido.get_input_names()
with mido.open_input('fake_drums') as midi_in:
    for msg in midi_in:
        #if msg.type in ['note_on'] and msg.velocity > 0:
            print msg
