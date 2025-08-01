import ctypes
import customtkinter as tk
from pynput import mouse, keyboard
import threading, os, json, queue, time, sys, requests
import pyautogui as auto
from ahk import AHK
from datetime import datetime

import modules.questboard as qb
import modules.auraData as auraData
from logger import Logger, log
from updater import check_update

now = datetime.now()
formatted = now.strftime("%m-%d-%y %H-%M-%S")

os.makedirs("logs", exist_ok=True)
sys.stdout = sys.stderr = Logger("logs/" + formatted + ".log")

log("[main]: Starting up...")
log("[Auras]: Downloading aura file...")
AURA_FILE_URL = "https://raw.githubusercontent.com/Bigmancozmo/BMCs-Macro/refs/heads/main/auras.json"

def download_aura_file():
	response = requests.get(AURA_FILE_URL)
	if response.status_code == 200:
		with open("auras.json", "w", encoding="utf-8") as file:
			file.write(response.text)
		log("[Auras]: Downloaded new aura database")
	else:
		log("Failed to download aura database")
		file_exists = os.path.exists("auras.json")
		if file_exists:
			ctypes.windll.user32.MessageBoxW(0, "Failed to download aura database.\nKnown auras may be outdated!", "Error", 0x10)
		else:
			ctypes.windll.user32.MessageBoxW(0, "Failed to download aura database.\nIt appears you've never downloaded it before,\nso the macro cannot continue.", "Error", 0x10)
			log("Exiting..")
			sys.exit()

download_aura_file()

log("[main]: Loading auras...")
auraData.setup(json.loads(open("auras.json").read()))

log("[main]: Checking for updates...")
check_update()

status = "Idle"
coordinate_config_width = 420
GLOBAL_PAD = 4

ahk = AHK()
ahk.set_coord_mode('Mouse', 'Screen')

config_path = "config.json"
default_config = {
	"useAbyssalHunter": False,
	"invBtnPosX": 10,
	"invBtnPosY": 10,
	"invItemsTabPosX": 10,
	"invItemsTabPosY": 10,
	"genericCloseX": 10,
	"genericCloseY": 10,
	"collBtnX": 10,
	"collBtnY": 10,
	"collExitX": 10,
	"collExitY": 10,
	"invSearchX": 10,
	"invSearchY": 10,
	"invFirstItemSlotX": 10,
	"invFirstItemSlotY": 10,
	"itemUseBtnX": 10,
	"itemUseBtnY": 10,
	"auraEquipBtnX": 10,
	"auraEquipBtnY": 10,
	"autoEquipAura": "Common",

	# Questboard
	"qbTakeLuckyPotion": True,
	"qbTakeSpeedPotion": False,
	"qbTakeCoins": False,
	"qbRightBtnX": 10,
	"qbRightBtnY": 10,
	"qbClaimBtnX": 10,
	"qbClaimBtnY": 10,
	"qbDismissBtnX": 10,
	"qbDismissBtnY": 10,

	# Item use
	"useBR": False,
	"useSC": False,
}

if os.path.exists(config_path):
	with open(config_path, "r") as f:
		config = json.load(f)
	for k, v in default_config.items():
		if k not in config:
			config[k] = v
else:
	config = default_config.copy()

log("[main]: Loaded config")

def close_chat():
	ahk.run_script('''
		WinActivate, Roblox
		WinWaitActive, Roblox
		CoordMode, Mouse, Client
		MouseMove, 129, 27
	''')

	x, y = auto.position()
	color = auto.screenshot().getpixel((x, y))
	r, g, b = color
	if r > 230 and g > 230 and b > 230:
		auto.leftClick()

def get_click_coordinates():
	log("Click anywhere on the screen...")
	q = queue.Queue()
	root = tk.CTk()
	root.attributes("-fullscreen", True)
	root.attributes("-topmost", True)
	root.attributes("-alpha", 0.25)
	root.configure(fg_color="black")

	def on_click(x, y, button, pressed):
		if pressed:
			q.put((x, y))
			listener.stop()

	def start_listener():
		nonlocal listener
		listener = mouse.Listener(on_click=on_click)
		listener.start()

	def check_queue():
		try:
			x, y = q.get_nowait()
			root.coords = (x, y)
			root.quit()
			root.destroy()
		except queue.Empty:
			root.after(50, check_queue)

	listener = None
	threading.Thread(target=start_listener, daemon=True).start()
	root.after(50, check_queue)
	root.mainloop()

	return getattr(root, "coords", (None, None))

