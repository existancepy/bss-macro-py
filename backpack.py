import pyautogui as pag
import time
import os
import tkinter
import move
import loadsettings
ms = pag.size()
mw = ms[0]
mh = ms[1]
#0% 7697781
#31% 8381831
#52% 8502900
#84% 11231045
#100% 14889259
def bpc():
    dt = loadsettings.load()['display_type']
    def rgb_to_hex(r, g, b):
      return ('0x{:X}{:X}{:X}').format(r, g, b)
    X1=mw//2+63
    Y1=8
    if dt == "built-in retina display":
        X1= (mw//2+63)*2 #(round((mw/2+60), 0))*2
        Y1= 8*2 #14*2
        
    pix = pag.pixel(X1,Y1)
    backpackColor = int(rgb_to_hex(pix[0],pix[1],pix[2]),16)
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
    print("pixel colour: {}, backpack percentage: {}".format(backpackColor, perc))
    return perc



