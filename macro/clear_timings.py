
import pyautogui as pag
import time
import os
import tkinter
import loadsettings
import move
ws = loadsettings.load()["walkspeed"]

def loadtimings():
    tempdict = {}
    with open('timings.txt') as f:
        lines = f.read().split("\n")
    f.close()
    lines = [x for x in lines if x]
    for s in lines:
        l = s.replace(" ","").split(":")
        if l[1].isdigit():
            l[1] = int(l[1])
        tempdict[l[0]] = l[1]
    return tempdict

def savetimings():
    tempdict = loadtimings()
    templist = []
    for i in tempdict:
        templist.append("\n{}:0".format(i))
    with open('timings.txt','w') as f:
        f.writelines(templist)
    f.close()
savetimings()
