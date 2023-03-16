import pyautogui as pag
import os
import tkinter
import move
import loadsettings
setdat = loadsettings.load()
sizeword = setdat["gather_size"]
width = setdat["gather_width"]/2
size = 0
if sizeword.lower() == "s":
    size = 0.5
elif sizeword.lower() == "m":
    size =1
else:
    size = 1.5

for i in range(3):
    move.hold("w",0.4*(size+i/1.5))
    move.hold("d",0.4*(size+i/1.5))
    move.hold("s",0.4*(size+i/1.5))
    move.hold("a",0.4*(size+i/1.5))
    
 

    
    
