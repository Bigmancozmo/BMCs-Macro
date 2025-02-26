import os, time, glob, sys, json, threading
try:
	sys.stdout.reconfigure(encoding="utf-8")
except:
	print("Couldn't reconfigure console - are you using pythonw?")

class BiomeTracker:
	_thread = None
	_callbacks = []
	_biome = ""
	_last_biome = ""

	def get_latest_log():
		log_dir = os.path.expandvars("%LOCALAPPDATA%") + "\\Roblox\\logs"
		log_files = glob.glob(os.path.join(log_dir, "*.log"))
		return max(log_files, key=os.path.getctime) if log_files else None

	def trigger_callbacks(biomeName):
		for callback in BiomeTracker._callbacks:
			callback(biomeName)

	@staticmethod
	def __follow_log(log_path):
		with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
			f.seek(0, os.SEEK_END)
			while True:
				line = f.readline()
				if line:
					txt_coded = line.strip().encode("utf-8", "ignore").decode("utf-8")
					txt_split = txt_coded.split(" [BloxstrapRPC] ")
					if len(txt_split) >= 2:
						json_dec = json.loads(txt_split[1])
						if json_dec["command"] == "SetRichPresence":
							BiomeTracker._biome = json_dec["data"]["largeImage"]["hoverText"]
							if BiomeTracker._biome != BiomeTracker._last_biome:
								BiomeTracker.trigger_callbacks(BiomeTracker._biome)
							BiomeTracker._last_biome = BiomeTracker._biome
				else:
					time.sleep(1)

	def __init__(self):
		self.latest_log = BiomeTracker.get_latest_log()
		if self.latest_log:
			if BiomeTracker._thread is None:
				BiomeTracker._thread = threading.Thread(target=BiomeTracker.__follow_log, args=(self.latest_log,), daemon=True)
				BiomeTracker._thread.start()
	
	def register_biome_change_callback(self, callback):
		BiomeTracker._callbacks.append(callback)