import pyautogui as pag
import time
import os
import tkinter
import tkinter as tk
from tkinter import ttk
import move
import loadsettings
import reset
import backpack
import sys
import imagesearch
from webhook import webhook
print("Your python version is {}".format(sys.version_info[0]))
savedata = {}
started = 0
currentfield = ""
bpc = 0
def validateSettings():
    msg = ""
    files = os.listdir("./")
    validfield = [x.split("_")[1][:-3] for x in files if x.startswith("field_")]
    validgp = [x.split("_",1)[1][:-3] for x in files if x.startswith("gather_")]
    validsize = ["s","m","l"]
    s = loadsettings.load()
    if s['hive_number'] > 6 or s['hive_number'] < 0:
        msg += "\nInvalid hive number, it must be between 1-6 (inclusive)"
    if not s['gather_pattern'].lower() in validgp:
        msg += "\nInvalid gathering pattern, it has to be either {}".format(validgp)
    if not s['gather_size'].lower() in validsize:
        msg += "\nInvalid gather size, it has to be either {}".format(validsize)
    if not isinstance(s['gather_time'], int):
        msg += "\nInvalid gather time"
    if s['pack'] < 0 or s['pack'] > 100:
        msg += "\nInvalid pack, it must be between 1-100 (inclusive)"
    if not s['gather_field'] in validfield:
        msg += ("Invalid gather_field")
    if not s['gather_enable'] == 1 and not s['gather_enable'] == 0:
        msg += ("Invalid gather_enable. Use either 'yes' or 'no'")
    return msg


def loadSave():
    with open('save.txt') as f:
        lines = f.read().split("\n")
    f.close()
    for s in lines:
        l = s.replace(" ","").split(":")
        if l[1].isdigit():
            l[1] = int(l[1])
        savedata[l[0]] = l[1]

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

def savetimings(m):
    tempdict = loadtimings()
    tempdict[m] = time.time()
    templist = []
    
    for i in tempdict:
        templist.append("\n{}:{}".format(i,tempdict[i]))
    with open('timings.txt','w') as f:
        f.writelines(templist)
    f.close()
    
loadSave()
ww = savedata["ww"]
wh = savedata["wh"]

ms = pag.size()
mw = ms[0]
mh = ms[1]
def canon():
    #Move to canon:
    webhook("","Moving to canon","dark brown")
    move.hold("w",2)
    move.hold("d",0.9*(setdat["hive_number"])+1)
    pag.keyDown("d")
    time.sleep(0.5)
    move.press("space")
    time.sleep(0.2)
    st = time.perf_counter()
    r = ""
    pag.keyUp("d")
    while True:
        pag.keyDown("d")
        time.sleep(0.15)
        pag.keyUp("d")
        r = pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2))
        if r:
            webhook("","Canon found","dark brown")
            return
        if time.perf_counter()  - st > 10/28*setdat["walkspeed"]:
            webhook("","Cannon not found, resetting","dark brown")
            break
        
    reset.reset()   
    canon()
def convert():
    for _ in range(2):
        r = pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2))
        if r:
            webhook("","Starting convert","brown")
            move.press("e")
            st = time.perf_counter()
            while True:
                c = pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2))
            
                if not c:
                    webhook("","Convert done","brown")
                    time.sleep(3)
                    break
                if time.perf_counter()  - st > 600:
                    webhook("","Converting took too long, moving on","brown")
                    break
            
            break
        else:
            time.sleep(0.25)
    return
def walk_to_hive():
    
    webhook("","Going back to hive","dark brown")
    exec(open("walk_{}.py".format(setdat['gather_field'])).read())
    st = time.perf_counter()
    while True:
        pag.keyDown("a")
        time.sleep(0.15)
        pag.keyUp("a")
        r = pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2))
        if r:
            convert()
            break
        if time.perf_counter()  - st > 30/28*setdat["walkspeed"]:
            webhook("","Cant find hive, resetting","dark brown")
            reset.reset()
            break
    reset.reset()
def checkRespawn(m,t):
    timing = float(loadtimings()[m])
    respt = int(''.join([x for x in list(t) if x.isdigit()]))
    if t[-1] == 'h':
        respt = respt*60*60
    else:
        respt = respt*60
        
    if setdat['gifted_vicious_bee']:
        respt = respt/100*85
    if time.time() - timing > respt:
        return 1
    return 0

def savesettings(dictionary):
    templist = []
    for i in dictionary:
        templist.append("\n{}:{}".format(i,dictionary[i]))
    with open('settings.txt', "w") as f:
        f.writelines(templist)
    f.close()
