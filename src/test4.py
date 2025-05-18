from datetime import timedelta

def cdTextToSecs(rawText, brackets, defaultTime=0):
    if brackets:
        closePos = rawText.rfind(")")
        #get cooldown if close bracket is present or not
        if closePos >= 0:
            cooldownRaw = rawText[rawText.rfind("(")+1:closePos]
        elif "(" in rawText:
            cooldownRaw = rawText.split("(")[1]
        else:
            cooldownRaw = rawText
    else:
        cooldownRaw = rawText
    #clean it up, extract only valid characters
    cooldownRaw = ''.join([x for x in cooldownRaw if x.isdigit() or x == ":" or x == "s"])
    cooldownSeconds = None #cooldown in seconds

    def extractNumFromText(text):
        return ''.join(filter(str.isdigit, text))
    
    #convert time to seconds
    validTime = True
    if ":" in cooldownRaw:
        times = cooldownRaw.split(":")
        cooldownSeconds = 0
        #convert
        for i,e in enumerate(times[::-1]):
            num = extractNumFromText(e)
            if not num:
                validTime = False
                break
            cooldownSeconds += int(num) * 60**i

    elif cooldownRaw.count("s") == 1: #only seconds
        num = extractNumFromText(e)
        if not num:
            validTime = False
        cooldownSeconds = num
    else:
        validTime = False
    
    if not validTime or (defaultTime and cooldownSeconds > defaultTime):
        cooldownSeconds = defaultTime

    return cooldownSeconds


ans = cdTextToSecs("Use the wealth clock (57:01)", True, 0)
print(ans)
print(timedelta(seconds=ans))