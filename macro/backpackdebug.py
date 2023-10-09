import pyautogui as pag
import os
import loadsettings
import time
from pixelcolour import getPixelColor
import numpy as np
savedata = {}
ms = pag.size()
mw = ms[0]
mh = ms[1]
dt = loadsettings.load()['display_type']
ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
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

os.system(cmd)
time.sleep(1)
def rgb_to_hex(r, g, b):
      return ('0x{:X}{:X}{:X}').format(r, g, b)
    
def bpc():
    dt = loadsettings.load()['display_type']
    ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
    xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
    X1=mw//2+63
    Y1=7
    if dt == "built-in retina display":
        X1*=2 #(round((mw/2+60), 0))*2
        Y1*=2 #14*2
    im = np.array(pag.screenshot(region = (X1,Y1,1,1) ))
    col = tuple(im[0,0])
    print(col)
    backpackColor = int(rgb_to_hex(col[0],col[1],col[2]),16)
    #gm = 0.00001284664 #100/(14889259-7105124)
    #gc = -91.276 #100- gm*14889259
    #perc = int(gm*backpackColor+gc)

    if backpackColor >= 14889259: #13775147
        perc = 100
    elif backpackColor >= 11231045:
        perc = 85
    elif backpackColor >= 8502900:
        perc = 50
    elif backpackColor >= 8381831:
        perc = 30
    else:
        perc = 0
    #print("Pixel Colour: {}, Backpack Percentage: {}.".format(backpackColor, perc))
    print("Pixel Colour: {}, Backpack Percentage: {}.".format(backpackColor, perc))
    return perc
bpc()
    
#pag.moveTo(X1,Y1)

