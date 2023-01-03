import pyautogui as pag
import time
import os
import tkinter
import move
cmd = """
osascript -e 'activate application "Roblox"' 
"""
time.sleep(1)
os.system(cmd)
savedata = {}
def loadSave():
    with open('save.txt') as f:
        lines = f.read().split("\n")
    f.close()
    for s in lines:
        l = s.replace(" ","").split(":")
        if l[1].isdigit():
            l[1] = int(l[1])
        savedata[l[0]] = l[1]
loadSave()


print(pag.size())
