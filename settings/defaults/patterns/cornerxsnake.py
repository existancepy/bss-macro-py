if sizeword.lower() == "xs":
    size = 0.5
elif sizeword.lower() == "s":
    size = 1
elif sizeword.lower() == "l":
    size = 2
elif sizeword.lower() == "xl":
    size = 2.5
else:
    size = 1.5
    
wm = 0.5*size
sm = 0.25*size
df = (((wm*2)**2)+((sm*4)**2))**0.5
self.keyboard.walk(tclrkey,wm)
self.keyboard.walk(tcfbkey,sm)
self.keyboard.walk(afclrkey,wm*2)
self.keyboard.walk(tcfbkey,sm)
self.keyboard.walk(tclrkey,wm*2)
self.keyboard.keyDown(afclrkey)
self.keyboard.keyDown(afcfbkey)
sleep(df)
self.keyboard.keyUp(afcfbkey)
self.keyboard.keyUp(afclrkey)
self.keyboard.walk(tclrkey,wm*2)
self.keyboard.walk(tcfbkey,sm)
self.keyboard.walk(afclrkey,wm*2)
self.keyboard.walk(tcfbkey,sm*8)
self.keyboard.walk(afclrkey,0.6*width)
self.keyboard.walk(tclrkey,0.4*width)
self.keyboard.walk(afcfbkey,sm*4)
self.keyboard.walk(tclrkey,wm*2)
self.keyboard.walk(afcfbkey,sm)
self.keyboard.walk(afclrkey,wm*2)
self.keyboard.walk(afcfbkey,sm)
self.keyboard.walk(tclrkey,wm*2)
self.keyboard.walk(afcfbkey,sm)
self.keyboard.walk(afclrkey,wm*2)
self.keyboard.walk(afcfbkey,sm)
self.keyboard.walk(tclrkey,wm*2)
self.keyboard.keyDown(tcfbkey)
self.keyboard.keyDown(afclrkey)
sleep(df/2)
self.keyboard.keyUp(afclrkey)
self.keyboard.keyUp(tcfbkey)




        
