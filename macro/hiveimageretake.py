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
pag.moveTo(350,100)
ww = savedata["ww"]
wh = savedata["wh"]
xo = ww//4
yo = wh-2
xt = ww//8
yt = 2
im = pag.screenshot(region = (xo,yo,xt,yt))

if setdat['display_type'] ==  "built-in retina display":
    im.save('./images/retina/hive1.png')
else:
    im.save('./images/built-in/hive1.png')

time.sleep(0.4)
time.sleep(2)
for _ in range(4):
    move.press(",")
xo = ww//4
yo = wh//4*3
xt = xo*3-xo
yt = wh-yo
r = imagesearch.find("hive1.png",0, xo, yo, xt, yt)
print("threshold is {}".format(r[3]))
    
