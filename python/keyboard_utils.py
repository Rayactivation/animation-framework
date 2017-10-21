from threading import Thread
from time import sleep

import traceback
import osc_utils
from state import STATE

def start_keyboard_thread(framework):
    keyboard_thread = Thread(
        target=listen_for_keyboard, args=(framework, ), name="KeyboardListeningThread")
    keyboard_thread.setDaemon(True)
    keyboard_thread.start()

def listen_for_keyboard(scene):
    # SceneManager -> None
    osc_client = osc_utils.get_osc_client()
    keep_running = True
    while keep_running:
        try:
            key = raw_input("Send a keyboard command: ")
            if not key:
                continue
            key_lower = key.lower()
            if ("quit" == key_lower):
                # TODO: We should really use atexit for all this. This is
                # a short-term fix to not take down the simulator with us
                print "Received shutdown command. Exiting now"
                scene.shutdown()
                keep_running = False
            elif key_lower.startswith("next"):
                # Increment one or more scenes
                args = key_lower.split(" ")
                if len(args) > 1:
                    osc_utils.send_simple_message(osc_client, "/scene/next", [args[1]])
                else:
                    osc_utils.send_simple_message(osc_client, "/scene/next")
            elif key_lower.startswith("scene "):
                args = key_lower.split(" ", 1)
                osc_utils.send_simple_message(osc_client, "/scene/select", [args[1]])
            elif key_lower.startswith("disable ") or key.startswith("enable "):
                # Accepts disable (simulator|arduino|*) [b_id]
                args = key_lower.split(" ", 2)
                enabled = args[0] == "enable"
                if len(args) == 3:
                    STATE.stations.change_client_status(
                        enabled=enabled, client_type=args[1], station_id=int(args[2]))
                elif len(args) == 2:
                    STATE.stations.change_client_status(enabled=enabled, client_type=args[1])
            else:
                args = key.split(" ")
                if len(args) == 1:
                    osc_utils.send_simple_message(osc_client, args[0])
                elif len(args) >= 2:
                    osc_utils.send_simple_message(osc_client, args[0], args[1:])
        except:
            traceback.print_exc()

        sleep(.1)