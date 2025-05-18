import cv2
import pyautogui as pag
from modules.screen.imageSearch import templateMatch
from modules.screen.screenshot import mssScreenshot, mssScreenshotNP
import numpy as np
import time
from PIL import Image
from modules.misc.imageManipulation import pillowToCv2
from concurrent.futures import ThreadPoolExecutor

class HasteCompensation():
    def __init__(self, isRetina, baseMoveSpeed):
        self.isRetina = isRetina
        self.baseMoveSpeed = baseMoveSpeed

        self.hasteStacks = []
        for i in range(10):
            self.hasteStacks.append(self.adjustBuffImage(f"./images/buffs/haste{i+1}.png"))
        self.hasteStacks = list(enumerate(self.hasteStacks))[::-1]

        self.bearMorphs = []
        for i in range(5):
            self.bearMorphs.append(self.adjustBuffImage(f"./images/buffs/bearmorph{i+1}-retina.png", grayscale=True))

        self.hastePlus = self.adjustBuffImage(f"./images/buffs/haste+.png")         
        self.mw, self.mh = pag.size()                 
        self.prevHaste = 0         
        self.prevHaste368 = 0 #tracking the previous haste to accurately determine if the haste stack is 3,6 or 8
        self.hasteEnds = 0
        self.prevHasteEnds = 0


    def adjustBuffImage(self, path, grayscale=False):
        img = Image.open(path)
        #get original size of image
        width, height = img.size
        #if its built-in, half the image
        scaling = 1 if self.isRetina else 2
        #resize image
        img = img.resize((int(width/scaling), int(height/scaling)))
        #convert to cv2
        img = pillowToCv2(img)
        if grayscale:
                return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        return pillowToCv2(img)

    def thresholdMatch(self, target, screen, threshold=0.7):
        res = templateMatch(target, screen)
        _, val, _, loc = res
        return (val > threshold, val)

    def getHaste(self):
        st = time.perf_counter()
        screen = np.array(mssScreenshot(0,30,self.mw/1.8,70))
        screenGray = cv2.cvtColor(screen.copy(), cv2.COLOR_RGB2GRAY)
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
            elif self.prevHaste368 == 7:
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
        bearMorph = any(self.thresholdMatch(x, screenGray, 0.75)[0] for x in self.bearMorphs)
        if bearMorph: 
            bearMorph = 4
        
        #match haste+
        if self.thresholdMatch(self.hastePlus, screen, 0.75)[0]:
            hasteOut += 10
        #print(f"Haste stacks: {hasteOut}, Bear: {bearMorph}") # Debug
        out = (self.baseMoveSpeed+bearMorph)*(1+(0.1*hasteOut))
        
        return out

