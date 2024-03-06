import pyautogui as pag
import os
import loadsettings
import numpy as np
from logpy import log
import subprocess
ms = pag.size()
mw = ms[0]
mh = ms[1]
data = {6975603: 2, 8518291: 6, 8518034: 9, 8517778: 11, 8517521: 13, 8517264: 14, 8517008: 15, 8517007: 16, 8516751: 17, 8450959: 22, 8450702: 19, 8450190: 20, 8450189: 26, 8450446: 23, 8449933: 27, 8384140: 29, 8383884: 30, 8383115: 31, 8315013: 33, 8380036: 34, 8313987: 36, 8379267: 37, 8313218: 38, 8378497: 39, 8377214: 41, 8376701: 42, 8375932: 43, 8440186: 44, 8439673: 47, 8439159: 48, 8503925: 49, 8503413: 50, 8567923: 52, 8632433: 53, 8696687: 55, 8825706: 59, 8890473: 60, 9020006: 61, 9085029: 63, 9084516: 64, 9214818: 65, 9214305: 66, 9409630: 67, 9474397: 68, 9538908: 69, 9799256: 71, 9863767: 73, 10059348: 75, 10254418: 76, 10319441: 77, 10449486: 78, 10580046: 79, 10710092: 80, 10774858: 81, 11035976: 82, 11231045: 84, 11296068: 85, 11491394: 86, 11752511: 87, 11817535: 88, 12143932: 90, 12404537: 91, 12469561: 92, 12795958: 93, 12861237: 94, 13187891: 96, 13449266: 97, 13776175: 99, 13886187: 100}
data = sorted(data.items())     
#0% 7697781
#31% 8381831
#52% 8502900
#84% 11231045
#100% 14889259

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

def rgb_to_dec(r, g, b):
      return (r * 256 * 256) + (g * 256) + b
def bpc():
    Y1=8
    add = 65
    setdat = loadsettings.load()
    
    if setdat["new_ui"]: Y1 = 31  
    if setdat['display_type'] == "built-in retina display":
        add*= 2
        Y1 *= 2
    savedat = loadRes()
    ww = savedat['ww']
    X1=ww//2+add
    im = np.array(pag.screenshot(region = (X1,Y1,1,1) ))
    col = tuple(im[0,0])
    #print(col)
    backpackColor = rgb_to_dec(col[0],col[1],col[2])
    #gm = 0.00001284664 #100/(14889259-7105124)
    #gc = -91.276 #100- gm*14889259
    #perc = int(gm*backpackColor+gc)
    perc = 0
    for k,v in data:
        if backpackColor >= k:
            perc = v
        
    #print("Pixel Colour: {}, Backpack Percentage: {}.".format(backpackColor, perc))
    print("Pixel Colour: {}, Backpack Percentage: {}.".format(col, perc))
    return perc
