from datetime import datetime
import sys

class Logger:
    def __init__(self, filename):
        self.log = open(filename, "w")
        self.terminal = sys.__stdout__ if sys.__stdout__ is not None else sys.stdout
        if self.terminal is None:
            # no console, fallback to something dumb that just swallows writes
            class Dummy:
                def write(self, msg): pass
                def flush(self): pass
            self.terminal = Dummy()
        print("[Logger]: Created logger")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()
    def flush(self):
        self.terminal.flush()
        self.log.flush()

def log(text):
	now = datetime.now()
	formatted = now.strftime("%H:%M:%S.") + f"{int(now.microsecond / 1000):03d}"
	print("["+formatted+"]: "+text)