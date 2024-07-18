import cv2
import numpy as np

redcannon = cv2.imread('./sussers.png')
img = cv2.imread('./redcannon.png')
img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
res = cv2.matchTemplate(img_cv, redcannon, cv2.TM_CCOEFF_NORMED)
print(cv2.minMaxLoc(res))
