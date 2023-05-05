import pyautogui as pag
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

def roblox():
    cmd = """
    osascript -e 'activate application "Roblox"' 
    """
    os.system(cmd)
    time.sleep(3)
    
savedat = loadRes()
ww = savedat['ww']
wh = savedat['wh']

roblox()
im = pag.screenshot(region=(0,0,ww,wh))
im.save("screen.png")
cmd = """
    osascript -e 'activate application "Terminal"' 
    """
os.system(cmd)
