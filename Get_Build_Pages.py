import pyautogui
from pathlib import Path
import time

# Need to setup default save location

path = r'C:\Users\Tanner\Google Drive\Documents\Programming\Python\Python_Scripts\Pokemon_Unite\mhtlm_files'

new_mon = True

if new_mon == True:

    files = [f.unlink() for f in Path(path).glob("*") if f.is_file()]

    height = 460
    rows = 6
    columns = 10
    for i in range(rows):
        width = 720
        for j in range(columns):
            if i == 5 and j == 4:
                break
            pyautogui.click(width, height)
            time.sleep(.5)
            pyautogui.moveTo(100, 400)
            time.sleep(1)
            pyautogui.hotkey("ctrlleft", "s")
            time.sleep(3)
            pyautogui.press("enter")
            time.sleep(1)
            pyautogui.hotkey("altleft", "left")
            time.sleep(1)
            width += 122
        height += 146