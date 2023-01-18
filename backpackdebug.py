import pyautogui as pag
import os
import tkinter
import move
import loadsettings
import time
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
cmd = """
        osascript -e  'activate application "Roblox"'
    """

    
def rgb_to_hex(r, g, b):
      return ('0x{:X}{:X}{:X}').format(r, g, b)
    
X1=mw//2+59+3
Y1=14
if dt == "built-in retina display":
    X1=(round((mw/2+60), 0))*2
    Y1=14*2
    
pix = pag.pixel(X1,Y1)
backpackColor = int(rgb_to_hex(pix[0],pix[1],pix[2]),16)

gm = 0.00001284664 #100/(14889259-7105124)
gc = -91.276 #100- gm*14889259
perc = int(gm*backpackColor+gc)

if perc > 100:
    perc = 100
elif perc <0:
    perc = 0
return perc
