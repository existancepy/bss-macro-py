#Ahk code converted by Existance Macro


self.keyboard.keyDown(tclrkey, False)
self.keyboard.tileWait(( 4 * size ) + ( width * 0.1 ) - 0.1)
self.keyboard.keyUp(tclrkey, False)
self.keyboard.keyDown(afclrkey, False)
self.keyboard.tileWait( 8 * size )
self.keyboard.keyUp(afclrkey, False)
self.keyboard.keyDown(tclrkey, False)
self.keyboard.tileWait( 4 * size )
self.keyboard.keyUp(tclrkey, False)