def save_settings():
	with open(config_path, "w") as f:
		json.dump(config, f)

def move_mouse(target_x, target_y):
	ahk.mouse_move(target_x, target_y)

def move_to_defined(posName):
	xValue = config[posName+"X"]
	yValue = config[posName+"Y"]
	move_mouse(xValue, yValue)
	time.sleep(0.1)

def click_pos(posName):
	move_to_defined(posName)
	auto.leftClick()
	time.sleep(0.3)

def on_key_press(key):
	try:
		if key == keyboard.Key.f1:
			app.event_generate("<<StartPressed>>")
		elif key == keyboard.Key.f3:
			app.event_generate("<<StopPressed>>")
	except:
		pass

def equip_aura(name):
	move_to_defined("invBtnPos")
	x, invY = auto.position()
	move_to_defined("collBtn")
	collX, collY = auto.position()
	yDiff = abs(invY-collY) # idk which order so we just absolute value it
	storageY = collY-yDiff

	move_mouse(x, storageY)
	auto.leftClick()
	time.sleep(0.3)

	click_pos("invSearch")
	ahk.send(name)
	click_pos("invFirstItemSlot")
	ahk.run_script("Loop 5\n{\nSend {WheelUp}\n}")
	time.sleep(1)
	click_pos("invFirstItemSlot")
	r, g, b = auto.screenshot().getpixel((config["auraEquipBtnX"], config["auraEquipBtnY"]))
	if g >= r:
		click_pos("auraEquipBtn")
	click_pos("genericClose")

def use_item(name):
	click_pos("invBtnPos")
	time.sleep(1)
	click_pos("invItemsTabPos")
	time.sleep(1)
	click_pos("invFirstItemSlot")
	ahk.run_script("Loop 5\n{\nSend {WheelDown}\n}")
	time.sleep(1)
	click_pos("invFirstItemSlot")
	click_pos("invSearch")
	ahk.send(name)
	click_pos("invFirstItemSlot")
	click_pos("itemUseBtn")
	click_pos("genericClose")
	time.sleep(1)

def hold_key(key, length):
	ahk.key_down(key)
	time.sleep(length)
	ahk.key_up(key)

def align_camera():
	click_pos("collBtn")
	click_pos("collExit")
	ahk.send("{Escape}")
	time.sleep(0.5)
	ahk.send("R")
	time.sleep(0.5)
	ahk.send("{Enter}")
	time.sleep(1.5)
	
	ahk.run_script('''
		WinActivate, Roblox
		WinWaitActive, Roblox

		WinGetPos, X, Y, W, H, Roblox
		CenterX := X + W // 2
		CenterY := Y + H // 2

		Click, up, right
		MouseMove, %CenterX%, %CenterY%, 0
		Click, down, right
		Sleep, 200
		MouseMove, %CenterX%, % (CenterY + 100), 0
		Click, up, right
	''')
	
	auto.leftClick()
	time.sleep(1)

def handle_questboard():
	align_camera()
	hold_key('s', 5)
	hold_key('w', 1)
	hold_key('s', 0.8)
	ahk.run_script('''
		WinActivate, Roblox
		WinWaitActive, Roblox
	''')
	hold_key('space', 0.1)
	hold_key('s', 2.3)
	hold_key('d', 0.9)
	time.sleep(0.2)
	ahk.key_press('e')
	time.sleep(0.5)
	qb.handle(config)

def align_character():
	log("Aligning character...")
	time.sleep(1)
	auto.leftClick()
	hold_key('s', 5)
	hold_key('a', 2)
	hold_key('s', 3)
	time.sleep(0.1)
	hold_key('w', 0.1)
	hold_key('d', 1.5)
	time.sleep(0.1)
	hold_key('a', 0.1)
	hold_key('w', 0.1)

def go_to_resonance():
	close_chat()
	align_camera()
	align_character()
	log("Going to Grail of Resonance")
	hold_key('s', 0.1)
	hold_key('space', 0.1)
	hold_key('s', 1.5)
	hold_key('a', 0.5)
	hold_key('s', 5.7)
	hold_key('a', 1.5)
	hold_key('s', 1)
	hold_key('a', 0.2)
	hold_key('s', 0.3)
	hold_key('a', 0.2)
	hold_key('s', 0.5)

