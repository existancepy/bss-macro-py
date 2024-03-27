import re

generalReplace = {
    ":=": "=",
    "reps": "width",
    "'": '"',
    "sqrt": "math.sqrt",
    '""':'"',
    "\ufeff":"",
    "a_index":"i"
}

def ahkPatternToPython(ahk):
    #set to lowercase
    ahk = ahk.lower()

    #do replacements
    for k, v in generalReplace.items():
        ahk = ahk.replace(k,v)
    #convert into lines
    #comments and identations
    ahkCleaned = [x.split(";")[0].strip() for x in ahk.split("\n")]
    #remove empty lines
    ahkCleaned = [x for x in ahkCleaned if x]
    #auto indent
    #remove single close brackets
    out = []
    level = 0
    for line in ahkCleaned:
        if line == "}":
            level -= 1
        else:
            out.append("{}{}".format("\t"*level, line))
            if line[-1] == "{":
                level += 1
        
    #extract out only the pattern code
    start = None
    end = None
    for i,e in enumerate(out):
        if e.startswith("(LTrimJoin"):
            start = i+1
        elif e == ')"':
            end = i
    if not start is None and not end is None:
        out = out[start:end]
    #convert loop reps
    for i,e in enumerate(out[:]):
        line = e.strip()
        noSpaces = line.replace(" ","")
        #replace loop
        if noSpaces == 'loop"width"{' or noSpaces == 'loopwidth{':
            out[i] = e.replace(line, 'for i in range(width):')
        #convert send
        elif line.startswith("send"):
            cmds = []
            lineCopy = line
            while True:
                openB = lineCopy.find("{")
                closeB = lineCopy.find("}")
                if openB == -1 or closeB == -1:
                    identation = leading_spaces = len(e) - len(e.lstrip())
                    out[i] = e.replace(line, "\n{}".format(identation*"\t").join(cmds))
                    break
                add = lineCopy[openB:closeB+1]
                lineCopy = lineCopy.replace(add,"",1)
                add = add[1:-1].strip()
                #remove whitespace between quotations
                add = re.sub(r'"\s*([^"]*?)\s*"', r'"\1"', add)
                #split into parameters
                args = add.split(" ")

                #get key
                key = args[0]
                #check if variable 
                if key[0] == '"' and key[-1] == '"':
                    key = key[1:-1]
                else:
                    key = f'"{key}"'
                #get command
                if args[1] == "up":
                    cmds.append(f"keyboard.release({key})")
                elif args[1] == "down":
                    cmds.append(f"keyboard.press({key})")
                elif args[1].isdigit():
                    for _ in range(int(args[1])):
                        cmds.append(f"keyboard.press({key})")
                        cmds.append(f"time.sleep(0.08)")
                        cmds.append(f"keyboard.release({key})")
        #deal with waits
        elif line.startswith("walk"):
            out[i] = e.replace("walk", "move.tileWait").replace('"',"")
        elif line.startswith("if"):
            out[i] = e.replace('"',"").replace(" ","").replace("{",":")
    return "\n".join(out)
