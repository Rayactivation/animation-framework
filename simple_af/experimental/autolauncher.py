import argparse
import json
import logging
import OSC
from time import sleep
from subprocess import Popen, check_call
import simple_af.launcher
from simple_af.osc_utils import create_osc_server

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(parents=[simple_af.launcher.get_command_line_parser(add_help=False)])
parser.add_argument(
    '-a',
    '--address',
    dest='address',
    default='0.0.0.0',
    action='store',
    type=str,
    help='server address to receive OSC messages on')
parser.add_argument(
    '-p',
    '--port',
    dest='port',
    default=6000,
    action='store',
    type=int,
    help='port to receive OSC messages on')
parser.add_argument(
    '-c',
    '--cmd',
    dest='command',
    action='store',
    type=str,
    help='command to run',
    required=True)

options = parser.parse_args()

server = create_osc_server(host=options.address, port=options.port)
print "Started OSC server at {}:{}".format(options.address, options.port)


class GitProcessLauncher(object):
    def __init__(self):
        self.proc = None
        self.KEEP_RUNNING=True

    def _poll_process(self):
        if self.proc:
            returncode = self.proc.poll()
            if returncode is not None:
                #TODO use return code somehow
                self.proc = None


    def do_pull(self):
        '''Pull from github and restart the process'''
        self.do_stop()
        print('Pulling from github')
        check_call(['git','pull'])
        print('Pulled from github')
        self.do_start()

    def do_stop(self):
        self._poll_process()
        if self.proc:
            '''
            This is python 3 code but we're on 2 for now so just kill
            try:
                self.proc.communicate(input='quit', timeout=5000)
            except TimeoutExpired:
                print "Stop command timeout. Exceuting kill command now"
                self.proc.kill()
            self._poll_process()
            '''
            print("Killing process")
            self.proc.kill()
            self._poll_process()
            for i in range(5):
                if self.proc:
                    print("Processing still running, sleeping")
                    sleep(1)
                else:
                    print "Process killed"
                    return
            print("Process did not stop")
        else:
            print "Process was not running. Stop not executed"

    def do_start(self):
        self._poll_process()
        if self.proc:
            raise Exception("Process already running?")

        # This is sketchy. create the process based on the command line passed in.
        # This will likely just be a "launch.sh" script configured in the server so it can be pulled down as well
        self.proc = Popen(options.command)

    def do_restart(self):
        self.do_stop()
        self.do_start()

    def terminate_completely(self):
        try:
            self.do_stop()
        finally:
            self.KEEP_RUNNING = False


handle = GitProcessLauncher()


def terminate_service(path, tags, args, source):
    handle.terminate_completely()

server.addMsgHandler("/service/stop", terminate_service)

actions = {
    "start":handle.do_start,
    "stop":handle.do_stop,
    "restart":handle.do_restart,
    "update":handle.do_pull
}


def handle_action(path, tags, args, source):
    action = args[0].lower()
    print("Doing action {}".format(action))
    actions[action]()

server.addMsgHandler("/action", handle_action)

handle.do_start()
while handle.KEEP_RUNNING:
    sleep(1)