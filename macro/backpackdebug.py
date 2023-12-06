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
def loadRes():
    outdict =  {}
    with open('save.txt') as f:
        lines = f.read().split("\n")
    f.close()
    for s in lines:
        l = s.replace(" ","").split(":")
        if l[1].isdigit():
            l[1] = int(l[1])
        outdict[l[0]] = l[1]
    return outdict

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
def rgb_to_dec(r, g, b):
      return (r*256*256)+(g*256)+b
    
def bpc():
    savedat = loadRes()
    ww = savedat['ww']
    wh = savedat['wh']
    X1=mw//2+70
    Y1=7
    print(ww, X1)
    im = np.array(pag.screenshot(region = (X1,Y1,1,1) ))
    testimg = pag.screenshot(region = (X1,Y1,100,100))
    testimg.save("backpack.png")
    col = tuple(im[0,0])
    print(col)
    backpackColor = rgb_to_dec(col[0],col[1],col[2])
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