def moblootPattern(f,s,r,t):
    if r == "l":
        for _ in range(t):
            move.press(",")
    elif r == "r":
        for _ in range(t):
            move.press(",")
    for i in range(2):
        move.hold("w", 0.72*f)
        move.hold("a", 0.1*s)
        move.hold("s", 0.72*f)
        move.hold("a", 0.1*s)
    for i in range(2):
        move.hold("w", 0.72*f)
        move.hold("d", 0.1*s)
        move.hold("s", 0.72*f)
        move.hold("d", 0.1*s)
    
def background():
    global bpc
    global currentfield
    xo = ww//2
    yo = wh//2
    if currentfield:
        bpc = backpack.bpc()
        if currentfield == "mushroom":
            if checkRespawn("ladybug_mushroom","5m"): savetimings("ladybug_mushroom")
        elif currentfield == "strawberry":
            if checkRespawn("ladybug_strawberry","5m"): savetimings("ladybug_strawberry")
        elif currentfield == "clover":
            if checkRespawn("ladybug_clover","5m"):
                savetimings("ladybug_clover")
                savetimings("rhinobeetle_clover")
        elif currentfield == "pumpkin" or currentfield == "cactus":
            if checkRespawn("werewolf","1h"):  savetimings("werewolf")
        elif currentfield == "pinetree":
            if checkRespawn("werewolf","1h"):  savetimings("werewolf")
            if checkRespawn("mantis_pinetree","20m"):  savetimings("mantis_pinetree")
        elif currentfield == "pineapple":
            if checkRespawn("mantis_pineapple","20m"):  savetimings("mantis_pineapple")
            if checkRespawn("rhinobeetle_pineapple","5m"):  savetimings("rhinobeetle_pineapple")
        elif currentfield == "spider":
            if checkRespawn("spider_spider","30m"):  savetimings("spider_spider")
        elif currentfield == "rose":
            if checkRespawn("scorpion_rose","20m"):  savetimings("scorpion_rose")
        elif currentfield == "blueflower":
            if checkRespawn("rhinobeetle_blueflower","5m"):  savetimings("rhinobeetle_blueflower")
        elif currentfield == "bamboo":
            if checkRespawn("rhinobeetle_bamboo","5m"):  savetimings("rhinobeetle_bamboo")


def killMob(field,mob):
    global currentfield
    webhook("","Traveling: {} ({})".format(mob.title(),field.title()),"dark brown")
    convert()
    canon()
    exec(open("field_{}.py".format(field)).read())
    xo = ww//2
    yo = wh//2
    start = time.time()
    move.apkey("space")
    webhook("","Looting: {} ({})".format(mob.title(), field.title()),"bright green")
    while True:
        moblootPattern(1.5,1.5,"none",2)
        if time.time() - start > 15:
            break
    currentfield = field.replace(" ","").lower()
    background()
    currentfield = ""
    reset.reset()
    convert()
    
    
