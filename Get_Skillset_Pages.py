import pyautogui
from pathlib import Path
import time


# Need to setup default save location

path = r'C:\Users\Tanner\Google Drive\Documents\Programming\Python\Python_Scripts\Pokemon_Unite\Pokemon_Sites'
new_week = True

if new_week:

    files = [f.unlink() for f in Path(path).glob("*") if f.is_file()]

height = 950
rows = 5
columns = 13
for i in range(rows):

    width = 890
    for j in range(columns):
        if i == 4 and j == 7:

            break
        else:
            pyautogui.click(width, height)
            time.sleep(4)
            pyautogui.hotkey("ctrlleft", "s")
            time.sleep(2)
            pyautogui.press("enter")
            time.sleep(2)
            pyautogui.hotkey("altleft", "left")
            time.sleep(2)
            width += 162

    height += 185
