from modules.misc.imageManipulation import pillowToCv2
from modules.screen.screenshot import mssScreenshot
from modules.misc.appManager import openApp
from modules.controls.keyboard import keyboard
import numpy as np
import cv2
import time
import pyautogui as pag

mw, mh = pag.size()

class fieldDriftCompensation():
    def __init__(self, isRetina):
        self.isRetina = isRetina
        #double pixel coordinates, double kernel size
        if isRetina:
            self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(15,15))
        else:
            self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(8,8))
    #imgSRC is a cv2 img
    def getSaturatorInImage(self, imgSRC):
        imgHLS = cv2.cvtColor(imgSRC, cv2.COLOR_BGR2HLS)

        sLow = 250
        sHi = 255
        lLow = 120
        lHi = 200
        hLow = 170/2
        hHi = 220/2

        # Apply thresholds to each channel (H, L, S)
        binary_mask = cv2.inRange(
            cv2.cvtColor(imgHLS, cv2.COLOR_BGR2HLS),
            np.array([hLow, lLow, sLow], dtype=np.uint8),
            np.array([hHi, lHi, sHi], dtype=np.uint8)
            )
        
        binary_mask = cv2.erode(binary_mask, self.kernel, iterations=1)
        contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours: return None
        # return the bounding with the largest area
        x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
        #display results
        '''
        cv2.rectangle(imgSRC, (x, y), (x+w, y+h), (0, 255, 0), 2)
        imgRST = cv2.bitwise_and(imgHLS, imgMSK)
        imgBGR = cv2.cvtColor(imgRST, cv2.COLOR_HLS2BGR)
        cv2.imshow("src", imgSRC)
        cv2.imshow("result", imgBGR)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        '''
        #get the center and return its coordinates
        return (x+w//2, y+h//2)

    def getSaturatorLocation(self):
        saturatorLocation = self.getSaturatorInImage(pillowToCv2(mssScreenshot(0,100, mw, mh-100)))
        if saturatorLocation is None: return None
        x,y = saturatorLocation
        if self.isRetina:
            x /= 2
            y /= 2
        y += 100
        return (x,y)
        
    def press(self, k,t):
        keyboard.keyDown(k, False)
        time.sleep(t)
        keyboard.keyUp(k, False)
        
    def slowFieldDriftCompensation(self, initialSaturatorLocation):
        winUp, winDown = mh/2.14, mh/1.88
        winLeft, winRight = mw/2.14, mw/1.88
        saturatorLocation = initialSaturatorLocation
        for _ in range(8):
            if saturatorLocation is None: break #cant find saturator
            x,y = saturatorLocation
            if x >= winLeft and x <= winRight and y >= winUp and y <= winDown: 
                break
            if x < winLeft:
                self.press("a",0.2)
            elif x > winRight:
                self.press("d",0.2)
            if y < winUp:
                self.press("w",0.2)
            elif y > winDown:
                self.press("s",0.2)

            saturatorLocation = self.getSaturatorLocation()

    #natro's field drift compensation
    #works well with fast detection times (<0.2s)
    def fastFieldDriftCompensation(self, initialSaturatorLocation):
        
        winUp, winDown = mh/2.14, mh/1.88
        winLeft, winRight = mw/2.14, mw/1.88
        hmove, vmove = "", ""
        st = time.time()
        if initialSaturatorLocation:
            x,y = initialSaturatorLocation

            #move towards saturator
            if x >= winLeft and x <= winRight and y >= winUp and y <= winDown: 
                return
            if x < winLeft:
                keyboard.keyDown("a", False)
                hmove = "a"
            elif x > winRight:
                keyboard.keyDown("d", False)
                hmove = "d"
            if y < winUp:
                keyboard.keyDown("w", False)
                vmove = "w"
            elif y > winDown:
                keyboard.keyDown("s", False)
                vmove = "s"

            i = 0
            while hmove or vmove:
                #check if reached saturator
                if (hmove == "a" and x >= winLeft) or (hmove == "d" and x <= winRight):
                    keyboard.keyUp(hmove, False)
                    hmove = ""
                    
                if (vmove == "w" and y >= winUp) or (vmove == "s" and y <= winDown):
                    keyboard.keyUp(vmove, False)
                    vmove = ""
                
                time.sleep(0.02)
                #taking too long, just give up
                if i >= 100:
                    print("give up")
                    keyboard.releaseMovement()
                    break
                #update saturator location
                saturatorLocation = self.getSaturatorLocation()
                if saturatorLocation is not None:
                    x,y = saturatorLocation

                else: #cant find saturator, pause
                    keyboard.releaseMovement()
                    #try to find saturator
                    for _ in range(10):
                        time.sleep(0.02)
                        saturatorLocation = self.getSaturatorLocation()
                        #saturator found
                        if saturatorLocation:
                            #move towards saturator
                            if hmove:
                                keyboard.keyDown(hmove)
                            if vmove:
                                keyboard.keyDown(vmove)
                            x,y = saturatorLocation
                            break
                    else: #still cant find it, give up
                        return
                i += 1
                
    def run(self):
        #calculate how fast it takes to get the saturator and determine if the fast or slow version should be used
        st = time.time()
        saturatorLocation = self.getSaturatorLocation()
        timing = time.time()-st
        if timing > 0.25:
            self.slowFieldDriftCompensation(saturatorLocation)
        else:
            self.fastFieldDriftCompensation(saturatorLocation)