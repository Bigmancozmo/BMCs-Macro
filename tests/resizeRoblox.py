# Test stuff... for me

import win32gui

def get_window_handle(window_name):
    try:
        hwnd = win32gui.FindWindow(None, window_name)
        return hwnd
    except win32gui.error:
        return None

window_name = "Roblox"
win = get_window_handle(window_name)

win32gui.MoveWindow(win, 0, 0, 600, 600, True)