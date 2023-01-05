import pyautogui as pag
import time
import os
import tkinter
import imagesearch

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
    pag.moveTo(350,100)
    ww = savedata["ww"]
    wh = savedata["wh"]
    xo = ww//4
    yo = wh//4*3
    xt = xo*3
    yt = wh
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
            break
        for _ in range(4):
            pag.press(",")
        time.sleep(0.5)
    time.sleep(1)

