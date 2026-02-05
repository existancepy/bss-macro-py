
self.keyboard.walk(tclrkey,(0.25*size))
self.keyboard.walk(tcfbkey,(0.25*size))
for i in range(width):
    if i != 0:
        self.keyboard.walk(tclrkey,(0.2*i)/2)
        self.keyboard.walk(tcfbkey,(0.2*i)/2)
    self.keyboard.walk(afclrkey,0.5*size+0.2*i)
    self.keyboard.walk(afcfbkey,0.5*size+0.2*i)
    self.keyboard.walk(tclrkey,0.5*size+0.2*i)
    self.keyboard.walk(tcfbkey,0.5*size+0.2*i)

for i in range(width,0,-1):
    if i != width:
        self.keyboard.walk(afcfbkey,(0.2*i)/2)
        self.keyboard.walk(afclrkey,(0.25*i)/2)
    self.keyboard.walk(afclrkey,0.5*size+0.2*i)
    self.keyboard.walk(afcfbkey,0.5*size+0.2*i)
    self.keyboard.walk(tclrkey,0.5*size+0.2*i)
    self.keyboard.walk(tcfbkey,0.5*size+0.2*i)

    
self.keyboard.walk(afcfbkey,0.25*size)
self.keyboard.walk(afclrkey,0.25*size)

    
 

    
    
