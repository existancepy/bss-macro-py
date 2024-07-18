import pyautogui as pg
import numpy as np
import cv2 as cv
from PIL import ImageGrab, Image
import time
import os
import mss
import mss.tools
import pyautogui as pag

REGION = (0, 0, 400, 400)
imgNames = ["day", "night", "day-gifted", "night-gifted", "noshadow-gifted", "noshadow-day", "noshadow-night", "wing"]
imgs = []
for x in imgNames:
    imgs.append(cv.imread(f'./images/general/{x}.png'))

mw, mh = pag.size()
def screenshot():
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"left": 0, "top": 3/4*mh, "width": mw, "height": mh/4}
        # Grab the data and convert to pillow img
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        return img

def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(
            f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap



@timing
def benchmark_opencv_pil(x, method = 'cv.TM_CCOEFF_NORMED'):
    img = screenshot()
    img_cv = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
    res = cv.matchTemplate(img_cv, x, method)
    print(cv.minMaxLoc(res))
    return (res >= 0.9).any()


if __name__ == "__main__":
    cmd = """
    osascript -e 'activate application "Roblox"' 
    """
    os.system(cmd)
    time.sleep(2)

    for x in imgs:
        im_opencv = benchmark_opencv_pil(x)
        print(im_opencv)

        
    cmd = """
    osascript -e 'activate application "Terminal"' 
    """
    os.system(cmd)
