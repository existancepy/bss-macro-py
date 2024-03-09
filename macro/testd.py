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


savedata = loadRes()
ww = savedata['ww']
wh = savedata['wh']
q_title = ""
giver = "polar"
ocr = [[[[[114.0, 72.0], [525.0, 74.0], [525.0, 104.0], [114.0, 102.0]], ('Polar Bear: Beetle Brew', 0.9887086749076843)], [[[67.0, 147.0], [571.0, 150.0], [571.0, 178.0], [67.0, 175.0]], ('Collect 140,000 Pollen from the Pineapple', 0.9992214441299438)], [[[215.0, 183.0], [425.0, 183.0], [425.0, 205.0], [215.0, 205.0]], ('Patch. 0/140.000', 0.9988036155700684)], [[[39.0, 253.0], [599.0, 253.0], [599.0, 273.0], [39.0, 273.0]], ('Collect 40.000 Pollen from the Dandelion Field', 0.9802424311637878)], [[[260.0, 283.0], [382.0, 283.0], [382.0, 308.0], [260.0, 308.0]], ('0/40,000', 0.9919106364250183)], [[[204.0, 349.0], [431.0, 354.0], [431.0, 380.0], [204.0, 374.0]], ('Defeat 8 Ladybugs', 0.998041033744812)], [[[294.0, 382.0], [346.0, 382.0], [346.0, 409.0], [294.0, 409.0]], ('0/8', 0.9965672492980957)], [[[183.0, 453.0], [453.0, 453.0], [453.0, 474.0], [183.0, 474.0]], ('Defeat 8 Rhino Beetles', 0.9814670085906982)], [[[294.0, 482.0], [346.0, 482.0], [346.0, 508.0], [294.0, 508.0]], ('0/8', 0.9982492327690125)], [[[113.0, 571.0], [527.0, 574.0], [527.0, 605.0], [113.0, 601.0]], ('Brown Bear: Mush-Clove', 0.9939067959785461)], [[[57.0, 651.0], [584.0, 653.0], [584.0, 674.0], [57.0, 673.0]], ('Collect 240.000.000 Pollen from the Clover', 0.9778481721878052)], [[[104.0, 684.0], [533.0, 684.0], [533.0, 708.0], [104.0, 708.0]], ('Field. Complete! Talk to Brown Bear', 0.9711253643035889)]]]
ocr = ocr[0]
lines = [x[1][0].lower() for x in ocr]
for i in lines:
    if giver in i:
        if ":" in i: i  = i.split(":")[1]
        q_title = i.replace(giver,"").replace("bear","")
        break
print(q_title)   
