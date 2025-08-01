auras = {}

CURRENT_BIOME = "Normal" # TODO

def setup(json):
	global auras
	auras = json

def getAuraData(aura):
	if aura in auras:
		data = auras[aura]
		if "biome" in data:
			if data["biome"] == CURRENT_BIOME:
				return {
					"text": "default",
					"rarity": data.native
				}
		if data["rarity"] == 0:
			return {
				"text": "Special Aura",
				"rarity": 0
			}
		return {
			"text": "default",
			"rarity": data["rarity"]
		}
	else:
		return {
			"text": "Unknown aura",
			"rarity": 0
		}