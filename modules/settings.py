def set_biome_webhook_url(value):
	with open("settings/biome_webhook_url", "w") as f:
		f.write(value)

def get_biome_webhook_url():
	content = ""
	try:
		with open("settings/biome_webhook_url", "r") as f:
			content = f.read()
	except FileNotFoundError:
		content = ""
	return content

def set_ps_link(value):
	with open("settings/ps_link", "w") as f:
		f.write(value)

def get_ps_link():
	content = ""
	try:
		with open("settings/ps_link", "r") as f:
			content = f.read()
	except FileNotFoundError:
		content = ""
	return content