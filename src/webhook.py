import requests, threading

from vars import VERSION, DISCORD_INVITE, COLORS

WEBHOOK = "https://discord.com/api/webhooks/1445951285739389010/hgzgaDMYNsw-gOSylO6EJFCdGUGfXyGTLfRriVU18IOJPqgOZ-xEvWDFh_T80OzzJ-Id"
VERSION_TEXT = f"BMC's Macro | {VERSION}"

def sendMessage(data):
	threading.Thread(target=requests.post, args=(WEBHOOK,), kwargs={"json": data}).start()

def startMessage():
	sendMessage({
		"embeds": [
			{
				"description": "# Macro Started",
				"color": COLORS["green"],
				"fields": [
					{
						"name": "Discord Server",
						"value": DISCORD_INVITE
					}
				],
				"footer": {
					"text": VERSION_TEXT
				}
			}
		],
	})

def macroClosed():
	sendMessage({
		"embeds": [
			{
				"description": "# Application Closed",
				"color": COLORS["red"],
				"footer": {
					"text": VERSION_TEXT
				}
			}
		],
	})

def stopMessage():
	sendMessage({
		"embeds": [
			{
				"description": "# Macro Stopped",
				"color": COLORS["red"],
				"fields": [
					{
						"name": "Discord Server",
						"value": DISCORD_INVITE
					}
				],
				"footer": {
					"text": VERSION_TEXT
				}
			}
		],
	})
