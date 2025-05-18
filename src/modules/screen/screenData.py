#update the screen user data
import pyautogui as pag
import numpy as np
import subprocess
import sys
import os
from ..misc import settingsManager
screenPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/user/screen.txt'))
def setScreenData():
    #get screen info
    multiplierData = {
        #ysm, xsm, ylm,  xlm
        "2880x1800": [1,1,1,1],
        "2940x1912": [1.1,0.98,1,1.2],
        "1920x1080": [1.2,0.92,1.3,1.5],
        "1440x900": [1,1,1,1],
        "1366x768": [0.8,1,1,1.2],
        "4096x2304": [1.45,0.91,1.32,1.5],
        "3024x1964": [1,0.98, 1.2, 1.2],
        "3360x2100": [1.2,0.95,1.2,1.3],
        "4480x2520": [1.4,0.89,1.4,1.9],
        "3600x2338": [1.45,0.93,1.2,1.6],
        "3584x2240": [1.3, 0.93, 1.2, 1.5],
        "1280x800": [0.9,1.03,1,1],
        "3840x2160": [1.13,0.92,1.3,1.5],
        "3456x2234": [1.2, 0.93, 1.3, 1.6],
        "2560x1600": [0.9, 1.02, 1, 1.1],
        "2560x1440": [1.45,0.87,1.8,2.2],
        "5120x2880": [1.4,0.87,1.7,2],
        "3420x2224":[0.81, 0.95, 1.12, 1.24],
        "3840x2486": [1.3, 0.92, 1.45, 1.45],
        "3420x2214":[0.9, 0.95, 1.1, 1.15],
        "3440x1440": [1.6, 0.84, 1.6, 2.3]
    }

    wwd, whd = pag.size()
    screenData = {
        "display_type": "built-in",
        "screen_width": wwd,
        "screen_height": whd,
        "y_multiplier": 1,
        "x_multiplier": 1,
        "y_length_multiplier":1,
        "x_length_multiplier":1
    }

    #for macs: check if its reina, set the screen width and height, set multipliers
    if sys.platform == "darwin":
        #get a screenshot. The size of the screenshot is the true screen size
        sh, sw, _ = np.array(pag.screenshot()).shape
        if whd*2 == sh: #check if retina (screenshot size is twice pyautogui's size)
            screenData["screen_width"] = sw
            screenData["screen_height"] = sh
            screenData["display_type"] = "retina"
            print("display type: retina")
            
        else:
            print("display type: built-in")
        print("Screen coordinates: {}x{}".format(sw,sh))
        ndisplay = "{}x{}".format(sw,sh)
        #get multipliers
        if ndisplay in multiplierData:
            screenData["y_multiplier"] = multiplierData[ndisplay][0]
            screenData["x_multiplier"] = multiplierData[ndisplay][1]
            screenData["y_length_multiplier"] = multiplierData[ndisplay][2]
            screenData["x_length_multiplier"] = multiplierData[ndisplay][3]
    #save the data
    settingsManager.saveDict(screenPath, screenData)

def getScreenData():
    return settingsManager.readSettingsFile(screenPath)
