import pyautogui as pag
import os
import tkinter
import move
import loadsettings

sizeword = setdat["gather_size"]
width = setdat["gather_width"]
size = 0
if sizeword.lower() == "s":
    size = 0.5
elif sizeword.lower() == "m":
    size =1
else:
    size = 1.5
move.hold("a",(0.25*size))
move.hold("w",(0.25*size))
for i in range(width):
    if i != 0:
        move.hold("a",(0.2*i)/2)
        move.hold("w",(0.2*i)/2)
    move.hold("d",0.5*size+0.2*i)
    move.hold("s",0.5*size+0.2*i)
    move.hold("a",0.5*size+0.2*i)
    move.hold("w",0.5*size+0.2*i)

for i in range(width,0,-1):
    print(i)
    if i != width:
        move.hold("s",(0.2*i)/2)
        move.hold("d",(0.25*i)/2)
    move.hold("d",0.5*size+0.2*i)
    move.hold("s",0.5*size+0.2*i)
    move.hold("a",0.5*size+0.2*i)
    move.hold("w",0.5*size+0.2*i)

    
move.hold("s",0.25*size)
move.hold("d",0.25*size)

    
 

    
    
