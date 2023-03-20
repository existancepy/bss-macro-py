import pyautogui as pag
import os
import tkinter
import move
import loadsettings
setdat = loadsettings.load()
sizeword = setdat["gather_size"][gfid]
width = setdat["gather_width"][gfid]/2
size = 0
if sizeword.lower() == "s":
    size = 1
elif sizeword.lower() == "l":
    size =2
else:
    size = 1.5

    
 

    
    
