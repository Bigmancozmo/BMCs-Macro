from logging import warn, warning
from vars import DEFAULT_BIOME
import webhook
import os, time

def getLatestLogPath():
	logs = os.path.join(os.environ["LOCALAPPDATA"], "Roblox", "logs")
	latest = max(
		(os.path.join(logs, f) for f in os.listdir(logs)),
		key=os.path.getmtime
	)
	return latest

latestLog = getLatestLogPath()
lastLine = 0
lastBiome = DEFAULT_BIOME
lastImageID = 0

def handleLine(line):
	global lastBiome
	global lastImageID

	try: # who gives a fuck if it errors
		if "[BloxstrapRPC]" in line:
			biomeName = line.split('"hoverText":"')[2].split('","assetId')[0]
			imageId = line.split('","assetId":')[2][:-4]
			if biomeName != lastBiome:
				if lastBiome != DEFAULT_BIOME:
					webhook.sendBiomeEnd(lastBiome, lastImageID)
				if biomeName == DEFAULT_BIOME:
					return
				webhook.sendBiomeStart(biomeName, imageId)
				lastBiome = biomeName
				lastImageID = imageId
	except Exception as e:
		warning("Failed to read biome name")
		warning(e)

# Find the last BloxstrapRPC line and handle it, to know the starting biome.
with open(latestLog, "r", encoding="utf-8", errors="ignore") as f:
	lines = f.readlines()
	lastLine = len(lines)
	for line in reversed(lines):
		if "[BloxstrapRPC]" in line:
			handleLine(line)
			break

# Start the SPYWARE
while True:
	with open(latestLog, "r", encoding="utf-8", errors="ignore") as f:
		lines = f.readlines()
	newLines = lines[lastLine:]
	for line in newLines:
		handleLine(line)
	lastLine = len(lines)
	time.sleep(0.05)
