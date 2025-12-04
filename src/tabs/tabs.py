from logging import warning
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QScrollArea
from PyQt6.QtGui import QPainter, QPolygon
import json

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

class TriangleWidget(QWidget):
	def paintEvent(self, event):
		painter = QPainter(self)
		points = QPolygon([
			QPoint(50, 0),
			QPoint(0, 100),
			QPoint(100, 100)
		])
		painter.setBrush(Qt.GlobalColor.red)
		painter.drawPolygon(points)

class AuraInfo(QWidget):
	def __init__(self, aura, biome, chance, nativeChance):
		super().__init__()
		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignmentFlag.AlignTop)
		layout.setSpacing(0)
		layout.setContentsMargins(0, 0, 0, 0)

		btn = QPushButton(aura)
		btn.setCursor(Qt.CursorShape.PointingHandCursor)
		btn.clicked.connect(self.btn_clicked)
		layout.addWidget(btn)

		self.frame = QFrame()
		self.frame.setFrameShape(QFrame.Shape.StyledPanel)
		self.frame.setFrameShadow(QFrame.Shadow.Raised)
		self.frame.setFixedHeight(30)
		self.frame.setVisible(False)
		layout.addWidget(self.frame)

		infoLayout = QHBoxLayout()
		infoLayout.setContentsMargins(4, 0, 4, 0)

		chanceText = QLabel("Chance - " + str(chance))
		biomeText = QLabel("Biome - " + str(biome))
		nativeRarityText = QLabel("Native - " + str(nativeChance))

		infoLayout.addWidget(chanceText)
		infoLayout.addWidget(biomeText)
		infoLayout.addWidget(nativeRarityText)

		self.frame.setLayout(infoLayout)

		self.setLayout(layout)
	
	def btn_clicked(self):
		self.frame.setVisible(not self.frame.isVisible())

class AurasTab(Tab):
	def __init__(self):
		super().__init__()

		aura_data = {}
		succeeded = True
		try:
			with open(resource_path("data/auras.json"), "r") as f:
				aura_data = json.load(f)
		except:
			warning("Failed to read data/auras.json")
			succeeded = False

		container = QWidget()
		container_layout = QVBoxLayout()
		container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
		container_layout.setSpacing(4)
		container_layout.setContentsMargins(0, 0, 0, 0)

		if succeeded:
			try:
				container_layout.addWidget(QLabel("Click on auras to view info about them"))

				for aura, data in aura_data.items():
					biome = "N/A"
					chance = "N/A"
					native = "N/A"
					if "biome" in data:
						biome = data["biome"]
					if "chance" in data:
						if data["chance"] > 0:
							chance = "1 in "+str(data["chance"])
					if "native" in data:
						native = "1 in "+str(data["native"])
					container_layout.addWidget(AuraInfo(aura, biome, chance, native))
			except Exception as e:
				warning(e)
				container_layout.addWidget(QLabel("Failed to load aura info, aura-related features may not work properly"))
		else:
			container_layout.addWidget(QLabel("Failed to read data/auras.json, aura-related features may not work"))

		container.setLayout(container_layout)

		scroll = QScrollArea()
		scroll.setFrameShape(QFrame.Shape.NoFrame)
		scroll.setWidgetResizable(True)
		scroll.setWidget(container)

		main_layout = QVBoxLayout()
		main_layout.addWidget(scroll)
		self.setLayout(main_layout)