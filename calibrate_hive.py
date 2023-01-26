
import pyautogui as pag
import time
import os
import tkinter
import loadsettings
import move

cmd = """
osascript -e 'activate application "Roblox"' 
"""
os.system(cmd)
time.sleep(2)
    
webhook("","Calibrating: Hive","dark brown",1)
vals = []
def loadSave():
    info = {}
    with open('save.txt') as f:
        lines = f.read().split("\n")
    f.close()
    for s in lines:
        l = s.replace(" ","").split(":")
        if l[1].isdigit():
            l[1] = int(l[1])
        info[l[0]] = l[1]
    return info
        
for _ in range(1):
    webhook("","Obtaining: max_val","dark brown")
    savedata = loadSave()
    pag.moveTo(350,100)
    ww = savedata["ww"]
    wh = savedata["wh"]
    xo = ww//4
    yo = wh//4*3
    xt = xo*3-xo
    yt = wh-yo
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
        vals.append(r[3])
        for _ in range(4):
            pag.press(",")
        
        time.sleep(0.5)
    time.sleep(1)
vals = sorted(vals,reverse=True)
print(vals)
thresh = (vals[1]+vals[2])/2
webhook("","Calculated: Threshold\nValue: {}".format(thresh),"dark brown")
loadsettings.save("hivethreshold",thresh)
