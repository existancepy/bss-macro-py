self.keyboard.slowPress("e")
sleep(0.52)
self.keyboard.keyDown("w")
self.keyboard.slowPress("space")
self.keyboard.slowPress("space")
sleep(5.35)
self.keyboard.keyUp("w")
time.sleep(2.2)
self.keyboard.walk("w", 1.7)


targetY = self.mh/1.3
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
for _ in range(int(3/0.02)):
    self.keyboard.walk("w", 0.02)
    screen = mssScreenshotNP(0, 100, self.mw/2, self.mh-200)
    res = findColorObjectHSL(screen, [(270, 25, 20), (310, 80, 80)], kernel=kernel, best=2, draw=False)
    if res:
        res = max(res, key=lambda x: x[1])
        if res[1]/2+100 >= targetY:
            self.logger.webhook("","Aligned with gummy bee","dark brown", "screen")
            break 
else:
    self.logger.webhook("Notice","Could not detect gummy bee's location","red", "screen")
    #self.keyboard.walk("w",2.48)
itemCoords = self.findItemInInventory("gumdrops")
if itemCoords is not None:
    self.keyboard.walk("a",1.4)
    self.keyboard.walk("w",0.15)
    self.keyboard.walk("a",0.3)
    time.sleep(0.3)
    self.keyboard.press("space")
    time.sleep(0.1)
    self.keyboard.walk("w",0.1)
    self.useItemInInventory(x=itemCoords[0], y=itemCoords[1])
    self.canDetectNight = False #dont let night be detected inside gummy bear's lair
    time.sleep(2)
    self.keyboard.walk("w",2.5)
    time.sleep(0.5)
    self.canDetectNight = True

