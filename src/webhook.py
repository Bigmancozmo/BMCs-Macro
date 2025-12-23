import requests, threading, json, time
from io import BytesIO
from PIL import Image
import util

from vars import VERSION, DISCORD_INVITE, COLORS

WEBHOOK = "https://discord.com/api/webhooks/1445951285739389010/hgzgaDMYNsw-gOSylO6EJFCdGUGfXyGTLfRriVU18IOJPqgOZ-xEvWDFh_T80OzzJ-Id"
VERSION_TEXT = f"BMC's Macro | {VERSION}"

DISCORD_FIELD = {
	"name": "Discord Server",
	"value": DISCORD_INVITE
}

def getTimestampField():
	return {
		"name": "Timestamp",
		"value": f'<t:{int(time.time())}:R>'
	}

def sendMessage(data):
	threading.Thread(target=requests.post, args=(WEBHOOK,), kwargs={"json": data}).start()

def startMessage():
	sendMessage({
		"embeds": [
			{
				"description": "# Macro Started",
				"color": COLORS["green"],
				"fields": [DISCORD_FIELD, getTimestampField()],
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
				"fields": [DISCORD_FIELD, getTimestampField()],
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
				"fields": [DISCORD_FIELD, getTimestampField()],
				"footer": {
					"text": VERSION_TEXT
				}
			}
		],
	})

def averageNonWhites(url):
	response = requests.get(url)
	img = Image.open(BytesIO(response.content)).convert("RGB")
	pixels = list(img.getdata())

	non_white = [p for p in pixels if p != (255, 255, 255)]

	if non_white:
		avg = tuple(sum(c[i] for c in non_white)//len(non_white) for i in range(3))
		return avg
	else:
		return (255, 255, 255)

def getBiomeStuff(name, imageID):
	imageReq = requests.get(f'https://thumbnails.roblox.com/v1/assets?assetIds={imageID}&size=150x150&format=Png&isCircular=false')
	imageUrl = ""
	r, g, b = (0, 0, 0)
	if imageReq.status_code == 200:
		if len(imageReq.json()["data"]) > 0:
			imageUrl = imageReq.json()["data"][0]["imageUrl"]
			r, g, b = averageNonWhites(imageUrl)
	
	discord_color = util.pack_rgb(r, g, b)

	with open(util.resource_path("data/biomeColors.json"), "r") as f:
		data = json.load(f)
		if name in data:
			r, g, b = util.hex_to_rgb(data[name])
			discord_color = util.pack_rgb(r, g, b)
	
	return (imageUrl, discord_color)

def sendBiomeEnd(name, imageID):
	imageUrl, discord_color = getBiomeStuff(name, imageID)
	sendMessage({
		"embeds": [
			{
				"description": "# <:icons_dleave:875754473023229972> " + name + " ended",
				"color": discord_color,
				"fields": [DISCORD_FIELD, getTimestampField()],
				"footer": {
					"text": VERSION_TEXT
				},
				"thumbnail": {
					"url": imageUrl
	  			}
			}
		],
	})

def sendBiomeStart(name, imageID):
	imageUrl, discord_color = getBiomeStuff(name, imageID)

	sendMessage({
		"embeds": [
			{
				"description": "# <:icons_djoin:875754472834469948> " + name + " started",
				"color": discord_color,
				"fields": [DISCORD_FIELD, getTimestampField()],
				"footer": {
					"text": VERSION_TEXT
				},
				"thumbnail": {
					"url": imageUrl
	  			}
			}
		],
	})
