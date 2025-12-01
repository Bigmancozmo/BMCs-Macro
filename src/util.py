import os, hashlib, sys

def hash_folder(folder_path):
	all_data = bytearray()
	for root, dirs, files in os.walk(folder_path):
		dirs.sort()
		files.sort()
		for f in files:
			file_path = os.path.join(root, f)
			with open(file_path, "rb") as file:
				content = file.read()
				content = content.replace(b"\r\n", b"\n")
				all_data += content
	return hashlib.sha256(all_data).hexdigest()

def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, relative_path)
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)