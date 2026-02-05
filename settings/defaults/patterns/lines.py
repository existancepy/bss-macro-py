#Ahk code converted by Existance Macro


for i in range(width):
	self.keyboard.keyDown(tcfbkey, False)
	self.keyboard.tileWait(11 * size)
	self.keyboard.keyUp(tcfbkey, False)
	self.keyboard.keyDown(tclrkey, False)
	self.keyboard.tileWait(1)
	self.keyboard.keyUp(tclrkey, False)
	self.keyboard.keyDown(afcfbkey, False)
	self.keyboard.tileWait(11 * size)
	self.keyboard.keyUp(afcfbkey, False)
	self.keyboard.keyDown(tclrkey, False)
	self.keyboard.tileWait(1)
	self.keyboard.keyUp(tclrkey, False)
#away from center
for i in range(width):
	self.keyboard.keyDown(tcfbkey, False)
	self.keyboard.tileWait(11 * size)
	self.keyboard.keyUp(tcfbkey, False)
	self.keyboard.keyDown(afclrkey, False)
	self.keyboard.tileWait(1)
	self.keyboard.keyUp(afclrkey, False)
	self.keyboard.keyDown(afcfbkey, False)
	self.keyboard.tileWait(11 * size)
	self.keyboard.keyUp(afcfbkey, False)
	self.keyboard.keyDown(afclrkey, False)
	self.keyboard.tileWait(1)
	self.keyboard.keyUp(afclrkey, False)
