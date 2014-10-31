from .exceptions import InvalidStateException

import os
from threading import Thread
import time

class StdinHandler(object):

    stdin_fifo_file_handle = None

    def __init__(self):
        self.stdin_fifo_file = '/tmp/gdbpwny.{}.stdin'.format(os.getpid())
        os.mkfifo(self.stdin_fifo_file)
        Thread(target=self.open_fifo).start()

    def open_fifo(self):
        print("open_fifo()")
        self.stdin_fifo_file_handle = open(self.stdin_fifo_file, 'w')

    def write(self, stdin_string, blocking=False):
        print("write({})".format(repr(stdin_string)))
        loop = True
        while loop:
            if self.stdin_fifo_file_handle:
                self.stdin_fifo_file_handle.write(stdin_string)
                self.stdin_fifo_file_handle.flush()
                loop = False
            elif not blocking:
                raise InvalidStateException("No stdin fifo handle. Probably need to run() first.")
            else:
                time.sleep(1)

    def close(self):
        if self.stdin_fifo_file_handle:
            self.stdin_fifo_file_handle.close()
        else:
            raise InvalidStateException("No stdin fifo handle. Probably need to run() first.")

    def get_path(self):
        return self.stdin_fifo_file
