from tkinter import *
from style.styler import style as s
import tkinter.font as tkFont

class Header(Frame):
	def __init__(self, master=None, **kwargs):
		super().__init__(master, **kwargs)
		self.config(bg=s['bg'])
		self.font_extrabold_16 = tkFont.Font(family="Sarpanch ExtraBold", size=16)
		Label(self, text="BMC's Macro", font=self.font_extrabold_16, fg=s['text'], bg=s['bg']).pack()
		Frame(self, bg=s['outline'], width=210, height=s['paddingSize']).pack()