class HasteCompensationOptimized():
    mw, mh = pag.size() 
    BUFF_REGION = (0, 30, int(mw / 1.8), 70)

    def __init__(self, isRetina, baseMoveSpeed):
        self.isRetina = isRetina
        self.baseMoveSpeed = baseMoveSpeed
        self.buff_region = HasteCompensationOptimized.BUFF_REGION

        #load templates
        self.hasteStacks = []
        for i in range(10):
            img = self._loadTemplate(f"./images/buffs/haste{i+1}.png")
            self.hasteStacks.append(img)
        #store as (index, template) pairs
        self.hasteStacks = list(enumerate(self.hasteStacks))[::-1] 

        self.bearMorphs = []
        for i in range(5):
            # Prepare bear morph templates
            img = self._loadTemplate(f"./images/buffs/bearmorph{i+1}-retina.png")
            self.bearMorphs.append(img)

        #no gray, haste+ is color-dependent
        self.hastePlus = self._loadTemplate(f"./images/buffs/haste+.png", gray=False)

        self.prevHaste = 0
        self.prevHaste368 = 0
        self.hasteEnds = 0
        self.prevHasteEnds = 0

    def _loadTemplate(self, path, gray=True):
        try:
            img = Image.open(path)
            width, height = img.size
            #scale based on display type
            scaling = 1 if self.isRetina else 2
            img = img.resize((int(width / scaling), int(height / scaling)))
            #convert to cv2
            cv2Img = np.array(img)
            if gray:
                return cv2.cvtColor(cv2Img, cv2.COLOR_RGB2GRAY)
            else:
                return cv2.cvtColor(cv2Img, cv2.COLOR_RGB2BGR)

        except FileNotFoundError:
            print(f"Warning: Template image not found at {path}")
            return None # Handle missing files gracefully
        except Exception as e:
            print(f"Error processing template {path}: {e}")
            return None

    def _thresholdMatch(self, target_template, screen_grayscale, threshold=0.7):
        """Performs template matching on grayscale images."""
        if target_template is None: # Skip if template failed to load
             return (False, 0.0)
             
        res = cv2.matchTemplate(screen_grayscale, target_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        return (max_val > threshold, max_val)


    def getHaste(self):
        screenBGR = cv2.cvtColor(mssScreenshotNP(self.buff_region[0], self.buff_region[1], self.buff_region[2], self.buff_region[3]), cv2.COLOR_RGBA2BGR)

        screen_grayscale = cv2.cvtColor(screenBGR, cv2.COLOR_BGR2GRAY)

        bestHaste = 0
        bestHasteMaxVal = 0
        for i, template in self.hasteStacks:
            if template is None: continue
       
            res, val = self._thresholdMatch(template, screen_grayscale, 0.75) 
            if res and val > bestHasteMaxVal:
                bestHasteMaxVal = val
                bestHaste = i + 1 # i is the 0-based index


        #3, 6, 8 can be misrecognised as each other
        if bestHaste in [3, 6, 8]:
            if self.prevHaste368 == 2: 
                bestHaste = 3
            elif self.prevHaste368 == 5: 
                bestHaste = 6 
            elif self.prevHaste368 == 7:
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

        #match bear
        bearMorph = 0 
        bear_threshold = 0.75
        for template in self.bearMorphs:
            if template is None: continue
            if self._thresholdMatch(template, screen_grayscale, bear_threshold)[0]:
                bearMorph = 4
                break

        #match haste+
        haste_plus_threshold = 0.75
        if self._thresholdMatch(self.hastePlus, screenBGR, haste_plus_threshold)[0]:
            print("hastePlus")
            hasteOut += 10

        #print(f"Haste stacks: {hasteOut}, Bear: {bearMorph}")
        final_speed = (self.baseMoveSpeed + bearMorph) * (1 + (0.1 * hasteOut))

        # print(f"Calculation time: {time.perf_counter() - st:.4f}s") # Debug timing
        return final_speed
    
class HasteCompensationFastest():
    mw, mh = pag.size() 
    BUFF_REGION = (0, 30, int(mw / 1.8), 70)

    def __init__(self, isRetina, baseMoveSpeed):
        self.isRetina = isRetina
        self.baseMoveSpeed = baseMoveSpeed
        self.buff_region = HasteCompensationOptimized.BUFF_REGION

        # --- Optimization 2: Preload and Preprocess Templates ---
        self.hasteStacks = []
        for i in range(10):
            # Load, resize, and convert to grayscale ONCE during initialization
            img = self._load_and_prepare_template(f"./images/buffs/haste{i+1}.png")
            self.hasteStacks.append(img)
        # Store as (index, template) pairs, reversed order is already handled
        self.hasteStacks = list(enumerate(self.hasteStacks))[::-1] 

        self.bearMorphs = []
        for i in range(5):
            # Prepare bear morph templates
            img = self._load_and_prepare_template(f"./images/buffs/bearmorph{i+1}-retina.png")
            self.bearMorphs.append(img)

        # Prepare haste+ template
        self.hastePlus = self._load_and_prepare_template(f"./images/buffs/haste+.png")

        self.prevHaste = 0
        self.prevHaste368 = 0 # Tracking previous haste for 3/6/8 ambiguity
        self.hasteEnds = 0
        self.prevHasteEnds = 0 # Value used during compensation period

    def _load_and_prepare_template(self, path):
        """Loads, resizes, converts to CV2 format, and converts to grayscale."""
        try:
            img = Image.open(path)
            # Get original size
            width, height = img.size
            # Adjust scaling based on Retina display
            scaling = 1 if self.isRetina else 2
            # Resize image
            new_width = max(1, int(width / scaling)) # Ensure width is at least 1
            new_height = max(1, int(height / scaling)) # Ensure height is at least 1
            img = img.resize((new_width, new_height))
            # Convert to cv2 format (ensure it returns BGR)
            cv2_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            # --- Optimization 3: Convert Templates to Grayscale ---
            # Template matching is often faster on grayscale images
            gray_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
            return gray_img
        except FileNotFoundError:
            print(f"Warning: Template image not found at {path}")
            return None # Handle missing files gracefully
        except Exception as e:
            print(f"Error processing template {path}: {e}")
            return None

    def _thresholdMatch(self, target_template, screen_grayscale, threshold=0.7):
        """Performs template matching on grayscale images."""
        if target_template is None: # Skip if template failed to load
             return (False, 0.0)
             
        res = cv2.matchTemplate(screen_grayscale, target_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # For TM_CCOEFF_NORMED, the best match is the max_val
        # print(f"Matching {target_template.shape} against {screen_grayscale.shape}: MaxVal={match_value:.2f}") # Debug

        # _, val, _, loc = res # Original line assumes templateMatch returns this tuple
        # Using max_val from cv2.minMaxLoc directly:
        return (max_val > threshold, max_val)


    def getHaste(self):
        st = time.perf_counter() # Keep for timing checks


        screen_cv2 = cv2.cvtColor(mssScreenshotNP(self.buff_region[0], self.buff_region[1], 
                                   self.buff_region[2], self.buff_region[3]), cv2.COLOR_RGBA2BGR)

        screen_grayscale = cv2.cvtColor(screen_cv2, cv2.COLOR_BGR2GRAY)

        bestHaste = 0
        bestHasteMaxVal = 0

        # Match haste stacks (templates are already grayscale)
        def match_haste(args):
            i, template = args
            res, val = self._thresholdMatch(template, screen_grayscale, 0.7)
            return (i, res, val)
        
        with ThreadPoolExecutor(max_workers=6) as executor:
            args = [(i, template) for i, template in self.hasteStacks]
            results = executor.map(match_haste, args)

        for haste, res, val in results:
            if res and val > bestHasteMaxVal:
                bestHaste = haste+1
                bestHasteMaxVal = val

        # Ambiguity resolution for 3, 6, 8
        if bestHaste in [3, 6, 8]:
            # This logic seems complex and potentially error-prone.
            # Consider if higher thresholds or different template images
            # could distinguish these better.
            if self.prevHaste368 == 2: 
                bestHaste = 3 # Confirmed 3
            elif self.prevHaste368 == 5: 
                bestHaste = 6 # Confirmed 6
            else: bestHaste = 8 # Default to 8 if ambiguity detected without clear precursor?
        else:
            self.prevHaste368 = bestHaste # Update tracker state


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

        # Match bear morph (using any() for efficiency)
        bearMorph = 0 # Default to 0
        def match_bear(template):
            return self._thresholdMatch(template, screen_grayscale, 0.75)[0]
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = executor.map(match_bear, self.bearMorphs)
            
        if any(results):
            bearMorph = 4

        # Match haste+
        haste_plus_threshold = 0.75
        if self._thresholdMatch(self.hastePlus, screen_grayscale, haste_plus_threshold)[0]:
            hasteOut += 10

        # Calculate final speed
        # print(f"Haste stacks: {hasteOut}, Bear: {bearMorph}") # Debug
        final_speed = (self.baseMoveSpeed + bearMorph) * (1 + (0.1 * hasteOut))

        # print(f"Calculation time: {time.perf_counter() - st:.4f}s") # Debug timing
        return final_speed