from pynput.keyboard import Key, Controller
from delay import sleep
import os
import tkinter
import move
import loadsettings
import time
import Quartz

sizeword = setdat["gather_size"]
width = setdat["gather_width"]
size = 0
if sizeword.lower() == "s":
    size = 1
elif sizeword.lower() == "m":
    size = 1.5
else:
    size = 2
wm = 0.2*size
sm = 0.65*size
move.hold("a",width*wm*2)
move.hold("s",sm)
for _ in range(width):
    move.hold("d",wm)
    move.hold("w",sm)
    move.hold("d",wm)
    move.hold("s",sm)
    
move.hold("a",width*wm*2)
move.hold("w",sm)
for _ in range(width):
    move.hold("d",wm)
    move.hold("s",sm)
    move.hold("d",wm)
    move.hold("w",sm)


        
