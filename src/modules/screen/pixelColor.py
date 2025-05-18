import mss 
import numpy as np
def getPixelColor(X1,Y1):
    region = {'top': Y1, 'left': X1, 'width': 1, 'height': 1}
    
    with mss.mss() as sct:
        img = sct.grab(region)
        im = np.array(img)
        col = tuple(im[0,0])[:-1][::-1]
        return col