from datetime import datetime
import sys

class Logger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w")
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