class SettingsCoordinateOption(tk.CTkFrame):
	def on_pick_button(self):
		clickX, clickY = get_click_coordinates()
		config[self.internalNameX] = clickX
		config[self.internalNameY] = clickY
		save_settings()

	def __init__(self, master, optionName, internalNameX, internalNameY, **kwargs):
		super().__init__(master, **kwargs)
		self.configure(width=coordinate_config_width, height=40)

		self.internalNameX = internalNameX
		self.internalNameY = internalNameY

		self.label = tk.CTkLabel(self, text=optionName, fg_color="transparent", width=(coordinate_config_width-130))
		self.label.grid(row=0, column=0)

		self.pick_button = tk.CTkButton(self, text="Pick Coordinates", command=self.on_pick_button, width=130)
		self.pick_button.grid(row=0, column=1)

class SetCoordinatesWindow(tk.CTkToplevel):
	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)

		self.option_count = 0
		self.resizable(False, False)
		self.lift()
		self.focus_force()
		self.attributes("-topmost", True)

	def add_option(self, label, optionName):
		option = SettingsCoordinateOption(self, label, optionName+"X", optionName+"Y")
		option.grid(row=self.option_count, column=0, pady=3)
		self.option_count += 1

class SettingsCoordinateWindow(SetCoordinatesWindow):
	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)

		self.title("Edit Button Coordinates")
		self.geometry(str(coordinate_config_width)+"x450")

		self.add_option("Inventory Button", "invBtnPos")
		self.add_option("Inventory Items Tab", "invItemsTabPos")
		self.add_option("Inventory X Button", "genericClose")
		self.add_option("Inventory Item Use Button", "itemUseBtn")
		self.add_option("Inventory Search Bar", "invSearch")
		self.add_option("Inventory First Item Slot", "invFirstItemSlot")
		self.add_option("Aura Equip Button", "auraEquipBtn")
		self.add_option("Collection Button", "collBtn")
		self.add_option("Collection Exit Button", "collExit")

class QuestboardCoordinatesWindow(SetCoordinatesWindow):
	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)

		self.title("Questboard Button Coordinates")
		self.geometry(str(coordinate_config_width)+"x450")

		self.add_option("Next Quest Button", "qbRightBtn")
		self.add_option("Accept Button", "qbAcceptBtn")
		self.add_option("Dismiss Button", "qbDismissBtn")

class SettingsTab(tk.CTkFrame):
	def on_edit_coordinates_button(self):
		if hasattr(self, 'set_coords_win') and self.set_coords_win.winfo_exists():
			self.set_coords_win.lift()
			self.set_coords_win.focus_force()
			return
		self.set_coords_win = SettingsCoordinateWindow(self)

	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)
		
		self.edit_coordinates_button = tk.CTkButton(self, text="Edit Coordinates", command=self.on_edit_coordinates_button, width=150)
		self.edit_coordinates_button.place(x=5, y=5)

class QuestboardTab(tk.CTkFrame):
	def on_edit_coordinates_button(self):
		if hasattr(self, 'set_coords_win') and self.set_coords_win.winfo_exists():
			self.set_coords_win.lift()
			self.set_coords_win.focus_force()
			return
		self.set_coords_win = QuestboardCoordinatesWindow(self)

	def collect_luckies_toggled(self):
		config["qbTakeLuckyPotion"] = self.lucky_potion_checkbox.get() == 1

	def collect_speeds_toggled(self):
		config["qbTakeSpeedPotion"] = self.lucky_potion_checkbox.get() == 1

	def collect_coins_toggled(self):
		config["qbTakeCoins"] = self.coin_checkbox.get() == 1
		if not self.disable_first_notif:
			if(self.coin_checkbox.get() == 1):
				response = ctypes.windll.user32.MessageBoxW(
					0,
					"Having this option enabled will automatically do the\nGrail of Resonance. Disable it if you don't want that.",
					"Info",
					0
				)
		self.disable_first_notif = False

	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)
		self.disable_first_notif = False
		self.lucky_potion_checkbox = tk.CTkCheckBox(self, text="Collect Lucky Potions", command=self.collect_luckies_toggled)
		if config["qbTakeLuckyPotion"]:
			self.lucky_potion_checkbox.toggle();
		self.lucky_potion_checkbox.place(x=5, y=40)

		self.speed_potion_checkbox = tk.CTkCheckBox(self, text="Collect Speed Potions", command=self.collect_speeds_toggled)
		if config["qbTakeSpeedPotion"]:
			self.speed_potion_checkbox.toggle();
		self.speed_potion_checkbox.place(x=5, y=70)

		self.coin_checkbox = tk.CTkCheckBox(self, text="Collect Coins", command=self.collect_coins_toggled)
		if config["qbTakeCoins"]:
			self.disable_first_notif = True
			self.coin_checkbox.toggle();
		self.coin_checkbox.place(x=5, y=100)

		self.edit_coordinates_button = tk.CTkButton(self, text="Edit Coordinates", command=self.on_edit_coordinates_button, width=150)
		self.edit_coordinates_button.place(x=5, y=5)

