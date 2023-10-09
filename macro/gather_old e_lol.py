import pyautogui as pag
import os
import tkinter
import move
import loadsettings
import time
sizeword = setdat["gather_size"]
width = round(setdat["gather_width"]*1.5)
size = 0
if sizeword.lower() == "s":
    size = 0.5
elif sizeword.lower() == "m":
    size =1
else:
    size = 1.5
cmd = """
osascript -e 'activate application "Roblox"' 
"""
os.system(cmd)

 

move.hold("w",0.5*size)
for _ in range(width):
    move.hold("a",0.125*(width/4))
    move.hold("a",0.125*(width/4))
for _ in range(width):
    move.hold("s",0.5*size)
    move.hold("d",0.125*(width/4))
    move.hold("w",0.5*size)
    move.hold("d",0.125*(width/4))
move.hold("s",0.5*size)
for _ in range(width):
    move.hold("a",0.125*(width/4))
    move.hold("a",0.125*(width/4))
for _ in range(width):
    move.hold("w",0.5*size)
    move.hold("d",0.125*(width/4))
    move.hold("s",0.5*size)
    move.hold("d",0.125*(width/4))
