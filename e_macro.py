import pyautogui as pag
import time
import os
import tkinter
import move
import loadsettings
import pinetree
import reset
import gather_elol

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


def canon():
    #Move to canon:
    move.hold("w",2)
    move.hold("d",0.9*(setdat["hive_number"])+1)
    pag.keyDown("d")
    time.sleep(0.5)
    pag.press("space")
    st = time.perf_counter()
    r = ""
    time.sleep(0.1)
    pag.keyUp("d")
    while True:
        pag.keyDown("d")
        time.sleep(0.15)
        pag.keyUp("d")
        r = pag.locateOnScreen("./images/e_button.png",region=(0,0,ww,wh//2))
        if r:
            print("canon found")
            move.press("e")
            return
        if time.perf_counter()  - st > 10/28*setdat["walkspeed"]:
            print('no cannon')
            break
        
    reset.reset()   
    canon()
def convert():
    for _ in range(2):
        r = pag.locateOnScreen("./images/e_button.png",region=(0,0,ww,wh//2))
        if r:
            move.press("e")
            st = time.perf_counter()
            while True:
                c = pag.locateOnScreen("./images/e_button.png",region=(0,0,ww,wh//2))
                if not c:
                    print("convert done")
                    time.sleep(3)
                    break
                if time.perf_counter()  - st > 600:
                    print("converting took too long, moving on")
                    break
            
            break
        else:
            time.sleep(0.25)
    return
'''
root = tkinter.Tk()
root.withdraw()
ww,wh = root.winfo_screenwidth(), root.winfo_screenheight()
print("{},{}".format(ww,wh))
root.destroy()

updateSave("ww",ww)
updateSave("wh",wh)
'''


cmd = """
osascript -e 'activate application "Roblox"' 
"""
os.system(cmd)

setdat = loadsettings.load()
reset.reset()
convert()
canon()
pinetree.go()
move.press(".")
move.press(".")
move.press("1")
for _ in range(10):
    pag.mouseDown()
    gather_elol.gather()
    pag.mouseUp()


    

    




