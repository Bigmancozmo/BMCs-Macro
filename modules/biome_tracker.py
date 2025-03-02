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
	_current_log = None

	@staticmethod
	def find_latest_log():
		default_path = os.path.expandvars("%LOCALAPPDATA%") + "\\Roblox\\logs"
		packages_path = os.path.expandvars("%LOCALAPPDATA%") + "\\Packages"
		log_candidates = []
		
		if os.path.exists(default_path):
			log_files = glob.glob(os.path.join(default_path, "*.log"))
			if log_files:
				log_candidates.append(max(log_files, key=os.path.getctime))
		
		if os.path.exists(packages_path):
			for folder in os.listdir(packages_path):
				if "ROBLOX" in folder:
					log_path = os.path.join(packages_path, folder, "LocalState", "logs")
					if os.path.exists(log_path):
						log_files = glob.glob(os.path.join(log_path, "*.log"))
						if log_files:
							log_candidates.append(max(log_files, key=os.path.getctime))
		
		latest_log = max(log_candidates, key=os.path.getctime) if log_candidates else None
		return latest_log

	def trigger_callbacks(biomeName):
		for callback in BiomeTracker._callbacks:
			callback(biomeName)

	@staticmethod
	def __follow_log():
		while True:
			latest_log = BiomeTracker.find_latest_log()
			if latest_log != BiomeTracker._current_log:
				BiomeTracker._current_log = latest_log
				print(f"Switching to new log file: {latest_log}")
				
			with open(latest_log, "r", encoding="utf-8", errors="ignore") as f:
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
						if BiomeTracker.find_latest_log() != BiomeTracker._current_log:
							print("Detected new log file, switching...")
							break
			time.sleep(5)

	def __init__(self):
		if BiomeTracker._thread is None:
			BiomeTracker._thread = threading.Thread(target=BiomeTracker.__follow_log, daemon=True)
			BiomeTracker._thread.start()

	def register_biome_change_callback(self, callback):
		BiomeTracker._callbacks.append(callback)
