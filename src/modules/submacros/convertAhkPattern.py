import re

generalReplace = {
    ":=": "𑑛",
    "reps": "width",
    "'": '"',
    "sqrt": "math.sqrt",
    "\ufeff":"",
    "a_index":"i",
    "&&": "and",
    ";": "#",
    "||": "or",
    "static": "",
    "dir": "direc",
}

def ahkPatternToPython(ahk):

    def checkOrder(string, pattern):
        i, j = 0, 0
        for char in string:
            if char == pattern[j]:
                j += 1
            if j == len(pattern):
                return True
            i += 1
     
        return False
    
    #set to lowercase
    ahk = ahk.lower()
    
    #do replacements
    for k, v in generalReplace.items():
        ahk = ahk.replace(k,v)

    #convert = to ==, but ignore != and =>
    # Use regex to match `=` that is not part of `=>` or `!=`
    ahk = re.sub(r'(?<![!>])=(?![>])', '==', ahk)
    #replace double quotes ("") with a single quote (") only when they are not preceded by =, >, or <
    ahk = re.sub(r'(?<![=><])""', '"', ahk)

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
            if line[-1] == "{" and line[0] == "}":
                level -=1
            out.append("{}{}".format("\t"*level, line))
            if line[-1] == "{":
                level += 1
    #extract out only the pattern code
    start = None
    end = None
    for i,e in enumerate(out):
        if "patterns[" in e:
            start = i+2
        elif e == ')"':
            end = i
    if not start is None and not end is None:
        out = out[start:end]
    
    #convert ahk to python
    indentLine = False
    for i,e in enumerate(out[:]):
        if indentLine:
            e = "\t" + e
            out[i] = e
            indentLine = False
            
        line = e.strip()
        noSpaces = line.replace(" ","")
        
        #replace loop
        if noSpaces == 'loop"width"{' or noSpaces == 'loopwidth{':
            out[i] = e.replace(line, 'for i in range(width):')
        elif line.startswith("loop"):
            #loop number of times
            digits = ''.join([x for x in line if x.isdigit()])
            if digits: 
                out[i] = e.replace(line, f'for i in range({int(digits)}):')
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
                if (key[0] == '"' and key[-1] == '"') or (key[0] == '%' and key[-1] == '%'):
                    key = key[1:-1]
                    #check for weird variable string thing that ahk can do
                    if key.count("%") == 2:
                        # Use regex to find text between %%
                        varNames = re.findall(r'%([^%]+)%', key)
                        # Remove the varNames from the input string
                        nonVarString = re.sub(r'%[^%]+%', '', key)
                        #use locals to access variables as a string
                        key = "locals[f'" + nonVarString + ''.join(["{" + x + "}" for x in varNames]) + "']"
                else:
                    key = f'"{key}"'
                #get command
                if args[1] == "up":
                    cmds.append(f"self.keyboard.keyUp({key}, False)")
                elif args[1] == "down":
                    cmds.append(f"self.keyboard.keyDown({key}, False)")
                elif args[1].isdigit():
                    for _ in range(int(args[1])):
                        cmds.append(f"self.keyboard.press({key})")
                else: #its probably a variable
                    var = args[1].replace('"', "").replace("%", "")
                    cmds.append(f"for _ in range({var}):")
                    cmds.append(f"\tself.keyboard.press({key})")
                
        #deal with waits
        elif line.startswith("walk"):
            out[i] = e.replace("walk", "self.keyboard.tileWait").replace('"',"")
        #if/else statements
        elif line.startswith("if"):
            if "{" in line: #regular nested if statement
                out[i] = e.replace("{",":")
            #one line if statement
            else:
                out[i] = e + ":"
                indentLine = True
                
        elif "else" in line and not "if" in line:
            out[i] = e.replace(line, "else:")
        #one line if/else statements
        elif checkOrder(line, "?:"):
            if "𑑛" in line:
                e = e.split("𑑛")[1]
            conditionSection, resultSection = e.split("?")
            trueSection, falseSection = resultSection.split(":")
            out[i] = out[i].replace(e, f"{trueSection} if {conditionSection} else {falseSection}")
        #function definition
        elif checkOrder(line, "(){") and not checkOrder(line, "𑑛(){"):
            out[i] = "def " + out[i].replace("{", ":")
            
        
    out.insert(0, "#Ahk code converted by Existance Macro\n\n")
    return "\n".join(out).replace("𑑛", "=")

test = '''

;@NoInterrupt
CameraRot(Dir, Num) {
	Static rot := false
	Static LRNum := 0
	Static LRDir := "Right"
	Init := OnExit((*) => rot && send("{" Rot%LRDir% " " Abs(LRNum) "}"), -1) 
	send "{" Rot%Dir% " " Num "}"
	rot := (dir = "Up" || dir = "Down" || dir = "Left" || dir = "Right")
	if (Dir="Left" || Dir="Right") {
		LRNum := (Dir="Left") ? LRNum+Num : LRNum-Num
		LRDir := (LRNum<0) ? "Right" : "Left"
	}
}
;function created by Kuruni and SP

Move(Dir, Dis, Dir2:="") {
	DirType := (Dir2!="")
	send "{" Dir " down}"
	if (DirType)
		send "{" Dir2 " down}"
	Walk(Dis)
	send "{" Dir " up}"
	if (DirType)
		send "{" Dir2 " up}"
}
;function created by Kuruni

loop reps {
	Move("s", 4)
	Move("d", 12)
	Move("w", 4, "a")
	Move("a", 8)
	Move("s", 4, "d")
	Move("a", 1)

	CameraRot("Right", 1)
	
	Move("w", 7)
	Move("s", 7, "d")
	Move("w", 5, "d")
	Move("a", 7)
	Move("w", 5, "d")
	Move("s", 7)
	Move("a", 10, "s")
	
	CameraRot("Right", 1)
	
	Move("w", 10)
	Move("a", 5, "s")
	Move("d", 5, "s")
	
	CameraRot("Left", 2)
	
}
'''
#print(ahkPatternToPython(test))

