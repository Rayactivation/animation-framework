import mido

#mido.set_backend('mido.backends.rtmidi_python')
mido.set_backend('mido.backends.rtmidi')
#mido.set_backend('mido.backends.portmidi')

with mido.open_output('fake_drums', virtual=True) as midi_out:
    keep_going=True
    while keep_going:
        key = raw_input("Send a keyboard command: ")
        if not key:
            print "Enter a note, 'note,velocity', or 'quit'"
            continue
        key_lower = key.lower()
        if ("quit" == key_lower):
            keep_going=False
            print "Exiting..."
        else:
            split_keys =  key_lower.split(',')
            try:
                asInts = map(lambda x: int(x), split_keys)
                print asInts
                if(len(split_keys)==1):
                    midi_out.send(mido.Message('note_on', note=asInts[0]))
                elif(len(split_keys) == 2):
                    midi_out.send(mido.Message('note_on', note=asInts[0], velocity=asInts[1]))
                else:
                    print "Enter a note, 'note,velocity', or 'quit'"
            except:
                print "An error occurred."
                print "Enter a note, 'note,velocity', or 'quit'"