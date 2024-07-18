import cv2
import numpy as np
import mss
import mss.tools
import pyautogui as pag
from PIL import Image
import os
import time

mw, mh = pag.size()

def roblox():
    cmd = """
    osascript -e 'activate application "Roblox"' 
    """
    os.system(cmd)
    time.sleep(3)

def terminal():
    cmd = """
    osascript -e 'activate application "Terminal"' 
    """
    os.system(cmd)
    
def mssScreenshot(x,y,w,h):
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"left": x, "top": y, "width": w, "height": h}
        # Grab the data and convert to pillow img
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        return img
    
redcannon = cv2.imread('./sussers.png')
def ebutton(pagmode=0):
    img = mssScreenshot(mw//2-200,20,400,125)
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    res = cv2.matchTemplate(img_cv, redcannon, cv2.TM_CCOEFF_NORMED)
    print(cv2.minMaxLoc(res))
    return (res >= 0.9).any()
roblox()
print(ebutton())
terminal()
