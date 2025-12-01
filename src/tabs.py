from logging import warning
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtWidgets import QVBoxLayout

from util import resource_path

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
			print("Read path:", resource_path("data/info.txt"))

		label = QLabel(contents)
		label.setAlignment(Qt.AlignmentFlag.AlignTop)

		layout.addWidget(label)
		self.setLayout(layout)