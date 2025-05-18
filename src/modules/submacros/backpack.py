
import modules.screen.pixelColor as pixelColor
data = {6975603: 2, 8518291: 6, 8518034: 9, 8517778: 11, 8517521: 13, 8517264: 14, 8517008: 15, 8517007: 16, 8516751: 17, 8450959: 22, 8450702: 19, 8450190: 20, 8450189: 26, 8450446: 23, 8449933: 27, 8384140: 29, 8383884: 30, 8383115: 31, 8315013: 33, 8380036: 34, 8313987: 36, 8379267: 37, 8313218: 38, 8378497: 39, 8377214: 41, 8376701: 42, 8375932: 43, 8440186: 44, 8439673: 47, 8439159: 48, 8503925: 49, 8503413: 50, 8567923: 52, 8632433: 53, 8696687: 55, 8825706: 59, 8890473: 60, 9020006: 61, 9085029: 63, 9084516: 64, 9214818: 65, 9214305: 66, 9409630: 67, 9474397: 68, 9538908: 69, 9799256: 71, 9863767: 73, 10059348: 75, 10254418: 76, 10319441: 77, 10449486: 78, 10580046: 79, 10710092: 80, 10774858: 81, 11035976: 82, 11231045: 84, 11296068: 85, 11491394: 86, 11752511: 87, 11817535: 88, 12143932: 90, 12404537: 91, 12469561: 92, 12795958: 93, 12861237: 94, 13187891: 96, 13449266: 97, 13776175: 99, 13886187: 100}
data = sorted(data.items())     
#0% 7697781
#31% 8381831
#52% 8502900
#84% 11231045
#100% 14889259

def rgb_to_dec(r, g, b):
      return (r * 256 * 256) + (g * 256) + b
    
