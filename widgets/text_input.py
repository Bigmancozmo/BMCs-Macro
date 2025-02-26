from tkinter import *
from style.styler import style as s
import tkinter.font as tkFont

class TextInput(Frame):
	def __on_submit_click(self):
		self.submit_func(self.entry.get())

	def __init__(self, master, width, height, optionName, clicked, entryPad=2, setText="", **kwargs):
		super().__init__(master, width=width, height=height, **kwargs)
		#self.pack_propagate(False)
		self.config(bg=s['bg'])
		self.font_bold_8 = tkFont.Font(family="Sarpanch ExtraBold", size=height)
		self.submit_func = clicked

		nameWidth = self.font_bold_8.measure(optionName)
		submitWidth = self.font_bold_8.measure("Submit")

		self.columnconfigure(0, weight=2)
		self.columnconfigure(1, weight=5)
		self.columnconfigure(2, weight=1)

		self.text = Label(self, text=optionName, font=self.font_bold_8, bg=s['bg'], fg=s['text'])
		self.text.grid(row=0, column=0, padx=5)

		self.entry = Entry(self, font=self.font_bold_8, bg=s['inputBg'], fg=s['text'], width=int((width-nameWidth-submitWidth)/height)-entryPad)
		self.entry.insert(0, setText)
		self.entry.grid(row=0, column=1, padx=5)

		self.text = Button(self, text="Submit", font=self.font_bold_8, bg=s['bg'], fg=s['text'], command=self.__on_submit_click)
		self.text.grid(row=0, column=2, padx=5)
