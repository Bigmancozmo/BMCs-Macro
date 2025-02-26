from tkinter import *
from PIL import Image, ImageTk

from style.styler import style as s

class Root(Frame):
	def __init__(self, master, width, height, **kwargs):
		super().__init__(master, width=width, height=height, **kwargs)
		self.pack_propagate(False)
		self.config(bg=s['bg'])

		self.cornerImgSrc_0 = Image.open("style/img/corner.png").rotate(0, expand=True)
		self.cornerImg_0 = ImageTk.PhotoImage(self.cornerImgSrc_0)

		self.cornerImgSrc_90 = Image.open("style/img/corner.png").rotate(90, expand=True)
		self.cornerImg_90 = ImageTk.PhotoImage(self.cornerImgSrc_90)

		self.cornerImgSrc_180 = Image.open("style/img/corner.png").rotate(180, expand=True)
		self.cornerImg_180 = ImageTk.PhotoImage(self.cornerImgSrc_180)

		self.cornerImgSrc_270 = Image.open("style/img/corner.png").rotate(270, expand=True)
		self.cornerImg_270 = ImageTk.PhotoImage(self.cornerImgSrc_270)

		self.corner_tl = Label(self, image=self.cornerImg_0, bg=s['bg']).place(x=0, y=0, anchor="nw")
		self.corner_tr = Label(self, image=self.cornerImg_270, bg=s['bg']).place(x=width, y=0, anchor="ne")
		self.corner_bl = Label(self, image=self.cornerImg_90, bg=s['bg']).place(x=0, y=height, anchor="sw")
		self.corner_br = Label(self, image=self.cornerImg_180, bg=s['bg']).place(x=width, y=height, anchor="se")
