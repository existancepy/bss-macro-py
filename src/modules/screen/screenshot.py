import mss
import mss.darwin
mss.darwin.IMAGE_OPTIONS = 0
from PIL import Image
import mss.tools
import time
import pyautogui as pag
import numpy as np
import cv2
import time
import os
import tempfile
import subprocess
import Quartz.CoreGraphics as CG
from modules.screen.screenData import getScreenData
from modules.misc.appManager import getWindowSize

mw, mh = pag.size()
multi = 2 if getScreenData()["display_type"] == "retina" else 1
'''
Theres an issue for a few people where the mss screenshot takes almost a minute to run in the macro process.
This seems to affect any screenshots taken with quartz, but not those taken with filepath
'''
usePillow = False

def pillowGrab(x,y,w,h):
    fh, filepath = tempfile.mkstemp(".png")
    os.close(fh)
    args = ["screencapture"]
    subprocess.call(args + ["-x", filepath])
    im = Image.open(filepath)
    im.load()
    os.unlink(filepath)
    bbox = (x, y, x + w, y + h)
    im_cropped = im.crop(bbox)
    im.close()
    return im_cropped

def cgGrab(region=None):
    # Set up the screen capture rectangle
    if region:
        left, top, width, height = region
    else:
        main_display_id = CG.CGMainDisplayID()
        width = CG.CGDisplayPixelsWide(main_display_id)
        height = CG.CGDisplayPixelsHigh(main_display_id)
        left, top = 0, 0

    rect = CG.CGRectMake(left, top, width, height)

    # Capture the screen region as an image
    image_ref = CG.CGWindowListCreateImage(
        rect,
        CG.kCGWindowListOptionOnScreenOnly,
        CG.kCGNullWindowID,
        CG.kCGWindowImageDefault
    )

    # Get image width/height and raw pixel data
    width = CG.CGImageGetWidth(image_ref)
    height = CG.CGImageGetHeight(image_ref)
    bytes_per_row = CG.CGImageGetBytesPerRow(image_ref)
    data_provider = CG.CGImageGetDataProvider(image_ref)
    data = CG.CGDataProviderCopyData(data_provider)

    # Convert to NumPy array
    img = np.frombuffer(data, dtype=np.uint8).reshape((height, bytes_per_row // 4, 4))
    img = img[:, :width, :]  # Trim padding if needed

    # Convert to PIL Image (in BGRA format)
    return img
 
#returns an NP array, useful for cv2
def mssScreenshotNP(x,y,w,h, save = False):
    #return cgGrab((x,y,w,h))
    if usePillow:
        screen = pillowGrab(int(x*multi),int(y*multi),int(w*multi),int(h*multi))
        screen = np.array(screen)
        screen_bgra = cv2.cvtColor(screen, cv2.COLOR_RGB2BGRA)
        return screen_bgra

    else:
        with mss.mss() as sct:
            # The screen part to capture
            monitor = {"left": int(x), "top": int(y), "width": int(w), "height": int(h)}
            # Grab the data and convert to opencv img
            sct_img = sct.grab(monitor)
            if save: mss.tools.to_png(sct_img.rgb, sct_img.size, output=f"screen-{time.time()}.png")
            return np.array(sct_img)


def mssScreenshot(x=0,y=0,w=mw,h=mh, save = False, filename=None):
    # img = cgGrab((x,y,w,h))
    # img = img[:, :, [2, 1, 0]]
    # img = Image.fromarray(img, 'RGB')
    # return img
    if usePillow:
        return pillowGrab(int(x*multi),int(y*multi),int(w*multi),int(h*multi))
    else:
        with mss.mss() as sct:
            # The screen part to capture
            monitor = {"left": int(x), "top": int(y), "width": int(w), "height": int(h)}
            # Grab the data and convert to pillow img
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            if save: mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename if filename else f"screen-{time.time()}.png")
            return img

def screenshotRobloxWindow(filename = None, regionMultipliers = None):
    res = getWindowSize("roblox roblox")
    if res:
        x,y,w,h = res
    else:
        x = 0
        y = 0
        w = mw
        h = mh
    if regionMultipliers:
        x = x*regionMultipliers[0] if regionMultipliers[0] <= 1 else regionMultipliers[0]
        y *= y*regionMultipliers[1] if regionMultipliers[1] <= 1 else regionMultipliers[1]
        w *= w*regionMultipliers[2] if regionMultipliers[2] <= 1 else regionMultipliers[2]
        h *= h*regionMultipliers[3] if regionMultipliers[3] <= 1 else regionMultipliers[3]
    return mssScreenshot(x,y,w,h, save=bool(filename), filename=filename)

def benchmarkMSS():
    global usePillow
    try:
        with mss.mss() as sct:
            monitor = {"left": 0, "top": 0, "width": 100, "height": 100}
            start = time.time()
            sct.grab(monitor)
            duration = time.time() - start
            if duration > 1:
                print(f"MSS took {duration:.2f}s — switching to Pillow.")
                usePillow = True
            else:
                print(f"MSS is fast enough: {duration:.2f}s")
                return True
    except Exception as e:
        print(f"[ERROR] MSS failed: {e} — switching to Pillow.")
        usePillow = True
    
    return False

#returns a rgba pillow screenshot
def mssScreenshotPillowRGBA(x=0,y=0,w=mw,h=mh):   
    with mss.mss() as sct:
        monitor = {"left": int(x), "top": int(y), "width": int(w), "height": int(h)}
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGBA", sct_img.size, sct_img.bgra, "raw", "BGRA")
        #img.save(f"buff_area.png")
        return img