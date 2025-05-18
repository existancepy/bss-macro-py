import cv2
import modules.screen.ocr as ocr
from PIL import Image
import numpy as np

display_type = "built-in"
#Load quest data from quest_data.txt
quest_data = {}
quest_bear = ""
quest_title = ""
quest_info = []

with open("./data/bss/quest_data.txt", "r") as f:
    qdata = [x for x in f.read().split("\n") if x]

for line in qdata:
    if line.startswith("==") and line.endswith("=="): #bear
        if quest_title:
            quest_data[quest_bear][quest_title] = quest_info  
        quest_bear = line.strip("=")
        quest_data[quest_bear] = {}
        quest_title, quest_info = "", []
    
    elif line.startswith("-"): #new quest title
        if quest_title:  
            quest_data[quest_bear][quest_title] = quest_info
        quest_title = line.lstrip("-").strip()
        quest_info = []
    
    else:  #quest objectives
        quest_info.append(line)
quest_data[quest_bear][quest_title] = quest_info 

#quest title found, now find the objectives
questTitle = "scorpion salad"
questGiver = "polar bear"
objectives = quest_data[questGiver][questTitle]

#merge the texts into chunks. Using those chunks, compare it with the known objectives
#assume that the merging is done properly, so 1st chunk = 1st objective
screen = cv2.imread("quest.png")
#crop it below the quest title
questTitleYPos = 80
# screen = screen[questTitleYPos: , : ]

screenOriginal = np.copy(screen)
#convert to grayscale
screenGray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
img = cv2.inRange(screenGray, 0, 50)
img = cv2.GaussianBlur(img, (5, 5), 0)
#dilute the image so that texts can be merged into chunks
kernelSize = 10 if display_type == "retina" else 7
kernel = np.ones((kernelSize, kernelSize), np.uint8) 
img = cv2.dilate(img, kernel, iterations=1)
contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#filter out the contour sizes
minArea = 8000       #too small = noise
maxArea = 80000      #too big = background or large UI elements
maxHeight = 150       #cap height to filter out title bar

if display_type == "built-in":
    minArea //= 2
    maxArea //= 2
    maxHeight //= 2


completedObjectives = []
incompleteObjectives = []
i = 0
for contour in contours[::-1]:
    x, y, w, h = cv2.boundingRect(contour)
    #check if contour meets size requirements
    area = w*h
    if area < minArea or area > maxArea or h > maxHeight:
        cv2.rectangle(screen, (x, y), (x+w, y+h), (0, 255, 255), 1) #draw a yellow bounding box
        print(area)
        print(h)
        continue
    textImg =  Image.fromarray(screen[y:y+h, x:x+w])
    textChunk = []
    for line in ocr.ocrRead(textImg):
        textChunk.append(line[1][0].strip().lower())
    textChunk = ''.join(textChunk)
    print(textChunk)
    if "complete" in textChunk:
        completedObjectives.append(objectives[i])
        color = (0, 255, 0)  #green
    else:
        incompleteObjectives.append(objectives[i])
        color = (0, 0, 255)  #red
    
    #draw bounding boxes and add the quest text
    cv2.rectangle(screen, (x, y), (x+w, y+h), color, 2)
    cv2.putText(screen, objectives[i], (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    i += 1

    if i == len(objectives):
        break

questImgPath = "latest-quest.png"
cv2.imshow("a", screen)
cv2.waitKey(0)
#cv2.imwrite(questImgPath, screenOriginal)

print(completedObjectives)
print(incompleteObjectives)