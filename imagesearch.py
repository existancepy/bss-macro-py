import pyautogui as pag
import time
import os
import tkinter
import move
import cv2
from PIL import ImageGrab
import numpy as np

savedata = {}
def loadSave():
    with open('save.txt') as f:
        lines = f.read().split("\n")
    f.close()
    for s in lines:
        l = s.replace(" ","").split(":")
        if l[1].isdigit():
            l[1] = int(l[1])
        savedata[l[0]] = l[1]
loadSave()
ww = savedata["ww"]
wh = savedata["wh"]

'''
screen = np.array(ImageGrab.grab())
screen = cv2.cvtColor(src=screen, code=cv2.COLOR_BGR2RGB)

small_image = cv2.imread('./images/saturator.png')
large_image = screen
result = cv2.matchTemplate(small_image, large_image, method)
mn,_,mnLoc,_ = cv2.minMaxLoc(result)
MPx,MPy = mnLoc
print(MPx,MPy)
pag.moveTo(MPx//2,MPy//2)
# Step 2: Get the size of the template. This is the same size as the match.
trows,tcols = small_image.shape[:2]

# Step 3: Draw the rectangle on large_image
cv2.rectangle(large_image, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,255),2)

# Display the original image with the rectangle around the match.
cv2.imshow('output',large_image)

# The image is only displayed if we call this
cv2.waitKey(0)
'''

def find(img,confi, x1 = 0, y1 = 0, x2 = ww, y2 = wh):
    method = cv2.TM_CCOEFF_NORMED
    screen = pag.screenshot(region=(x1,y1,x2,y2))
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

    small_image = cv2.imread('./images/{}'.format(img))
    large_image = screen
    result = cv2.matchTemplate(small_image, large_image, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    x,y = max_loc
    print("Trying to find {}. max_val is {} ".format(img,max_val))
    if max_val >= confi:
        return [1,x,y]
    return 




