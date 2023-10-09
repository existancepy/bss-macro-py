from paddleocr import PaddleOCR
import loadsettings
import pyautogui as pag
import numpy as np
from logpy import log
import os
import time
def loadRes():
    outdict =  {}
    with open('save.txt') as f:
        lines = f.read().split("\n")
    f.close()
    for s in lines:
        l = s.replace(" ","").split(":")
        if l[1].isdigit():
            l[1] = int(l[1])
        outdict[l[0]] = l[1]
    return outdict

ocr = PaddleOCR(lang='en', show_log = False, use_angle_cls=True)
result = ocr.ocr("e_button-1692249791.492825.png",cls=True)[0]
result = sorted(result, key = lambda x: x[1][1], reverse = True)
print(result)
