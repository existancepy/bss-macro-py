#Ahk code converted by Existance Macro


cforkgap=0.75 #flowers between lines
cforkdiagonal = cforkgap*math.sqrt(2)
cforklength = (40-cforkgap*16-cforkdiagonal*4)/6
if(facingcorner) :
	self.keyboard.keyDown(fwdkey, False)
	self.keyboard.tileWait(1.5, 10)
	self.keyboard.keyUp(fwdkey, False)
self.keyboard.keyDown(tclrkey, False)
self.keyboard.keyDown(afcfbkey, False)
self.keyboard.tileWait(cforkdiagonal*2)
self.keyboard.keyUp(afcfbkey, False)
self.keyboard.tileWait(((width-1)*4+2)*cforkgap)
self.keyboard.keyDown(tcfbkey, False)
self.keyboard.tileWait(cforkdiagonal*2)
self.keyboard.keyUp(tclrkey, False)
for i in range(width):
	self.keyboard.tileWait(cforklength * size, 99)
	self.keyboard.keyUp(tcfbkey, False)
	self.keyboard.keyDown(afclrkey, False)
	self.keyboard.tileWait(cforkgap*2)
	self.keyboard.keyUp(afclrkey, False)
	self.keyboard.keyDown(afcfbkey, False)
	self.keyboard.tileWait(cforklength * size, 99)
	self.keyboard.keyUp(afcfbkey, False)
	self.keyboard.keyDown(afclrkey, False)
	self.keyboard.tileWait(cforkgap*2)
	self.keyboard.keyUp(afclrkey, False)
	self.keyboard.keyDown(tcfbkey, False)
self.keyboard.tileWait(cforklength * size, 99)
self.keyboard.keyUp(tcfbkey, False)
self.keyboard.keyDown(afclrkey, False)
self.keyboard.tileWait(cforkgap*2)
self.keyboard.keyUp(afclrkey, False)
self.keyboard.keyDown(afcfbkey, False)
self.keyboard.tileWait(cforklength * size, 99)
self.keyboard.keyUp(afcfbkey, False)