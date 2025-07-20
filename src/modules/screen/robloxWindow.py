import pyautogui as pag
from modules.screen import screenData
from operator import itemgetter
from modules.misc.appManager import getWindowSize
from PIL import Image
from modules.screen.screenshot import mssScreenshotPillowRGBA
from modules import bitmap_matcher

class RobloxWindowBounds:
    '''
    Class to handle roblox window info and bss y offset
    '''

    def __init__(self):
        self.screenw, self.screenh = pag.size()
        self.mx = 0
        self.my = 0
        self.mw = self.screenw
        self.mh = self.screenh
        self.yOffset = 21 #bss offset due to the new ui
        self.contentYOffset = 0 #get area of content (excludes title bar/tab bar)

        screenInfo = screenData.getScreenData()
        self.display_type, self.ww, self.wh, self.ysm, self.xsm, self.ylm, self.xlm = itemgetter("display_type", "screen_width","screen_height", "y_multiplier", "x_multiplier", "y_length_multiplier", "x_length_multiplier")(screenInfo)
        self.isRetina = self.display_type == "retina"
        self.multi = 2 if self.isRetina else 1 #used for pixel calculation compatibility between retina and non-retina displays
    
    def setRobloxWindowBounds(self, setYOffset = True):
        self.mx, self.my, self.mw, self.mh = getWindowSize("roblox roblox")

        #calculate y offset and the actual roblox content bounds
        if setYOffset:
            honeyImg = Image.open(f"./images/menu/honeybar-{self.display_type}.png").convert('RGBA')
            screen = mssScreenshotPillowRGBA(self.mx,self.my,self.mw,self.mh//3)
            res = bitmap_matcher.find_bitmap_cython(screen, honeyImg, variance=5)
            if res:
                self.contentYOffset = max((res[1]//self.multi)-15-self.yOffset, 0)
                self.my+=self.contentYOffset
                self.mh-=self.contentYOffset
            
        


