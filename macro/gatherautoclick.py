from pynput.mouse import Button, Controller
import time
mouse = Controller()
open("status.txt","w").write("none")
while True:
    status = open("status.txt",'r').read()
    if status == "gathering":
        mouse.click(Button.left)
        time.sleep(0.8)
        