'''
root = tkinter.Tk()
root.withdraw()
ww,wh = root.winfo_screenwidth(), root.winfo_screenheight()
print("{},{}".format(ww,wh))
root.destroy()

updateSave("ww",ww)
updateSave("wh",wh)
'''
            

        
def startLoop():
    global currentfield
    try:
        global started
        val = validateSettings()

        if val:
            pag.alert(text='Your settings are incorrect! Check the terminal to see what is wrong.', title='Invalid settings', button='OK')
            print(val)
            sys.exit()
            
        webhook("Macro started","","dark brown")
        setdat = loadsettings.load()
        cmd = """
        osascript -e 'activate application "Roblox"' 
        """
        os.system(cmd)
        reset.reset()
        convert()

        while True:
            global bpc
            global currentfield
            timings = loadtimings()
            if setdat['stump_snail'] and checkRespawn("stump_snail","96h"):
                canon()
                webhook("","Traveling: Stump snail (stump) ","brown")
                exec(open("field_stump.py").read())
                time.sleep(0.2)
                move.press("1")
                pag.click()
                webhook("","Starting stump snail","brown")
                while True:
                    time.sleep(10)
                    pag.click()
                    if pag.locateOnScreen("./images/keepold.png", confidence = 0.85):break
                webhook("","Stump snail killed, keeping amulet","bright green")
                savetimings("stump_snail")
                pag.moveTo(mw//2-30,mh//100*60)
                pag.click()
            if setdat['werewolf'] and checkRespawn("werewolf","1h"):
                killMob("pumpkin","werewolf")
            if setdat["ladybug"] and checkRespawn("ladybug_strawberry","5m"):
                killMob("strawberry","ladybug")
            if setdat["ladybug"] and checkRespawn("ladybug_clover","5m"):
                killMob("clover","ladybug")
            if setdat["ladybug"] and checkRespawn("ladybug_mushroom","5m"):
                killMob("mushroom","ladybug")
            if setdat["rhinobeetle"] and checkRespawn("rhinobeetle_blueflower","5m"):
                killMob("blue flower","rhino beetle")
            if setdat["rhinobeetle"] and checkRespawn("rhinobeetle_clover","5m"):
                killMob("clover","rhino beetle")
            if setdat["rhinobeetle"] and checkRespawn("rhinobeetle_bamboo","5m"):
                killMob("bamboo","rhino beetle")
            if setdat["rhinobeetle"] and checkRespawn("rhinobeetle_pineapple","5m"):
                killMob("pineapple","rhino beetle")
            if setdat["mantis"] and checkRespawn("mantis_pinetree","20m"):
                killMob("pine tree","mantis")
            if setdat["mantis"] and checkRespawn("mantis_pineapple","20m"):
                killMob("pineapple","mantis")
            if setdat["scorpion"] and checkRespawn("scorpion_rose","20m"):
                killMob("rose","scorpion")
            if setdat["spider"] and checkRespawn("spider_spider","30m"):
                killMob("spider","spider")

            if setdat['gather_enable']:
                canon()
                webhook("","Traveling: {}".format(setdat['gather_field']),"dark brown")
                exec(open("field_{}.py".format(setdat['gather_field'])).read())
                currentfield = setdat['gather_field'].replace(" ","").lower()
                time.sleep(0.2)
                if setdat["before_gather_turn"] == "left":
                    for _ in range(setdat["turn_times"]):
                        move.press(",")
                elif setdat["before_gather_turn"] == "right":
                    for _ in range(setdat["turn_times"]):
                        move.press(".")
                time.sleep(0.2)
                move.press("1")
                pag.click()
                gp = setdat["gather_pattern"].lower()
                webhook("Gathering: {}".format(setdat['gather_field']),"Limit: {}.00 - {} - Backpack: {}%".format(setdat["gather_time"],setdat["gather_pattern"],setdat["pack"]),"light green")
                move.apkey("space")
                time.sleep(0.2)
                timestart = time.perf_counter()
                while True:
                    background()
                    pag.mouseDown()
                    exec(open("gather_{}.py".format(gp)).read())
                    pag.mouseUp()
                    timespent = (time.perf_counter() - timestart)/60
                    if bpc > setdat["pack"]:
                        webhook("Gathering: ended","Time: {:.2f} - Backpack - Return: {}".format(timespent, setdat["return_to_hive"]),"light green")
                        break
                    if timespent > setdat["gather_time"]:
                        webhook("Gathering: ended","Time: {:.2f} - Time Limit - Return: {}".format(timespent, setdat["return_to_hive"]),"light green")
                        break
                currentfield = ""
                if setdat["before_gather_turn"] == "left":
                    for _ in range(setdat["turn_times"]):
                        move.press(".")
                elif setdat["before_gather_turn"] == "right":
                    for _ in range(setdat["turn_times"]):
                        move.press(",")
                        
                if setdat['return_to_hive'] == "walk":
                    walk_to_hive()
                elif setdat['return_to_hive'] == "reset":
                    reset.reset()
                    convert()
                elif setdat['return_to_hive'] == "whirligig":
                    reject = 0
                    webhook("","Activating whirligig","dark brown")
                    if setdat['whirligig_slot'] == "none":
                        webhook("Notice","Whirligig option selected but no whirligig slot given, walking back","red")
                        walk_to_hive()
                    else:
                        move.press(str(setdat['whirligig_slot']))
                        time.sleep(1)
                        r = pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2))
                        if not r or reject:
                            webhook("Notice","Whirligig failed to activate, walking back","red")
                            walk_to_hive()
                        else:
                            convert()
                            reset.reset()

                            
    except KeyboardInterrupt:
        webhook("Macro stopped","","dark brown")
        started = 0
                
setdat = loadsettings.load()
started = 0
root = tk.Tk()
root.geometry('700x400')
#s = ttk.Style()
#s.theme_use("alt")
notebook = ttk.Notebook(root)
notebook.pack(expand=True, pady = 5)
root.title("exih_macro")
# create frames
frame1 = ttk.Frame(notebook, width=700, height=400)
frame2 = ttk.Frame(notebook, width=700, height=400)
frame3 = ttk.Frame(notebook, width=700, height=400)
frame4 = ttk.Frame(notebook, width=700, height=400)

