import loadsettings
from webhook import webhook
from html2image import Html2Image
from datetime import datetime
import time
import os
import math
import ast
from logpy import log
import subprocess
import pyautogui as pag
import time
hti = Html2Image()

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

def millify(n):
    if not n: return "0"
    millnames = ['',' K',' M',' B',' T', 'Qd']
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.2f}{}'.format(n / 10**(3 * millidx), millnames[millidx])
def minAndSecs(m):
    secs = round((float(m) - int(m))*60)
    return f"{int(m)}m {secs}s"

def hourlyReport(hourly=1):
    savedata = loadRes()
    ww = savedata['ww']
    wh = savedata['wh']
    ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
    xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
    ylm = loadsettings.load('multipliers.txt')['y_length_multiplier']
    xlm = loadsettings.load('multipliers.txt')['x_length_multiplier']
    with open('honey_history.txt','r') as f:
        honeyHist = ast.literal_eval(f.read())
    f.close()
    
    setdat = loadsettings.load()
    log(honeyHist)
    #remove values less than 1000
    for i, e in enumerate(honeyHist[:]):
        if len(str(e)) <= 4:
            honeyHist.pop(i)
    #remove values less than the previous one
    honeyHist = honeyHist[1:]
    counter = 1
    while counter < len(honeyHist):
        if honeyHist[counter] < honeyHist[counter-1]:
            honeyHist.pop(counter)
        else:
            counter += 1
    if hourly == 0:
        setdat['prev_honey'] = honeyHist[-1]
    log('prev honey: {}'.format(setdat['prev_honey']))
    log(honeyHist)
    currHoney = honeyHist[-1]
    session_honey = currHoney - setdat['start_honey']
    hourly_honey = currHoney - setdat['prev_honey']
    if hourly:
        loadsettings.save('prev_honey',currHoney)
        timehour = int(datetime.now().hour) - 1
    else:
        timehour = int(datetime.now().hour)
        
    stime = time.time() - setdat['start_time']
    day = stime // (24 * 3600)
    stime = stime % (24 * 3600)
    hour = stime // 3600
    stime %= 3600
    minutes = stime // 60
    stime %= 60
    seconds = round(stime)
    session_time = "{}d {}h {}m".format(round(day),round(hour),round(minutes))
    yvals = []
    for i in range(len(honeyHist)):
        if i != 0:
            hf, hb = honeyHist[i], honeyHist[i-1]
            yvals.append(int(hf) - int(hb))
    #yvals = [1,2,3,4,5,6,7,8]
    xvals = [x+1 for x in range(len(yvals))]
    rootDir = os.path.dirname(os.path.abspath(__file__)) + "/hourlyReport"
    with open("./hourlyReport/index.html", "r") as f:
        data = f.read().split("\n")
        data.insert(0,"")
    f.close()
    
    stats = loadsettings.load("stats.txt")
    rejoin_time = minAndSecs(stats["rejoin_time"])
    gather_time = minAndSecs(sum(stats["gather_time"]))
    convert_time = minAndSecs(sum(stats["convert_time"]))
    bug_time = minAndSecs(stats["bug_time"])
    objective_time = minAndSecs(stats["objective_time"])

    gather_avg = minAndSecs(sum(stats["gather_time"])/len(stats["gather_time"]))
    convert_avg = minAndSecs(sum(stats["convert_time"])/len(stats["convert_time"]))

    taskTimes = [stats["rejoin_time"],sum(stats["gather_time"]),stats["bug_time"],sum(stats["convert_time"]),stats["objective_time"]]
    print(data)
    data[30] = f"Rejoining:\t{rejoin_time}"
    data[34] = f"Gathering:\t{gather_time}"
    data[38] = f"Bug Runs:\t{bug_time}"
    data[42] = f"Converting:\t{convert_time}"
    data[46] = f"Collecting Objectives:\t{objective_time}"
    data[55] = f"{rootDir}/assets/buffs.png"
    data[65] = session_time
    data[70] = millify(currHoney)
    data[75] = millify(session_honey)
    data[80] = str(stats["vic_kills"])
    data[92] = millify(hourly_honey)
    data[98] = gather_avg
    data[104] = convert_avg
    data[109] = str(stats["bug_kills"])
    data[132] = f"const time = {xvals}"
    data[133] = f"const honey = {yvals}"
    data[197] = f'const times ='
    

    print(data[1:][89])
    with open("./hourlyReport/index.html","w") as f:
        f.write('\n'.join(data[1:]))
    f.close()
    
    try:
        UI = 25
        info  = str(subprocess.check_output("system_profiler SPDisplaysDataType", shell=True)).lower()
        if "retina" in info or "m1" in info or "m2" in info:
            UI*=2
    except FileNotFoundError:
        UI = 0
    buffim = pag.screenshot(region = (0,wh/(30*ysm)+UI,ww/2,wh/(16*ylm)))
    buffim.save("./hourlyReport/assets/buffs.png")

    hti.screenshot(html_file='./hourlyReport/index.html', save_as='hourlyReport-resized.png')
    webhook("**Hourly Report**","","light blue",0,1)
'''
import pyscreeze
import pyscreezeCustom
import numpy as np
savedata = loadRes()
ww = savedata['ww']
wh = savedata['wh']
cmd = """
        osascript -e 'activate application "Roblox"' 
    """
os.system(cmd)
time.sleep(1)
while True:
    area = pyscreeze.screenshot(region = (0,wh/2,ww,wh/2))
    area.save("a.png")
    res = list(pyscreezeCustom._locateAll_python("./images/general/grassD.png", area, limit=1, var = 10))
    if res:
        print("yes")
    else:
        print("no")
tar = (89, 135, 59)
screen = np.array(area)
h,w = screen.shape[:2]
print(w,h)
print(screen[829,300])
detected = False
for x in range(w):
    for y in range(h):
        pixel = list(screen[y,x])
        for i in range(3):
            if not (tar[i]-5 <= pixel[i] <= tar[i]+5):
                break
        else:
            print(f"detected: {x},{y}")
            detected = True
            break
    if detected: break
'''
path = os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + os.sep + os.pardir) 
path = os.path.join(path, "exports")
print(path)
