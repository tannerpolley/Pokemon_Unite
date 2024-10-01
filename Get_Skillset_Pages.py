import pyautogui
from pathlib import Path
import time
import os
import numpy as np
import json
from pynput import *

# def get_coords(x, y):
#     print(x, y)
#
# with mouse.Listener(on_move = get_coords) as listen:
#     listen.join()


# Need to setup default save location

path = r'C:\Users\Tanner\Documents\git\Pokemon_Unite\Pokemon_Sites'
new_week = False
get_pages = False

if new_week:

    files = [f.unlink() for f in Path(path).glob("*") if f.is_file() or f.is_dir()]


else:
    files = os.listdir(path)

height = 625
rows = 6
columns = 13
if get_pages:
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

pokemon_list = []
files = os.listdir(path)
for file in files:
    pokemon_list.append(file[35:-5])

with open("roles.json") as f_in:
    role_dict = json.load(f_in)
pokemon_list_key = role_dict.keys()
for pokemon in pokemon_list_key:
    if pokemon not in pokemon_list:
        print(pokemon)

