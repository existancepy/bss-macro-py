import pyautogui as pag
import os
import tkinter
import move
import loadsettings
import time
import Quartz
setdat = loadsettings.load()
sizeword = setdat["gather_size"]
width = round(setdat["gather_width"]*1.5)
size = 0
if sizeword.lower() == "s":
    size = 0.25
elif sizeword.lower() == "m":
    size =0.5
else:
    size = 1


move.hold("w",0.5*size)
move.hold("a",0.125*(width/4)*width*2+0.3*(width-1))
for _ in range(width):
    move.hold("s",0.5*size)
    move.hold("d",0.125*(width/4))
    move.hold("w",0.5*size)
    move.hold("d",0.125*(width/4))
move.hold("s",0.5*size)
move.hold("a",0.125*(width/4)*width*2+0.3*(width-1))
for _ in range(width):
    move.hold("w",0.5*size)
    move.hold("d",0.125*(width/4))
    move.hold("s",0.5*size)
    move.hold("d",0.125*(width/4))




        
