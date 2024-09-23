import pyautogui
from pathlib import Path
import time
import os
from pynput import *

# def get_coords(x, y):
#     print(x, y)
#
# with mouse.Listener(on_move = get_coords) as listen:
#     listen.join()


# Need to setup default save location

path = r'C:\Users\Tanner\Documents\git\Pokemon_Unite\Pokemon_Sites'
new_week = True

if new_week:

    files = [f.unlink() for f in Path(path).glob("*") if f.is_file() or f.is_dir()]

height = 625
rows = 6
columns = 13
for i in range(rows):

    width = -1865
    for j in range(columns):
        if i == 5 and j == 2:

            break
        else:
            pyautogui.moveTo(width, height)
            time.sleep(.5)
            pyautogui.scroll(-240)
            time.sleep(.5)
            pyautogui.click(width, height)
            time.sleep(4)
            pyautogui.hotkey("ctrlleft", "s")
            time.sleep(2)
            pyautogui.press("enter")
            time.sleep(2)
            pyautogui.hotkey("altleft", "left")
            time.sleep(2)
            width += 106

    height += 132
