import mido
from threading import Thread

from animation_framework import osc_utils
from animation_framework.framework import Effect

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
