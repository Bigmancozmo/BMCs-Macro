import configparser
import util
import os

FILE_PATH = util.resource_path("config.ini")

def createFile():
	if not os.path.exists(FILE_PATH):
		print("Creating config file")
		with open(FILE_PATH, 'w') as file:
			file.write("")
		return
	print("Found config.ini")

createFile()

config = configparser.ConfigParser()
config.read(FILE_PATH)

def saveConfig():
	with open(FILE_PATH, "w") as f:
		config.write(f)

def getKey(key, default=""):
	section = "Settings"
	if not config.has_section(section):
		config.add_section(section)
	if not config.has_option(section, key):
		config[section][key] = default
		saveConfig()
	return config[section][key]

def setKey(key, value):
	getKey(key, value) # Make sure it and the section exist
	config["Settings"][key] = value # Now we can simply just write to it
	print(f"Set key '{key}' to '{value}'")
	saveConfig()