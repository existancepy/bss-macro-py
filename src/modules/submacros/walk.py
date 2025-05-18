import cv2
import pyautogui as pag
from modules.screen.imageSearch import templateMatch
from modules.screen.screenshot import mssScreenshot
from modules.screen.screenData import getScreenData
import numpy as np
import time
from PIL import Image
from modules.misc.imageManipulation import pillowToCv2


class Walk():
    def __init__(self, isRetina, baseMoveSpeed):
        self.isRetina = isRetina
        self.baseMoveSpeed = baseMoveSpeed

        self.hasteStacks = []
        for i in range(10):
            self.hasteStacks.append(self.adjustBuffImage(f"./images/buffs/haste{i+1}.png"))
        self.hasteStacks = list(enumerate(self.hasteStacks))[::-1]

        self.bearMorphs = []
        for i in range(5):
            self.bearMorphs.append(self.adjustBuffImage(f"./images/buffs/bearmorph{i+1}.png"))

        self.hastePlus = self.adjustBuffImage(f"./images/buffs/haste+.png")         
        self.mw, self.mh = pag.size()                 
        self.prevHaste = 0         
        self.prevHaste368 = 0 #tracking the previous haste to accurately determine if the haste stack is 3,6 or 8
        self.hasteEnds = 0
        self.prevHasteEnds = 0


    def adjustBuffImage(self, path):
        img = Image.open(path)
        #get original size of image
        width, height = img.size
        #if its built-in, half the image
        scaling = 1 if self.isRetina else 2
        #resize image
        img = img.resize((int(width/scaling), int(height/scaling)))
        #convert to cv2
        return pillowToCv2(img)

    def thresholdMatch(self, target, screen, threshold=0.7):
        res = templateMatch(target, screen)
        _, val, _, loc = res
        return (val > threshold, val)

    def hasteCompensation(self):
        st = time.perf_counter()
        screen = np.array(mssScreenshot(0,30,self.mw/1.8,70))
        bestHaste = 0
        bestHasteMaxVal = 0
        #match haste
        for i,e in self.hasteStacks:
            res, val = self.thresholdMatch(e, screen)
            if res and val > bestHasteMaxVal:
                bestHasteMaxVal = val
                bestHaste = i+1
        #in some cases, 3 and 6 can be detected as 8
        #assume that 8 can also be detected as 3 or 6 and others
        if bestHaste in [3,6,8]:
            if self.prevHaste368 == 2:
                bestHaste = 3
            elif self.prevHaste368 == 5:
                bestHaste = 6
            else:
                bestHaste = 8
        elif bestHaste:
            self.prevHaste368 = bestHaste

        hasteOut = bestHaste
        #failed to detect haste, but the haste is still there (~7.5 secs remaining)
        if not hasteOut:
            currTime = time.time()
            if currTime > self.hasteEnds and self.prevHaste: #there is no ongoing hasteEnds
                self.prevHasteEnds = self.prevHaste #value to set for the time compensation
                #decrease the countdown for retina (detection is more accurate)
                if self.isRetina:
                    self.hasteEnds = currTime + (0 if hasteOut == 1 else 2)
                else:
                    self.hasteEnds = currTime + (4 if hasteOut == 1 else 7)
            #there is a hasteEnd ongoing
            if currTime < self.hasteEnds:
                hasteOut = self.prevHasteEnds

        self.prevHaste = bestHaste
        #match bear morph
        bearMorph = any(self.thresholdMatch(x, screen, 0.75)[0] for x in self.bearMorphs)
        if bearMorph: 
            bearMorph = 4
            #print("bear morph active")
        
        #match haste+
        if self.thresholdMatch(self.hastePlus, screen, 0.75)[0]:
            hasteOut += 10
        #print("hastePlus")
        #if hasteOut: print(f"Haste stacks: {hasteOut}")
        out = (self.baseMoveSpeed+bearMorph)*(1+(0.1*hasteOut))
        
        et = time.perf_counter()
        return st, et, out
    
    def walk(self, n):
        freq = 1  # Simulated frequency constant
        d = freq / 8
        l = n * freq * 4  # 4 studs per tile

        s, f, v = self.hasteCompensation()  # Get initial timestamps and speed
        d += v * (f - s)  # Accumulate initial movement

        while d < l:
            prev_v = v
            s, f, v = self.hasteCompensation()  # Get new timestamps and speed
            d += ((prev_v + v) / 2) * (f - s)  # Apply trapezoidal integration

