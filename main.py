from logging import warning
import sys, os, time, hashlib

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QTabWidget, QMainWindow, QLabel, QWidget, QPushButton, QDialog, QProgressBar
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout

VERSION = "v1.0.0"
WIDTH = 660
HEIGHT = 320

print("Running at:", __file__)

def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class Tab(QWidget):
	def __init__(self):
		super().__init__()

class InfoTab(Tab):
	def __init__(self):
		super().__init__()
		layout = QVBoxLayout()

		contents = "Failed to load data/info.txt"

		try:
			with open(resource_path("data/info.txt")) as f:
				contents = f.read()
		except:
			warning("Failed to read 'data/info.txt'")

		label = QLabel(contents)
		label.setAlignment(Qt.AlignmentFlag.AlignTop)

		layout.addWidget(label)
		self.setLayout(layout)

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
dialog.setWindowTitle("Asset Updater")
dialog.setFixedSize(QSize(250, 100))
dialog.setContentsMargins(20,20,20,20)

label = QLabel("Updating data...")
layout.addWidget(label)

pbar = QProgressBar()
pbar.setRange(0, 100)
pbar.setValue(0)
layout.addWidget(pbar)

dialog.setLayout(layout)
dialog.exec()

time.sleep(0.5)

app.exec()