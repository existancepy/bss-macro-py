from modules.screen.imageSearch import templateMatch
import cv2

screen = cv2.imread("setting.png")
template =  cv2.imread("./images/menu/robloxmenu-retina.png")

print(templateMatch(template, screen))