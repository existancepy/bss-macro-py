import pyautogui as pag
import time
import os
import loadsettings
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

def roblox():
    cmd = """
    osascript -e 'activate application "Roblox"' 
    """
    os.system(cmd)
    time.sleep(3)
    
savedat = loadRes()
ww = savedat['ww']
wh = savedat['wh']
ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
ylm = loadsettings.load('multipliers.txt')['y_length_multiplier']
xlm = loadsettings.load('multipliers.txt')['x_length_multiplier']
roblox()
im = pag.screenshot(region=(0,0,ww,wh))
im.save("screen.png")
cap = pag.screenshot(region=(ww//(2.65*xsm),wh//(20*ysm),ww//(21*xlm),wh//(17*ylm)))
cap.save('e_symbol.png')
cmd = """
    osascript -e 'activate application "Terminal"' 
    """
os.system(cmd)
print("Done! The following 2 images can be found in your bss-macro-py-main folder: \nscreen.png\ne_symbol.png")