def bpc(mw, newUI):
    Y1=6
    add = 59+3
    
    if newUI: Y1 = 31  
    X1=mw//2+add
    
    pix = pixelColor.getPixelColor(X1, Y1)
    col = rgb_to_dec(*pix)
    perc = 0
    #natro's backpack calc
    if col & 0xFF0000 <= 0x690000: # less or equal to 50%
        if(col & 0xFF0000 <= 0x4B0000) : #less or equal to 25%
            if(col & 0xFF0000 <= 0x420000) : #less or equal to 10%
                if((col & 0xFF0000 <= 0x410000) and (col & 0x00FFFF <= 0x00FF80) and (col & 0x00FFFF > 0x00FF86)): #less or equal to 5%
                    perc=0
                elif((col & 0xFF0000 > 0x410000) and (col & 0x00FFFF <= 0x00FF80) and (col & 0x00FFFF > 0x00FC85)): #greater than 5%
                    perc=5
                else:
                    perc=0
                            
            else: #greater than 10%
                if((col & 0xFF0000 <= 0x470000)) : #less or equal to 20%
                    if((col & 0xFF0000 <= 0x440000) and (col & 0x00FFFF <= 0x00FE85) and (col & 0x00FFFF > 0x00F984)): #less or equal to 15%
                        perc=10
                    elif((col & 0xFF0000 > 0x440000) and (col & 0x00FFFF <= 0x00FB84) and (col & 0x00FFFF > 0x00F582)): #greater than 15%
                        perc=15
                    else:
                        perc=0
                                    
                elif((col & 0xFF0000 > 0x470000) and (col & 0x00FFFF <= 0x00F782) and (col & 0x00FFFF > 0x00F080)): #greater than 20%
                    perc=20
                else:
                    perc=0
                            
                    
        else: #greater than 25%
            if(col & 0xFF0000 <= 0x5B0000) : #less or equal to 40%
                if((col & 0xFF0000 <= 0x4F0000) and (col & 0x00FFFF <= 0x00F280) and (col & 0x00FFFF > 0x00EA7D)): #less or equal to 30%
                    perc=25
                else : #greater than 30%
                    if((col & 0xFF0000 <= 0x550000) and (col & 0x00FFFF <= 0x00EC7D) and (col & 0x00FFFF > 0x00E37A)): #less or equal to 35%
                        perc=30
                    elif((col & 0xFF0000 > 0x550000) and (col & 0x00FFFF <= 0x00E57A) and (col & 0x00FFFF > 0x00DA76)): #greater than 35%
                        perc=35
                    else:
                        perc=0
                        
                
            else: #greater than 40%
                if((col & 0xFF0000 <= 0x620000) and (col & 0x00FFFF <= 0x00DC76) and (col & 0x00FFFF > 0x00D072)): #less or equal to 45%
                    perc=40
                elif((col & 0xFF0000 > 0x620000) and (col & 0x00FFFF <= 0x00D272) and (col & 0x00FFFF > 0x00C66D)): #greater than 45%
                    perc=45
                else:
                    perc=0
                            
                    
            
    else : #greater than 50%
        if(col & 0xFF0000 <= 0x9C0000) : #less or equal to 75%
            if(col & 0xFF0000 <= 0x850000) : #less or equal to 65%
                if(col & 0xFF0000 <= 0x7B0000) : #less or equal to 60%
                    if((col & 0xFF0000 <= 0x720000) and (col & 0x00FFFF <= 0x00C86D) and (col & 0x00FFFF > 0x00BA68)): #less or equal to 55%
                        perc=50
                    elif ((col & 0xFF0000 > 0x720000) and (col & 0x00FFFF <= 0x00BC68) and (col & 0x00FFFF > 0x00AD62)): #greater than 55%
                        perc=55
                    else:
                        perc=0
                                    
                elif((col & 0xFF0000 > 0x7B0000) and (col & 0x00FFFF <= 0x00AF62) and (col & 0x00FFFF > 0x009E5C)): #greater than 60%
                    perc=60
                else:
                    perc=0      
            else : #greater than 65%
                if((col & 0xFF0000 <= 0x900000) and (col & 0x00FFFF <= 0x00A05C) and (col & 0x00FFFF > 0x008F55)): #less or equal to 70%
                    perc=65
                elif((col & 0xFF0000 > 0x900000) and (col & 0x00FFFF <= 0x009155) and (col & 0x00FFFF > 0x007E4E)): #greater than 70%
                    perc=70
                else:
                    perc=0
                            
                    
        else: #greater than 75%
            if((col & 0xFF0000 <= 0xC40000)): #less or equal to 90%
                if((col & 0xFF0000 <= 0xA90000) and (col & 0x00FFFF <= 0x00804E) and (col & 0x00FFFF > 0x006C46)) : #less or equal to 80%
                    perc=75
                else: #greater than 80%
                    if((col & 0xFF0000 <= 0xB60000) and (col & 0x00FFFF <= 0x006E46) and (col & 0x00FFFF > 0x005A3F)) : #less or equal to 85%
                        perc=80
                    elif((col & 0xFF0000 > 0xB60000) and (col & 0x00FFFF <= 0x005D3F) and (col & 0x00FFFF > 0x004637)): #greater than 85%
                        perc=85
                    else:
                        perc=0
                                    
                            
            else: #greater than 90%
                if((col & 0xFF0000 <= 0xD30000) and (col & 0x00FFFF <= 0x004A37) and (col & 0x00FFFF > 0x00322E)) : #less or equal to 95%
                    perc=90
                else: #greater than 95%
                    if col == 0xF70017 or ((col & 0xFF0000 >= 0xE00000) and (col & 0x00FFFF <= 0x002427) and (col & 0x00FFFF > 0x001000)): #is equal to 100%
                        perc=100
                    elif((col & 0x00FFFF <= 0x00342E)):
                        perc=95
                    else:
                        perc=0
    #print("Pixel Colour: {}, Backpack Percentage: {}.".format(col, perc))
    return perc