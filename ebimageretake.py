import pyautogui as pag
import os
import tkinter
import move
import loadsettings
import time
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
cmd = """
        osascript -e  'activate application "Roblox"'
    """
os.system(cmd)
time.sleep(1)
setdat = loadsettings.load()
xo = ww//2.6
yo = wh//19
xt = ww//25
yt = wh//30
im = pag.screenshot(region = (xo,yo,xt,yt))
if setdat['display_type'] ==  "built-in retina display":
    im.save('./images/retina/eb.png')
else:
    im.save('./images/built-in/eb.png')
    
