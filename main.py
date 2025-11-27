from logging import warning
import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QTabWidget, QMainWindow, QLabel, QWidget, QPushButton
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout

VERSION = "v1.0.0"
WIDTH = 660
HEIGHT = 320

class Tab(QWidget):
	def __init__(self):
		super().__init__()

class InfoTab(Tab):
	def __init__(self):
		super().__init__()
		layout = QVBoxLayout()

		contents = "Failed to load info.txt"

		try:
			with open("./info.txt") as f:
				contents = f.read()
		except:
			warning("Failed to read './info.txt'")

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

app.exec()
