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
wm = 0.5*size
sm = 0.25*size
df = (((wm*2)**2)+((sm*4)**2))**0.5
move.hold("a",wm)
move.hold("w",sm)
move.hold("d",wm*2)
move.hold("w",sm)
move.hold("a",wm*2)
keyboard.press('d')
keyboard.press('s')
sleep(df)
keyboard.release('s')
keyboard.release('d')
move.hold("a",wm*2)
move.hold("w",sm)
move.hold("d",wm*2)
move.hold("w",sm*8)
move.hold("d",0.6*width)
move.hold("a",0.4*width)
move.hold("s",sm*4)
move.hold("a",wm*2)
move.hold("s",sm)
move.hold("d",wm*2)
move.hold("s",sm)
move.hold("a",wm*2)
move.hold("s",sm)
move.hold("d",wm*2)
move.hold("s",sm)
move.hold("a",wm*2)
keyboard.press('w')
keyboard.press('d')
sleep(df/2)
keyboard.release('d')
keyboard.release('w')




        
