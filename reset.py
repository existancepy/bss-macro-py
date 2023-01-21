import pyautogui as pag
import time
import os
import tkinter
import imagesearch
from webhook import webhook

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

def reset():
    for _ in range(2):
        webhook("","Resetting character","dark brown")
        pag.moveTo(350,100)
        ww = savedata["ww"]
        wh = savedata["wh"]
        xo = ww//4
        yo = wh//100*90
        xt = xo*2
        yt = wh//100*20
        time.sleep(2)
        pag.press('esc')
        time.sleep(0.1)
        pag.press('r')
        time.sleep(0.2)
        pag.press('enter')
        time.sleep(8)
        for _ in range(4):
            pag.press('pgup')
        time.sleep(0.1)
        for _ in range(6):
            pag.press('o')
        #im = pag.screenshot(region = (xo,yo,xt,yt))
        #im.save('a.png')

        time.sleep(0.4)
        for _ in range(4):
            r = imagesearch.find("hive1.png",0.85, xo, yo, xt, yt)
            if r:
                time.sleep(0.1)
                for _ in range(4):
                    pag.press(".")

                time.sleep(0.1)
                for _ in range(4):
                    pag.press('pgdn')
                return
            for _ in range(4):
                pag.press(",")
            
            time.sleep(0.5)
        time.sleep(1)
    for _ in range(4):
        pag.press(",")
    webhook("","Cannot find hive. Now undergoing threshold method.","dark brown",1)
    vals = []
    for _ in range(1):
        webhook("","Obtaining values","dark brown")
        pag.moveTo(350,100)
        ww = savedata["ww"]
        wh = savedata["wh"]
        xo = ww//4
        yo = wh//100*90
        xt = xo*2
        yt = wh//100*20
        time.sleep(2)
        pag.press('esc')
        time.sleep(0.1)
        pag.press('r')
        time.sleep(0.2)
        pag.press('enter')
        time.sleep(8)
        for _ in range(4):
            pag.press('pgup')
        time.sleep(0.1)
        for _ in range(6):
            pag.press('o')
        #im = pag.screenshot(region = (xo,yo,xt,yt))
        #im.save('a.png')

        time.sleep(0.4)
        for _ in range(4):
            r = imagesearch.find("hive1.png",0, xo, yo, xt, yt)
            vals.append(r[0])
            for _ in range(4):
                pag.press(",")
            
            time.sleep(0.5)
        time.sleep(1)
    vals = sorted(vals,reverse=True)
    thresh = (vals[1]+vals[2])/2
    for _ in range(4):
        pag.press(",")
        webhook("","Now attempting to find hive","dark brown")
        pag.moveTo(350,100)
        ww = savedata["ww"]
        wh = savedata["wh"]
        xo = ww//4
        yo = wh//100*90
        xt = xo*2
        yt = wh//100*20
        time.sleep(2)
        pag.press('esc')
        time.sleep(0.1)
        pag.press('r')
        time.sleep(0.2)
        pag.press('enter')
        time.sleep(8)
        for _ in range(4):
            pag.press('pgup')
        time.sleep(0.1)
        for _ in range(6):
            pag.press('o')
        #im = pag.screenshot(region = (xo,yo,xt,yt))
        #im.save('a.png')

        time.sleep(0.4)
        for _ in range(4):
            r = imagesearch.find("hive1.png",thresh, xo, yo, xt, yt)
            vals.append(r[0])
            if r:
                time.sleep(0.1)
                for _ in range(4):
                    pag.press(".")

                time.sleep(0.1)
                for _ in range(4):
                    pag.press('pgdn')
                return True
            for _ in range(4):
                pag.press(",")
            
            time.sleep(0.5)
        time.sleep(1)
    for _ in range(4):
        pag.press(",")
    return False
    webhook("Notice","Hive not found. Assume that player is facing the right direction","red",1)

