import pyautogui as pag
import os
import tkinter
import move
import loadsettings
setdat = loadsettings.load()
sizeword = setdat["gather_size"]
width = setdat["gather_width"]
size = 0
if sizeword.lower() == "s":
    size = 1
elif sizeword.lower() == "m":
    size =1.5
else:
    size = 2
def gather():
    move.hold("w",0.5*size)
    move.hold("d",0.3*width)
    move.hold("s",0.5*size)
    le = (0.3*width)/10
    for _ in range(3):
        move.hold("a",le)
        move.hold("w",0.5*size)
        move.hold("a",le)
        move.hold("s",0.5*size)
    move.hold("d",0.3*width)
    move.hold("w",0.5*size)
    for _ in range(2):
        move.hold("a",le)
        move.hold("s",0.5*size)
        move.hold("a",le)
        move.hold("w",0.5*size)
    move.hold("a",le)
    move.hold("s",0.5*size)
 
        
    
    
