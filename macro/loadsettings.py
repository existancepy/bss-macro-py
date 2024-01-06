import pyautogui as pag
import time
import os
import tkinter
import ast

def load(filename = "settings.txt"):
    info = {}
    with open(filename,"r") as f:
        lines = f.read().split("\n")
    f.close()
    print(lines)
    for s in lines:
        if not s.startswith("=") and not s == "":
            l = s.strip().split(":",1)
            if l[1].isdigit():
                l[1] = int(l[1])
            elif l[1].replace(".","").isdigit() and len(l[1].split(".")) == 2:
                l[1] = float(l[1])
            elif l[1].lower() == "yes":
                l[1] = 1
            elif l[1].lower()  == "no":
                l[1] = 0
            elif l[1].lower().startswith("http"):
                pass
            elif l[0] == "discord_bot_token":
                pass
            else:
                if l[1].startswith("[") and "]" in l[1]:
                    l[1]  = ast.literal_eval(l[1])
                    if str(l[1][0]).isdigit():
                        try:
                            newList = [int(x) for x in l[1]]
                            l[1] = newList
                        except:
                            pass
                    try:
                        newList = [x.lower() for x in l[1]]
                        l[1] = newList
                    except:
                        pass
                else:
                    l[1] = l[1].lower()
                
            info[l[0]] = l[1]
    return info

def planterLoad():
    info = {}
    with open('plantersettings.txt',"r") as f:
        lines = f.read().split("\n")
    f.close()
    for s in lines:
        if not s.startswith("=") and not s == "":
            l = s.strip().split(":",1)
            if l[1].isdigit():
                l[1] = int(l[1])
            elif l[1].replace(".","").isdigit():
                l[1] = float(l[1])
            elif isinstance(l[1], list):
                l[1]  = list(l[1])[0]
            else:
                try:
                    l[1] = ast.literal_eval(l[1])
                except:
                    l[1] = l[1].lower()
            info[l[0]] = l[1]
    return info
    
def save(setting,value,filename = "settings.txt"):
    info = load(filename)
    info[setting] = value
    out = ''
    for i in info:
        out += '\n{}:{}'.format(i,info[i])
    with open(filename,"w") as f:
        lines = f.write(out)
    f.close()



planterData = {
    "paper": {
        "grow_time":1,
        "grow_time_bonus":1,
        "grow_fields":[],
        "nectar_mult": [0.75,0.75,0.75,0.75,0.75]
    
        },

    "ticket": {
        "grow_time":2,
        "grow_time_bonus":1,
        "grow_fields":[],
        "nectar_mult": [2,2,2,2,2]
    
        },
    "festive": {
        "grow_time":4,
        "grow_time_bonus":1,
        "grow_fields":[],
        "nectar_mult": [3,3,3,3,3]
    
        },
    "plastic": {
        "grow_time":2,
        "grow_time_bonus":1,
        "grow_fields":[],
        "nectar_mult": [1,1,1,1,1]
    
        },
    "candy": {
        "grow_time":4,
        "grow_time_bonus":1.25,
        "grow_fields":['strawberry','pineapple','coconut'],
        "nectar_mult": [1,1,1,1.2,1] #Refreshing, Comforting, Satisfying, Motivating, Invigorating
    
        },
    "redclay": {
        "grow_time":6,
        "grow_time_bonus":1.25,
        "grow_fields":['sunflower','dandelion','mushroom','clover','strawberry','pineapple','stump','pumpkin','cactus','rose','mountain top','coconut','pepper'],
        "nectar_mult": [1,1,1.2,1,1.2] #Refreshing, Comforting, Satisfying, Motivating, Invigorating
    
        },
    "blueclay": {
        "grow_time":6,
        "grow_time_bonus":1.25,
        "grow_fields":['sunflower','dandelion','blue flower','clover','bamboo','pineapple','stump','pumpkin','cactus','pine tree','mountain top','coconut'],
        "nectar_mult": [1.2,1.2,1,1,1] #Refreshing, Comforting, Satisfying, Motivating, Invigorating
    
        },
    "tacky": {
        "grow_time":8,
        "grow_time_bonus":1.25,
        "grow_fields":['sunflower','dandelion','mushroom','blue flower','sunflower'],
        "nectar_mult": [1,1.25,1.25,1,1]
    
        },
    "pesticide": {
        "grow_time":10,
        "grow_time_bonus":1.3,
        "grow_fields":['spider','bamboo','strawberry'],
        "nectar_mult": [1,1,1.3,1.3,1]#Refreshing, Comforting, Satisfying, Motivating, Invigorating
    
        },
    "petal": {
        "grow_time":14,
        "grow_time_bonus":1.5,
        "grow_fields":['sunflower','dandelion','mushroom','blue flower','clover', 'spider','strawberry','bamboo','pineapple','stump','pumpkin','cactus','rose','pine tree','coconut', 'pepper'],
        "nectar_mult": [1,1.5,1.5,1,1]#Refreshing, Comforting, Satisfying, Motivating, Invigorating

    },
    "heattreated": {
        "grow_time":12,
        "grow_time_bonus":1.5,
        "grow_fields":['sunflower','dandelion','mushroom','clover','strawberry','pineapple','stump','pumpkin','cactus','rose','mountain top','coconut', 'pepper'],
        "nectar_mult": [1,1,1,1.4,1.4]#Refreshing, Comforting, Satisfying, Motivating, Invigorating
    },   
    "hydroponic": {
        "grow_time":12,
        "grow_time_bonus":1.5,
        "grow_fields":['sunflower','dandelion','blue flower','clover','bamboo','pineapple','stump','pumpkin','cactus','mountain top','coconut', 'pine tree'],
        "nectar_mult": [1.4,1.4,1,1,1]#Refreshing, Comforting, Satisfying, Motivating, Invigorating
    },
    "plenty": {
        "grow_time":16,
        "grow_time_bonus":1.5,
        "grow_fields": ['pepper','stump','coconut','mountain top'],
        "nectar_mult": [1.5,1.5,1.5,1.5,1.5]#Refreshing, Comforting, Satisfying, Motivating, Invigorating
    }
}

def planterInfo():
    return planterData
    
