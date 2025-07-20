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

self.keyboard.walk(tcfbkey,1.2*size)
self.keyboard.walk(afclrkey,0.7*width)
self.keyboard.walk(tclrkey,0.4*width)
self.keyboard.walk(afcfbkey,0.6*size)

for _ in range(2):
    self.keyboard.walk(afcfbkey,0.5*size)
    for _ in range(width):
        self.keyboard.walk(tclrkey,0.17)
        self.keyboard.walk(tclrkey,0.17)
        
    for _ in range(width):
        self.keyboard.walk(tcfbkey,0.5*size)
        self.keyboard.walk(afclrkey,0.17)
        self.keyboard.walk(afcfbkey,0.5*size)
        self.keyboard.walk(afclrkey,0.17)
    self.keyboard.walk(tcfbkey,0.5*size)

    for _ in range(width):
        self.keyboard.walk(tclrkey,0.17)
        self.keyboard.walk(tclrkey,0.17)

    for _ in range(width):
        self.keyboard.walk(afcfbkey,0.5*size)
        self.keyboard.walk(afclrkey,0.17)
        self.keyboard.walk(tcfbkey,0.5*size)
        self.keyboard.walk(afclrkey,0.17)





        