frame1.pack(fill='both', expand=True)
frame2.pack(fill='both', expand=True)
frame3.pack(fill='both', expand=True)
frame4 = ttk.Frame(notebook, width=700, height=400)


#get variables

notebook.add(frame1, text='Gather')
notebook.add(frame2, text='Bug run')
notebook.add(frame4, text='Collect')
notebook.add(frame3, text='Calibrate')

gather_enable = tk.IntVar(value=setdat["gather_enable"])
gather_field = tk.StringVar(root)
gather_field.set(setdat["gather_field"].title())
return_to_hive = tk.StringVar(root)
return_to_hive.set(setdat["return_to_hive"].title())
gather_pattern = tk.StringVar(root)
gather_pattern.set(setdat["gather_pattern"])
gather_size = tk.StringVar(root)
gather_size.set(setdat["gather_size"].title())
gather_width = tk.IntVar(value=setdat["gather_width"])
gather_time = setdat["gather_time"]
pack =setdat["pack"]
before_gather_turn = tk.StringVar(root)
before_gather_turn.set(setdat["before_gather_turn"])
turn_times = tk.IntVar(value=setdat["turn_times"])
whirligig_slot = tk.StringVar(root)
whirligig_slot.set(setdat["whirligig_slot"])
stump_snail = tk.IntVar(value=setdat["stump_snail"])
ladybug = tk.IntVar(value=setdat["ladybug"])
rhinobeetle = tk.IntVar(value=setdat["rhinobeetle"])
werewolf = tk.IntVar(value=setdat["werewolf"])
scorpion = tk.IntVar(value=setdat["scorpion"])
spider = tk.IntVar(value=setdat["spider"])
mantis = tk.IntVar(value=setdat["mantis"])
gifted_vicious_bee = tk.IntVar(value=setdat["gifted_vicious_bee"])
enable_discord_webhook = tk.IntVar(value=setdat["enable_discord_webhook"])
discord_webhook_url= setdat["discord_webhook_url"]
walkspeed = setdat["walkspeed"]
hive_number = tk.IntVar(value=setdat["hive_number"])

def startGo():
    global started
    global setdat
    if started: return
    started = 1
    setdict = {
        "hive_number": hive_number.get(),
        "walkspeed": speedtextbox.get(1.0,"end").replace("\n",""),
        "gifted_vicious_bee": gifted_vicious_bee.get(),
        "enable_discord_webhook": enable_discord_webhook.get(),
        "discord_webhook_url": urltextbox.get(1.0,"end").replace("\n",""),
        
        "gather_enable": gather_enable.get(),
        "gather_field": gather_field.get(),
        "gather_pattern": gather_pattern.get(),
        "gather_size": gather_size.get(),
        "gather_width": gather_width.get(),
        "gather_time": timetextbox.get(1.0,"end").replace("\n",""),
        "pack": packtextbox.get(1.0,"end").replace("\n",""),
        "before_gather_turn": before_gather_turn.get(),
        "turn_times": turn_times.get(),
        "return_to_hive": return_to_hive.get(),
        "whirligig_slot": whirligig_slot.get(),
        
        "stump_snail": stump_snail.get(),
        "ladybug": ladybug.get(),
        "rhinobeetle": rhinobeetle.get(),
        "spider": spider.get(),
        "scorpion": scorpion.get(),
        "werewolf": werewolf.get(),
        "mantis": mantis.get(),

        }
    savesettings(setdict)
    setdat = loadsettings.load()
    startLoop()
def stopScript():
    raise KeyboardInterrupt
#Tab 1
tkinter.Checkbutton(frame1, text="Enable Gathering", variable=gather_enable, bg = "#E4E4E4").place(x=0, y = 15)
dropField = tkinter.OptionMenu(frame1, gather_field, *[x.split("_")[1][:-3].title() for x in os.listdir("./") if x.startswith("field_")] )
dropField.place(width=110,x = 120, y = 50)
tkinter.Label(frame1, text = "Gathering Field", bg = "#E4E4E4").place(x = 0, y = 50)

tkinter.Label(frame1, text = "Gathering Pattern", bg = "#E4E4E4").place(x = 0, y = 85)
dropField = tkinter.OptionMenu(frame1, gather_pattern, *[x.split("_",1)[1][:-3] for x in os.listdir("./") if x.startswith("gather_")])
dropField.place(width=110,x = 120, y = 85)
tkinter.Label(frame1, text = "Size", bg = "#E4E4E4").place(x = 250, y = 85)
dropField = tkinter.OptionMenu(frame1, gather_size, *["S","M","L"] )
dropField.place(width=50,x = 290, y = 85)
tkinter.Label(frame1, text = "Width", bg = "#E4E4E4").place(x = 360, y = 85)
dropField = tkinter.OptionMenu(frame1, gather_width, *[(x+1) for x in range(10)] )
dropField.place(width=50,x = 410, y = 85)

