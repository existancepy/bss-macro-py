#original by dully176, converted by chillketchup

#change to True if you are using digital bee
digistops = False

#amount of field drift compensation, recommend having it low.
passivefdc = 0.3

#other variables, don't change unless you know what you are doing
stepsize = 3
rightdrift = 2
rightoff = 2
downdrift = 1
downoff = 3

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

sizemulti = 1/10*1.2
size *= sizemulti
passivefdc *= sizemulti


#pattern code
self.keyboard.press(rotup)
self.keyboard.press(rotup)
self.keyboard.press(rotup)
self.keyboard.press(rotup)

#one (variant 1) (digital)
self.keyboard.walk(backkey, stepsize * size)
self.keyboard.walk(rightkey, stepsize * size)
self.keyboard.walk(fwdkey, stepsize * size)
self.keyboard.press(rotleft)
self.keyboard.press(rotleft)
sleep(0.05)
self.keyboard.walk(backkey, (rightdrift + rightoff) * sizemulti)
self.keyboard.walk(fwdkey, rightoff * sizemulti)
if digistops: sleep(0.8)
self.keyboard.press(rotright)
self.keyboard.press(rotright)
sleep(0.05)
self.keyboard.walk(leftkey, stepsize * size * 2)
if digistops: sleep(0.85)
self.keyboard.press(rotleft)
sleep(0.05)
self.keyboard.multiWalk([backkey, leftkey], stepsize * size)
self.keyboard.multiWalk([backkey, rightkey], stepsize * size)
self.keyboard.multiWalk([fwdkey, rightkey], stepsize * size * 2)
self.keyboard.press(rotright)
sleep(0.05)
self.keyboard.walk(leftkey, stepsize * size)
if digistops: sleep(0.85)
self.keyboard.walk(backkey, stepsize * size)
self.keyboard.walk(rightkey, stepsize * size * 2)
self.keyboard.press(rotleft)
sleep(0.05)
self.keyboard.multiWalk([fwdkey, rightkey], stepsize * size)
self.keyboard.multiWalk([fwdkey, leftkey], stepsize * size)
self.keyboard.multiWalk([backkey, leftkey], stepsize * size)
self.keyboard.press(rotright)
sleep(0.05)

#two (digital)
self.keyboard.multiWalk([backkey, rightkey], stepsize * size + passivefdc)
if digistops: sleep(0.85)
self.keyboard.multiWalk([fwdkey, rightkey], stepsize * size)
self.keyboard.multiWalk([fwdkey, leftkey], stepsize * size)
self.keyboard.multiWalk([backkey, leftkey], stepsize * size * 2)
self.keyboard.press(rotleft)
sleep(0.05)
self.keyboard.walk(backkey, stepsize * size + passivefdc)
self.keyboard.walk(rightkey, stepsize * size)
self.keyboard.walk(fwdkey, stepsize * size * 2)
self.keyboard.press(rotright)
sleep(0.05)
self.keyboard.multiWalk([backkey, leftkey], stepsize * size)
if digistops: sleep(0.85)
self.keyboard.multiWalk([backkey, rightkey], stepsize * size + passivefdc)
self.keyboard.multiWalk([fwdkey, rightkey], stepsize * size * 2)
self.keyboard.press(rotleft)
sleep(0.05)
self.keyboard.walk(fwdkey, stepsize * size)
if digistops: sleep(0.85)
self.keyboard.walk(leftkey, stepsize * size)
self.keyboard.walk(backkey, stepsize * size + passivefdc)
self.keyboard.press(rotright)
sleep(0.05)

#one (variant 2)
self.keyboard.walk(backkey, stepsize * size)
self.keyboard.walk(rightkey, stepsize * size)
self.keyboard.walk(fwdkey, stepsize * size)
self.keyboard.walk(leftkey, stepsize * size * 2)
self.keyboard.press(rotleft)
sleep(0.05)
self.keyboard.multiWalk([backkey, leftkey], stepsize * size)
self.keyboard.press(rotleft)
sleep(0.05)
self.keyboard.walk(leftkey, (downdrift + downoff) * sizemulti)
self.keyboard.walk(rightkey, downoff * sizemulti)
self.keyboard.press(rotright)
sleep(0.05)
self.keyboard.multiWalk([backkey, rightkey], stepsize * size)
self.keyboard.multiWalk([fwdkey, rightkey], stepsize * size * 2)
self.keyboard.press(rotright)
sleep(0.05)
self.keyboard.walk(leftkey, stepsize * size)
self.keyboard.walk(backkey, stepsize * size)
self.keyboard.walk(rightkey, stepsize * size * 2)
self.keyboard.press(rotleft)
sleep(0.05)
self.keyboard.multiWalk([fwdkey, rightkey], stepsize * size)
self.keyboard.multiWalk([fwdkey, leftkey], stepsize * size)
self.keyboard.multiWalk([backkey, leftkey], stepsize * size)
self.keyboard.press(rotright)
sleep(0.05)

#two
self.keyboard.multiWalk([backkey, rightkey], stepsize * size + passivefdc)
self.keyboard.multiWalk([fwdkey, rightkey], stepsize * size)
self.keyboard.multiWalk([fwdkey, leftkey], stepsize * size)
self.keyboard.multiWalk([backkey, leftkey], stepsize * size * 2)
self.keyboard.press(rotleft)
sleep(0.05)
self.keyboard.walk(backkey, stepsize * size + passivefdc)
self.keyboard.walk(rightkey, stepsize * size)
self.keyboard.walk(fwdkey, stepsize * size * 2)
self.keyboard.press(rotright)
sleep(0.05)
self.keyboard.multiWalk([backkey, leftkey], stepsize * size)
self.keyboard.multiWalk([backkey, rightkey], stepsize * size + passivefdc)
self.keyboard.multiWalk([fwdkey, rightkey], stepsize * size * 2)
self.keyboard.press(rotleft)
sleep(0.05)
self.keyboard.walk(fwdkey, stepsize * size)
self.keyboard.walk(leftkey, stepsize * size)
self.keyboard.walk(backkey, stepsize * size + passivefdc)
self.keyboard.press(rotright)
sleep(0.05)

self.keyboard.press(rotdown)
self.keyboard.press(rotdown)
self.keyboard.press(rotdown)
self.keyboard.press(rotdown)

#hi
