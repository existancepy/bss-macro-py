import ast
#returns a dictionary containing the settings
profileName = "a"
def readSettingsFile(path):
    #get each line
    #read the file, format it to:
    #[[key, value], [key, value]]
    with open(path) as f:
        data = [[x.strip() for x in y.split("=", 1)] for y in f.read().split("\n") if y]
    f.close()
    #convert to a dict
    out = {}
    for k,v in data:
        try:
            out[k] = ast.literal_eval(v)
        except:
            #check if integer
            if v.isdigit():
                out[k] = int(v)
            elif v.replace(".","",1).isdigit():
                out[k] = float(v)
            out[k] = v
    return out

def saveDict(path, data):
    out = "\n".join([f"{k}={v}" for k,v in data.items()])
    with open(path, "w") as f:
        f.write(str(out))
    f.close()

#update one property of a setting
def saveSettingFile(setting,value, path):
    #get the dictionary
    data = readSettingsFile(path)
    #update the dictionary
    data[setting] = value
    #write it
    saveDict(path, data)

def loadFields():
    with open(f"../settings/profiles/{profileName}/fields.txt") as f:
        out = ast.literal_eval(f.read())
    f.close()
    for field,settings in out.items():
        for k,v in settings.items():
            #check if integer
            if isinstance(v,str): 
                if v.isdigit(): out[field][k] = int(v)
                elif v.replace(".","",1).isdigit(): out[field][k] = float(v)
    return out

def saveField(field, settings):
    fieldsData = loadFields()
    fieldsData[field] = settings
    with open(f"../settings/profiles/{profileName}/fields.txt", "w") as f:
        f.write(str(fieldsData))
    f.close()

def saveProfileSetting(setting, value):
    saveSettingFile(setting, value, f"../settings/profiles/{profileName}/settings.txt")

#increment a setting, and return the dictionary for the setting
def incrementProfileSetting(setting, incrValue):
    #get the dictionary
    data = readSettingsFile(f"../settings/profiles/{profileName}/settings.txt")
    #update the dictionary
    data[setting] += incrValue
    #write it
    saveDict(f"../settings/profiles/{profileName}/settings.txt", data)
    return data

def saveGeneralSetting(setting, value):
    saveSettingFile(setting, value, "../settings/generalsettings.txt")

def loadSettings():
    return readSettingsFile(f"../settings/profiles/{profileName}/settings.txt")

#return a dict containing all settings except field (general, profile, planters)
def loadAllSettings():
    return {**loadSettings(), **readSettingsFile("../settings/generalsettings.txt")}

#clear a file
def clearFile(filePath):
    open(filePath, 'w').close()