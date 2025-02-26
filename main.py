try:
	# Imports

	from tkinter import *
	from tkinter import ttk
	import tkinter.font as tkFont

	import ctypes, time, json, requests

	from widgets.root import Root
	from widgets.header import Header
	from widgets.text_input import TextInput

	import modules.settings as config
	from modules.biome_tracker import BiomeTracker

	from style.styler import style as s

	# Code

	print("Starting...")

	with open("data/biomes.json", "r") as file:
		biome_data = json.load(file)

	winW = s['width']
	winH = s['height']

	win = Tk()
	win.title("BMC's Macro")
	win.geometry(str(winW) + 'x' + str(winH) + '+300+120')
	win.configure(bg=s['outline'])
	win.resizable(False, False)
	win.attributes("-alpha", 0)

	print("Created tkinter window")

	font_black_16 = tkFont.Font(family="Sarpanch Black", size=16)
	font_bold_16 = tkFont.Font(family="Sarpanch Bold", size=16)
	font_extrabold_16 = tkFont.Font(family="Sarpanch ExtraBold", size=16)
	font_medium_16 = tkFont.Font(family="Sarpanch Medium", size=16)
	font_regular_16 = tkFont.Font(family="Sarpanch Regular", size=16)
	font_semibold_16 = tkFont.Font(family="Sarpanch SemiBold", size=16)
	print("Created fonts")

	tracker = BiomeTracker()

	def onBiomeChange(biome):
		whUrl = config.get_biome_webhook_url()
		server_join = "[Join Server](<https://google.com>)"
		if biome in biome_data:
			data = {
				"embeds": [
					{
						"title": "Biome Started",
						"description": "# Snowy\n" + server_join,
						"color": 13299967,
						"image": {
							"url": ""
						},
						"thumbnail": {
							"url": "https://raw.githubusercontent.com/Bigmancozmo/BMCs-Macro/refs/heads/main/data/img/Snowy.png"
						}
					}
				]
			}

			data["embeds"][0]["description"] = "# " + str(biome_data[biome]["name"]) + "\n" + server_join
			data["embeds"][0]["thumbnail"]["url"] = str(biome_data[biome]["image"])
			data["embeds"][0]["color"] = int(biome_data[biome]["color"])
			
			requests.post(whUrl, json=data)
		else:
			requests.post(whUrl, json={"content":"Biome without data spawned - " + biome + "\n" + server_join})

		print(biome)

	onBiomeChange("NORMAL")
	onBiomeChange("SNOWY")
	onBiomeChange("RAINY")
	onBiomeChange("WINDY")
	onBiomeChange("CORRUPTION")
	onBiomeChange("STARFALL")
	onBiomeChange("NULL")
	onBiomeChange("HELL")
	onBiomeChange("GLITCHED")
	onBiomeChange("DREAMSPACE")

	tracker.register_biome_change_callback(onBiomeChange)

	root = Root(win, s['width']-s['paddingSize']*2, s['height']-s['paddingSize']*2)
	root.place(x=s['paddingSize'],y=s['paddingSize'])
	Header(root, pady=8).pack()

	menu_frame_outer = Frame(root, bg=s['outline'], width=(s['width']-50), height=(s['height']-83))
	menu_frame_outer.pack_propagate(False)
	menu_frame_outer.pack()

	menu_frame_container = Root(menu_frame_outer, width=(s['width']-50-s['paddingSize']*2), height=(s['height']-83-s['paddingSize']*2))
	menu_frame_container.place(x=s['paddingSize'], y=s['paddingSize'])

	menu_frame = Frame(menu_frame_container, width=(s['width']-50-s['paddingSize']*2)-20, height=(s['height']-83-s['paddingSize']*2)-20, bg=s['bg'])
	menu_frame.place(x=10,y=10)

	def show_window():
		for i in range(10):
			win.attributes("-alpha", 0.1*i)
			time.sleep(0.03)
		win.attributes("-alpha", 1)

	def submit_biome_webhook(value):
		val = str(value)
		if val.find("https://discord.com/api/webhooks/") == -1:
			ctypes.windll.user32.MessageBoxW(0, "Invalid webhook URL! Change it, and try again.\nIf it remains invalid, the biome webhook will be disabled.", "Invalid Webhook", 0)
			return
		config.set_biome_webhook_url(val)
		ctypes.windll.user32.MessageBoxW(0, "Webhook updated!", "Success", 0)

	menu_frame.update_idletasks()
	# 35px y increment
	biome_webhook_input = TextInput(menu_frame, menu_frame.winfo_width(), height=10, optionName="Biome Webhook URL", clicked=submit_biome_webhook, entryPad=3, setText=config.get_biome_webhook_url())
	biome_webhook_input.place(x=0,y=0)

	print("Started!")
	win.after(1000, show_window)
	win.mainloop()
	print("Bye!")
	time.sleep(1)
except:
	import traceback
	with open("lastRun.log",'w') as a:
		a.write(traceback.format_exc())
else:
	with open("lastRun.log",'w') as a:
		a.write("OK")