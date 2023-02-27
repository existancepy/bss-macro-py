
import pyautogui as pag
import time
import os
import tkinter
import loadsettings
import move
import pytesseract
ws = loadsettings.load()["walkspeed"]
def ebutton(pagmode=0):
    cap = pag.screenshot(region=(ww//3,0,ww//6.5,wh//25))
    img = cv2.cvtColor(np.array(cap), cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, None, fx=1.3, fy=1.3)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    config = '--oem 3 --psm %d' % 13
    tesstr = pytesseract.image_to_string(img, config = config)
    tesstr = ''.join([x for x in tesstr if x.isdigit()])
    return tesstr

def apd(k):
    cmd = """
        osascript -e  'tell application "System Events" to key down "{}"'
    """.format(k)
    os.system(cmd)
def apu(k):
    cmd = """
        osascript -e  'tell application "System Events" to key up "{}"'
    """.format(k)
    os.system(cmd)


move.hold("s",5)
move.hold("d",6)
move.hold("w",9)
move.hold("d",2)
pag.keyDown("d")
time.sleep(0.1)
move.press("space")
time.sleep(0.15*28/ws)
pag.keyUp("d")
move.hold("w",7)
move.hold("d",4)
move.hold("s",0.5)
move.hold("a",0.1)
pag.keyDown("s")
time.sleep(0.1)
move.press("space")
time.sleep(0.1*28/ws)
pag.keyUp("s")
time.sleep(2.5)
move.press("e")
move.hold("w",4)
move.hold("d",3)
move.hold("s",0.6)


    
