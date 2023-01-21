
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
for _ in range(1):
    webhook("","Obtaining: max_val","dark brown")
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
