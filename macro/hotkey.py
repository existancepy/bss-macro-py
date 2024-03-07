import Cocoa
import os

cmds = ["pkill -9 Python","pkill -9 Python3","pkill -9 Python3.9","pkill -9 Python3.8","pkill -9 Python3.7"]

def ctrlPressed():
    return Cocoa.NSEvent.modifierFlags() == Cocoa.NSControlKeyMask
        
while True:
        if ctrlPressed():
            print("hi")
            break
    
