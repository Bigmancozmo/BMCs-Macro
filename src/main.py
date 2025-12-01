from logging import warning
import threading
import sys, os, hashlib, shutil, requests, time
from zipfile import ZipFile
from io import BytesIO

from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtWidgets import QApplication, QTabWidget, QMainWindow, QLabel, QWidget, QPushButton, QDialog, QProgressBar
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout

from tabs import InfoTab
from util import resource_path, hash_folder

VERSION = "v1.0.0"
WIDTH = 660
HEIGHT = 320

print("Running at:", __file__)

class Footer(QWidget):
	def __init__(self):
		super().__init__()
		
		height = 35

		self.setFixedHeight(height)

		layout = QHBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

		startButton = QPushButton("Start (F1)")
		stopButton = QPushButton("Stop (F3)")

		startButton.setFixedSize(QSize(100, height))
		stopButton.setFixedSize(QSize(100, height))

		layout.addWidget(startButton)
		layout.addWidget(stopButton)

		self.setLayout(layout)

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("BMC's Macro - " + VERSION)
		self.setFixedSize(QSize(WIDTH, HEIGHT))
		self.setContentsMargins(4, 4, 4, 4)

		central = QWidget()
		layout = QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)

		tabber = QTabWidget()
		tabber.addTab(InfoTab(), "Info")
		#tabber.addTab(Tab("Biomes"), "Biomes")
		#tabber.addTab(Tab("Questboard"), "Questboard")
		#tabber.addTab(Tab("Scheduler"), "Scheduler")

		footer = Footer()

		layout.addWidget(tabber)
		layout.addWidget(footer)
		central.setLayout(layout)

		self.setCentralWidget(central)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

print("yo gurt")

layout = QVBoxLayout()

dialog = QDialog()
dialog.setWindowTitle("Auto Updater")
dialog.setFixedSize(QSize(250, 100))
dialog.setContentsMargins(20,20,20,20)

label = QLabel("Checking for updates...")
layout.addWidget(label)

pbar = QProgressBar()
pbar.setRange(0, 100)
pbar.setValue(0)
layout.addWidget(pbar)

dialog.setLayout(layout)

def update_github_folder(user, repo, folder_path_in_repo, local_path, branch="main"):
	zip_url = f"https://github.com/{user}/{repo}/archive/refs/heads/{branch}.zip"
	with requests.get(zip_url, stream=True) as r:
		if r.status_code != 200:
			raise Exception(f"Failed to download zip: {r.status_code}")
		total = int(r.headers.get('content-length', 0))
		data = BytesIO()
		downloaded = 0
		for chunk in r.iter_content(chunk_size=8192):
			if chunk:
				data.write(chunk)
				downloaded += len(chunk)
				percent = min(downloaded / max(1, total) * 100, 100)
				print(f"\rDownloading: {percent:.2f}%", end="")
				pbar.setValue(int(percent))
		print("\nDownload complete!")

	data.seek(0)
	try:
		with ZipFile(data) as zip_file:
			temp_dir = "temp_extract"
			zip_file.extractall(temp_dir)
			src_folder = os.path.join(temp_dir, f"{repo}-{branch}", folder_path_in_repo)
			if os.path.exists(local_path):
				shutil.rmtree(local_path)
			shutil.copytree(src_folder, local_path)
			shutil.rmtree(temp_dir)
	except Exception as e:
		print("Error extracting zip:", e)
		with open("debug.zip", "wb") as f:
			f.write(data.getvalue())
		print("Saved downloaded file as debug.zip for inspection.")

def update():
	old_hash = hash_folder(resource_path("data"))
	if "_internal" in __file__:
		update_github_folder(
			"Bigmancozmo",
			"BMCs-Macro",
			"src/data",
			resource_path("update/data")
		)
	else:
		warning("Skipping auto update - not running compiled build.")
		QTimer.singleShot(0, dialog.close)
		return
	
	QTimer.singleShot(0, dialog.close)
	new_hash = hash_folder(resource_path("update/data"))

	time.sleep(1)

	if old_hash != new_hash:
		time.sleep(0.1)
		os.system(f"cd {resource_path("")} && rmdir /s /q data && xcopy update\data data /E /I")
		print("RESTARTING")
		time.sleep(0.1)
		os.execv(sys.executable, [sys.executable] + sys.argv)

threading.Thread(target=update, daemon=True).start()
dialog.exec()

app.exec()