class ItemUseTab(tk.CTkFrame):
	def use_br_toggled(self):
		config["useBR"] = self.use_br_checkbox.get() == 1

	def use_sc_toggled(self):
		config["useSC"] = self.use_sc_checkbox.get() == 1

	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)

		self.use_br_checkbox = tk.CTkCheckBox(self, text="Use Biome Randomizer", command=self.use_br_toggled)
		if config["useBR"]:
			self.use_br_checkbox.toggle();
		self.use_br_checkbox.place(x=5, y=5)

		self.use_sc_checkbox = tk.CTkCheckBox(self, text="Use Strange Controller", command=self.use_sc_toggled)
		if config["useSC"]:
			self.use_sc_checkbox.toggle();
		self.use_sc_checkbox.place(x=5, y=35)

class Tabber(tk.CTkTabview):
	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)

		self.configure(anchor="nw")
		
		#self.add("Biomes")
		#self.add("Webhook")
		#self.add("Merchant")
		self.add("Item Use")
		self.add("Settings")
		self.add("Questboard")
		#self.add("About")
		
		self.item_use_tab = ItemUseTab(master=self.tab("Item Use"))
		self.item_use_tab.pack(fill="both", expand=True)

		self.settings_tab = SettingsTab(master=self.tab("Settings"))
		self.settings_tab.pack(fill="both", expand=True)

		self.questboard_tab = QuestboardTab(master=self.tab("Questboard"))
		self.questboard_tab.pack(fill="both", expand=True)

class ControlButtons(tk.CTkFrame):
	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)
		
		self.configure(fg_color="transparent")
		
		self.start_button = tk.CTkButton(self, text="Start (F1)", command=self.start_button_event, width=100)
		self.start_button.grid(row=0, column=0, padx=5)
		
		self.stop_button = tk.CTkButton(self, text="Stop (F3)", command=self.stop_button_event, width=100)
		self.stop_button.grid(row=0, column=1)
	
	def start_button_event(self):
		global status
		if status == "Running":
			return
		log("[ControlButtons]: Start")
		self.event_generate("<<StartPressed>>")
		
	def stop_button_event(self):
		global status
		if status == "Stopped" or status == "Idle":
			return
		log("[ControlButtons]: Stop")
		self.event_generate("<<StopPressed>>")

class App(tk.CTk):
	def __init__(self):
		log("[App]: Initializing...")
		super().__init__()
		
		self.update_title()
		self.geometry("650x300")
		self.resizable(False, False)

		self.tabs = Tabber(master=self)
		self.tabs.pack(fill="x", pady=7)
		
		self.control_btns = ControlButtons(master=self)
		self.control_btns.pack(fill="y")
		
		self.bind("<<StartPressed>>", self.on_start)
		self.bind("<<StopPressed>>", self.on_stop)

		self.protocol("WM_DELETE_WINDOW", self.on_window_close)
		log("[App]: Started!")

	def update_title(self):
		self.title("BMC's Macro - "+status)
	
	def on_window_close(self):
		log("[App]: Closing...")
		save_settings()
		log("[App]: Settings saved")
		self.destroy()

	def on_start(self, event):
		global status
		if status == "Running":
			return
		log("[App]: Recieved start event")
		status = "Running"
		self.update_title()
		time.sleep(1)
		threading.Thread(target=self.run_macro, daemon=True).start()
	
	def run_macro(self):
		equip_aura("abyssal hunter")
		equip_aura(config["autoEquipAura"])
		while True:
			#close_chat()
			#if config["useSC"]:
			#	use_item("strange controller")
			#if config["useBR"]:
			#	use_item("biome randomizer")
			#equip_aura(config["autoEquipAura"])
			#handle_questboard()
			go_to_resonance()

	def on_stop(self, event):
		global status
		if status == "Stopped" or status == "Idle":
			return
		log("[App]: Recieved stop event")
		status = "Stopped"
		self.update_title()
		os.execv(sys.executable, ['python'] + sys.argv)

keyboard.Listener(on_press=on_key_press).start()

app = App()
app.mainloop()