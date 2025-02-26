import json, ctypes

with open("style/style.json", "r") as file:
    style = json.load(file)

ctypes.windll.gdi32.AddFontResourceW("style/font/Sarpanch-Black.ttf")
ctypes.windll.gdi32.AddFontResourceW("style/font/Sarpanch-Bold.ttf")
ctypes.windll.gdi32.AddFontResourceW("style/font/Sarpanch-ExtraBold.ttf")
ctypes.windll.gdi32.AddFontResourceW("style/font/Sarpanch-Medium.ttf")
ctypes.windll.gdi32.AddFontResourceW("style/font/Sarpanch-Regular.ttf")
ctypes.windll.gdi32.AddFontResourceW("style/font/Sarpanch-SemiBold.ttf")
print("Registered fonts")