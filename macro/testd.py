import pyautogui as pg
import numpy as np
import cv2 as cv
from PIL import ImageGrab, Image
import time
import os
import mss
import mss.tools

REGION = (0, 0, 400, 400)
GAME_OVER_PICTURE_PIL = Image.open("./images/general/e2.png")
GAME_OVER_PICTURE_CV = cv.imread('./images/general/e2.png')

def screenshot():
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"left": 1440/2-200, "top": 20, "width": 400, "height": 125}
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
def benchmark_pyautogui():
    res = pg.locateOnScreen(GAME_OVER_PICTURE_PIL,
                            grayscale=True,  # should provied a speed up
                            confidence=0.8,
                            region=REGION)
    return res is not None


@timing
def benchmark_opencv_pil(method):
    img = screenshot()
    img_cv = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
    res = cv.matchTemplate(img_cv, GAME_OVER_PICTURE_CV, method)
    print(cv.minMaxLoc(res))
    return (res >= 0.9).any()


if __name__ == "__main__":
    cmd = """
    osascript -e 'activate application "Roblox"' 
    """
    os.system(cmd)
    time.sleep(2)

    methods = ['cv.TM_CCOEFF_NORMED','cv.TM_CCOEFF','cv.TM_CCORR', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']


    # cv.TM_CCOEFF_NORMED actually seems to be the most relevant method
    for method in methods:
        print(method)
        im_opencv = benchmark_opencv_pil(eval(method))
        print(im_opencv)
        
    cmd = """
    osascript -e 'activate application "Terminal"' 
    """
    os.system(cmd)
