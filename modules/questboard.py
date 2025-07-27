import pytesseract
from PIL import Image
import pygetwindow as gw
import pyautogui as auto
import tkinter as tk
import time, ahk

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def handle(config):
    def move_mouse(target_x, target_y):
        ahk.mouse_move(target_x, target_y)

    def move_to_defined(posName):
        xValue = config[posName+"X"]
        yValue = config[posName+"Y"]
        move_mouse(xValue, yValue)
        time.sleep(0.1)

    def click_pos(posName):
        move_to_defined(posName)
        auto.leftClick()
        time.sleep(0.3)

    win = gw.getWindowsWithTitle("Roblox")[0]
    win.activate()
    time.sleep(0.5)

    w, h = win.width, win.height - 500
    x, y = win.left + (3 * win.width // 4), win.top + 350
    region = (x, y, (w // 4)-20, h)

    for i in range(5):
        click_pos("qbRightBtn")

        screenshot = auto.screenshot(region=region)
        text = pytesseract.image_to_string(screenshot)

        root = tk.Tk()
        root.overrideredirect(True)
        root.geometry(f"{region[2]}x{region[3]}+{x}+{y}")
        root.wm_attributes("-topmost", True)
        root.wm_attributes("-transparentcolor", "white")

        canvas = tk.Canvas(root, width=region[2], height=region[3], bg="white", highlightthickness=0)
        canvas.pack()
        canvas.create_rectangle(0, 0, region[2], region[3], outline="red", width=3)

        root.after(100, root.destroy)
        root.mainloop()

        itemsToGet = {
            "Lucky P": config["qbTakeLuckyPotion"],
            "Speed P": config["qbTakeSpeedPotion"]
        }

        found = any(item in text and enabled for item, enabled in itemsToGet.items())
        if found:
            print("Has wanted reward")
            click_pos("qbAcceptBtn")
        else:
            print("No wanted rewards")
            click_pos("qbDismissBtn")
    
    exitBtnX = win.width / 2
    exitBtnY = win.height * 0.867
    move_mouse(exitBtnX, exitBtnY)
    auto.leftClick()