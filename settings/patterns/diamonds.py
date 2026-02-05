#Ahk code converted by Existance Macro


for i in range(width):
	self.keyboard.keyDown(tcfbkey, False)
	self.keyboard.keyDown(tclrkey, False)
	self.keyboard.tileWait(5 * size + i)
	self.keyboard.keyUp(tclrkey, False)
	self.keyboard.keyDown(afclrkey, False)
	self.keyboard.tileWait(5 * size + i)
	self.keyboard.keyUp(tcfbkey, False)
	self.keyboard.keyDown(afcfbkey, False)
	self.keyboard.tileWait(5 * size + i)
	self.keyboard.keyUp(afclrkey, False)
	self.keyboard.keyDown(tclrkey, False)
	self.keyboard.tileWait(5 * size + i)
	self.keyboard.keyUp(tclrkey, False)
	self.keyboard.keyUp(afcfbkey, False)