tkinter.Label(frame1, text = "Before Gathering, Rotate Camera", bg = "#E4E4E4").place(x = 0, y = 120)
dropField = tkinter.OptionMenu(frame1, before_gather_turn, *["None","Left","Right"] )
dropField.place(width=60,x = 210, y = 120)
dropField = tkinter.OptionMenu(frame1, turn_times, *[(x+1) for x in range(4)] )
dropField.place(width=50,x = 275, y = 120)

tkinter.Label(frame1, text = "Gather Until:", bg = "#E4E4E4").place(x = 0, y = 155)
tkinter.Label(frame1, text = "Mins", bg = "#E4E4E4").place(x = 90, y = 155)
timetextbox = tkinter.Text(frame1, width = 4, height = 1)
timetextbox.insert("end",gather_time)
timetextbox.place(x = 130, y=158)
tkinter.Label(frame1, text = "Backpack%", bg = "#E4E4E4").place(x = 175, y = 155)
packtextbox = tkinter.Text(frame1, width = 4, height = 1)
packtextbox.insert("end",pack)
packtextbox.place(x = 260, y=158)
tkinter.Label(frame1, text = "To Hive By", bg = "#E4E4E4").place(x = 305, y = 155)
dropConvert = tkinter.OptionMenu(frame1 , return_to_hive, *["Walk","Reset","Whirligig"])
dropConvert.place(width=70,x = 380, y = 155)
tkinter.Label(frame1, text = "Whirligig Slot", bg = "#E4E4E4").place(x = 460, y = 155)
dropConvert = tkinter.OptionMenu(frame1 , whirligig_slot, *[1,2,3,4,5,6,7,"none"])
dropConvert.place(width=70,x = 550, y = 155)

#Tab 2
tkinter.Checkbutton(frame2, text="Apply gifted vicious bee hive bonus", variable=gifted_vicious_bee, bg = "#E4E4E4").place(x=0, y = 15)
tkinter.Checkbutton(frame2, text="Stump Snail", variable=stump_snail, bg = "#E4E4E4").place(x=0, y = 50)
tkinter.Checkbutton(frame2, text="Ladybug", variable=ladybug, bg = "#E4E4E4").place(x=0, y = 85)
tkinter.Checkbutton(frame2, text="Rhino Beetle", variable=rhinobeetle, bg = "#E4E4E4").place(x=80, y = 85)
tkinter.Checkbutton(frame2, text="Scorpion", variable=scorpion, bg = "#E4E4E4").place(x=190, y = 85)
tkinter.Checkbutton(frame2, text="Mantis", variable=mantis, bg = "#E4E4E4").place(x=275, y = 85)
tkinter.Checkbutton(frame2, text="Spider", variable=spider, bg = "#E4E4E4").place(x=345, y = 85)
tkinter.Checkbutton(frame2, text="Werewolf", variable=werewolf, bg = "#E4E4E4").place(x=415, y = 85)

#Tab 3


#Tab 4
tkinter.Label(frame3, text = "Hive Slot (6-5-4-3-2-1)", bg = "#E4E4E4").place(x = 0, y = 15)
dropField = tkinter.OptionMenu(frame3, hive_number, *[x+1 for x in range(6)] )
dropField.place(width=60,x = 160, y = 15)
tkinter.Label(frame3, text = "Move Speed (without haste)", bg = "#E4E4E4").place(x = 0, y = 40)
speedtextbox = tkinter.Text(frame3, width = 4, height = 1)
speedtextbox.insert("end",walkspeed)
speedtextbox.place(x = 185, y=42)
tkinter.Checkbutton(frame3, text="Enable Discord Webhook", variable=enable_discord_webhook, bg = "#E4E4E4").place(x=0, y = 65)
tkinter.Label(frame3, text = "Discord Webhook Link", bg = "#E4E4E4").place(x = 200, y = 65)
urltextbox = tkinter.Text(frame3, width = 24, height = 1, xscrollcommand = True)
urltextbox.insert("end",discord_webhook_url)
urltextbox.place(x = 350, y=67)



#Root
tkinter.Button(root, text = "Start",command = startGo, height = 2, width = 7 ).place(x=10,y=350)
root.mainloop()


        




