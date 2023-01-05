import pyautogui as pag
import time
import os
import tkinter

def load():
    info = {}
    with open('settings.txt',"r") as f:
        lines = f.read().split("\n")
    f.close()
    for s in lines:
        if not s.startswith("=") and not s == "":
            l = s.replace(" ","").split(":")
            if l[1].isdigit():
                l[1] = int(l[1])
            elif l[1].lower() == "yes":
                l[1] = 1
            elif l[1].lower()  == "no":
                l[1] = 0
            info[l[0]] = l[1]
    return info

        


