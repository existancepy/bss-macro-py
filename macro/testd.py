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
import traceback
import cv2
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

def addStat(a,b):
    pass

def usablePlanterName(planter):
    planter = planter.lower().replace(" ","")
    if "plenty" in planter:
        return "plenty"
    return planter

def displayPlanterName(planter):
    if planter == "redclay":
        return "Red Clay Planter"
    elif planter == "blueclay":
        return "Blue Clay Planter"
    elif planter  == "heattreated":
        return "Heat-Treated Planter"
    elif planter == "plenty":
        return "The Planter of Plenty"
    return "{} Planter".format(planter.title())

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
    setdat = loadsettings.load()
    savedata = loadRes()
    ww = savedata['ww']
    wh = savedata['wh']
    ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
    xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
    ylm = loadsettings.load('multipliers.txt')['y_length_multiplier']
    xlm = loadsettings.load('multipliers.txt')['x_length_multiplier']
    planterset = loadsettings.planterLoad()
        
    try:
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
                #check if upwards spike
                if counter > 1 and len(str(honeyHist[counter-2])) == len(str(honeyHist[counter])) and len(str(honeyHist[counter-1])) != len(str(honeyHist[counter])):
                    honeyHist.pop(counter-1)
                else:
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
            addStat("hourly_honey",hourly_honey)
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
            data1 = f.read()
        f.close()
        with open("./hourlyReport/index2.html", "r") as f:
            data2 = f.read()
        f.close()
        
        stats = loadsettings.load("./dataFiles/stats.txt")
        rejoin_time = minAndSecs(stats["rejoin_time"])
        gather_time = minAndSecs(sum(stats["gather_time"]))
        convert_time = minAndSecs(sum(stats["convert_time"]))
        bug_time = minAndSecs(stats["bug_time"])
        objective_time = minAndSecs(stats["objective_time"])

        gather_avg = minAndSecs(sum(stats["gather_time"])/len(stats["gather_time"]))
        convert_avg = minAndSecs(sum(stats["convert_time"])/len(stats["convert_time"]))
        
        hourly_honeys = stats["hourly_honey"]
        
        if planterset["enable_planters"]:
            showPlanters = "block"
        else:
            showPlanters = "none"

        planterImgDict = {
            "paper:":"https://cdn.discordapp.com/attachments/670121853238378526/1222887070092230846/paperplanter.png?ex=6617d955&is=66056455&hm=d24f2b0302fdbdd141c0e661f6d72c24e5113e2960986a43a472fd1b7b3dcaed&",
            "ticket":"https://cdn.discordapp.com/attachments/670121853238378526/1222887047975407747/ticketplanter.png?ex=6617d950&is=66056450&hm=c6f535bcd9b85a60a0fdd94252214a19c0b55e82ca8f77a52e58fcb931efa76e&",
            "plastic":"https://cdn.discordapp.com/attachments/670121853238378526/1222887047337873468/plasticplanter.png?ex=6617d950&is=66056450&hm=199314f9d587b85dd67e5bbddbcfd36f45b5cda2fb6040d0fa56790000f9c940&",
            "candy":"https://cdn.discordapp.com/attachments/670121853238378526/1222887069156642986/candyplanter.png?ex=6617d955&is=66056455&hm=9f0d535947b6b7d266274652f691f35b387796323f7ac0ae408046c0ea43ee7a&",
            "blueclay":"https://cdn.discordapp.com/attachments/670121853238378526/1222887928863264841/blueclayplanter.png?ex=6617da22&is=66056522&hm=12d1ae2c3c111fe6fb9185e86ee084603003a9c970dd1572170ba4631fff909d&",
            "redclay":"https://cdn.discordapp.com/attachments/670121853238378526/1222887047547584672/redclayplanter.png?ex=6617d950&is=66056450&hm=e0103144f651596892a875546ddf34c0697b11105d42924d87ec17afced198be&",
            "tacky":"https://cdn.discordapp.com/attachments/670121853238378526/1222887047765950474/tackyplanter.png?ex=6617d950&is=66056450&hm=4d03eb1e0816d2e9a87018d4b9fdecb7f71e50c9c3db57925785f0217b6a04b7&",
            "pesticide":"https://cdn.discordapp.com/attachments/670121853238378526/1222887046704533675/pesticideplanter.png?ex=6617d950&is=66056450&hm=00c9dfd020c75e7d09d01260cd9a892f6d704921c02e2191b9c9d616005ce7f3&",
            "heattreated":"https://cdn.discordapp.com/attachments/670121853238378526/1222887069635055646/heattreatedplanter.png?ex=6617d955&is=66056455&hm=bb76a1182da69001febebd6d9626a109126e58bcc9fe94b1be2105b0841ef1e8&",
            "hydroponic":"https://cdn.discordapp.com/attachments/670121853238378526/1222887069869674586/hydroponicplanter.png?ex=6617d955&is=66056455&hm=cd490ec2b73c79e0d847b71e4f997c1fecefbfa710e543fa096ea2224d13740e&",
            "petal":"https://cdn.discordapp.com/attachments/670121853238378526/1222887046897467472/petalplanter.png?ex=6617d950&is=66056450&hm=c8634575e49d7c65180e358c9c1b330ceb018c7335be7502f5a8163f44f0d850&",
            "plenty":"https://cdn.discordapp.com/attachments/670121853238378526/1222887047120027648/planterofplenty.png?ex=6617d950&is=66056450&hm=04c55110a006c6aa9b70264b1a2cca4b16522c47ebe2bedc2f14aebcbd2da275&",
            "festive":"https://cdn.discordapp.com/attachments/670121853238378526/1222887069442113536/festiveplanter.png?ex=6617d955&is=66056455&hm=f6931f2ab3ab4e529e294f57fa695f680adead513d3e73e65a88f7fc461f7278&"

        }
        replaceDict = {
            "-rejointime": f"Rejoining:\t{rejoin_time}",
            "-gathertime": f"Gathering:\t{gather_time}",
            "-bugruntime": f"Bug Runs:\t{bug_time}",
            "-converttime": f"Converting:\t{convert_time}",
            "-objectivetime": f"Objectives:\t{objective_time}",
            "-buffpath": f"{rootDir}/assets/buffs.png",
            "-sessiontime": session_time,
            "-currenthoney": millify(currHoney),
            "-sessionhoney": millify(session_honey),
            "-vickills": str(stats["vic_kills"]),
            "-quests": str(stats["quests"]),
            "-hourlyhoney": millify(hourly_honey),
            "-gatheravg": gather_avg,
            "-convertavg": convert_avg,
            "-bugkills": str(stats["bug_kills"]),
            "const time = []": f"const time = {xvals}",
            "const honey = []": f"const honey = {yvals}",
            "const times = []":  f'const times = [{stats["rejoin_time"]},{sum(stats["gather_time"])},{stats["bug_time"]},{sum(stats["convert_time"])},{stats["objective_time"]}]',
            "const hours = []": f"const hours = {[i+1 for i in range(len(hourly_honeys))]}",
            "const hourlyHoney = []": f"const hourlyHoney = {hourly_honeys}",
            "-showplanters": showPlanters,
            "-showplanter1": "none",
            "-showplanter2": "none",
            "-showplanter3": "none"
        }

        if planterset["enable_planters"]:
            with open("planterdata.txt","r") as f:
                lines = f.read().split("\n")
            f.close()
            occupiedStuff = ast.literal_eval(lines[0])
            
            with open("plantertimings.txt","r") as f:
                lines = f.read().split("\n")
            f.close()
            planterTimes = {}
            for i in lines:
                if ":" in i:
                    p,t = i.split(":")
                    planterTimes[p] = float(t)
            planters = [usablePlanterName(x[0]) for x in occupiedStuff]

            for i,currPlanter in enumerate(planters):
                replaceDict[f"-showplanter{i+1}"] =  "flex"
                replaceDict[f"-plantername{i+1}"] =  displayPlanterName(currPlanter)
                replaceDict[f"-planterimg{i+1}"] = planterImgDict[currPlanter]
                
                currField = occupiedStuff[i][1]
                if planterset["enable_planters"] == 1:
                    if str(planterset['harvest']) == "full":
                        growTime = planterInfo[currPlanter]['grow_time']
                        if currField in planterInfo[currPlanter]['grow_fields']:
                            growTime /= planterInfo[currPlanter]['grow_time_bonus']
                    elif str(planterset['harvest']) == "auto":
                        growTime = 1
                    else:
                        growTime = planterset['harvest']
                else:
                    growTime = planterset['manual_harvest']

                timeRemain = growTime*60*60 - (time.time() - planterTimes[currPlanter])
                if timeRemain > 0:
                    mins, _ = divmod(timeRemain, 60)
                    hours, mins = divmod(mins, 60)
                    replaceDict[f"-plantertime{i+1}"] =  f"{round(hours)}h {round(mins)}m"
                else:
                    replaceDict[f"-plantertime{i+1}"] =  "Ready"
                    
        for k, v in replaceDict.items():
            data1 = data1.replace(k,v)
            data2 = data2.replace(k,v)
        log(data1)
        log(data2)

        if setdat["new_ui"]:
            UI = wh/(16*ysm)
        else:
            UI = wh/(30*ysm)
        buffim = pag.screenshot(region = (0,UI,ww/2.1,wh/(16*ylm)))
        buffim.save("./hourlyReport/assets/buffs.png")

        hti.screenshot(html_str=data1, save_as='hourlyReport1.png')
        hti.screenshot(html_str=data2, save_as='hourlyReport2.png')
        img1 = cv2.imread('hourlyReport1.png')
        height, width, _ = img1.shape
        img2 = cv2.imread('hourlyReport2.png')

        img1 = img1[0:round(height*0.9), 0:width]
        img2 = img2[0:round(height/2), 0:width]
        imgOut = cv2.vconcat([img1, img2]) 
          
        cv2.imwrite("hourlyReport-resized.png", imgOut) 
        webhook("**Hourly Report**","","light blue",0,1)
    except Exception:
        
        print(traceback.format_exc())
        log(traceback.format_exc())
        webhook("","Hourly Report has an error that has been caught. The error can be found in macroLogs.log","red")

hourlyReport()
        
