import mss
from PIL import Image
import mss.tools
import time
import pyautogui as pag
import numpy as np
mw, mh = pag.size()
#returns an NP array, useful for cv2
def mssScreenshotNP(x,y,w,h, save = False):
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"left": int(x), "top": int(y), "width": int(w), "height": int(h)}
        # Grab the data and convert to opencv img
        sct_img = sct.grab(monitor)
        if save: mss.tools.to_png(sct_img.rgb, sct_img.size, output=f"screen-{time.time()}.png")
        return np.array(sct_img)


def mssScreenshot(x=0,y=0,w=mw,h=mh, save = False):
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"left": int(x), "top": int(y), "width": int(w), "height": int(h)}
        # Grab the data and convert to pillow img
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        if save: mss.tools.to_png(sct_img.rgb, sct_img.size, output=f"screen-{time.time()}.png")
        return img

def screenshotScreen(path, region = None):
    with mss.mss() as sct:
        if region is None:
            sct.shot(output=path)
        else:
            monitor = {"left": int(region[0]), "top": int(region[1]), "width": int(region[2]), "height": int(region[3])}
            sct_img = sct.grab(monitor)
            # Save to the picture file
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=path)
