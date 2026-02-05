#original from dully176, converted by sev3482

# field drift compensation, recommened low
dwfdc = 0.2 # diamond wall
hwfdc = 0.3 # honey wall
crfdc = 0.3 # corner
# wall alignment
dwalign = 1.5 # diamond wall align (because of gap)
hwalign = 1.5 # honey wall align (drifting)

if sizeword.lower() == "xs":
    size = 0.25
elif sizeword.lower() == "s":
    size = 0.5
elif sizeword.lower() == "l":
    size = 1.5
elif sizeword.lower() == "xl":
    size = 2
else:
    size = 1

#credit to chillketchup
sizemulti = 1/10*1.2
size *= sizemulti
#-----------------------

self.keyboard.press(rotup)
self.keyboard.press(rotup)
self.keyboard.press(rotup)
self.keyboard.press(rotup)

self.keyboard.walk(rightkey, (6 + hwfdc) * size + 0.16)
self.keyboard.walk(fwdkey, 1.5 * size)
self.keyboard.walk(leftkey, 6 * size)
self.keyboard.walk(fwdkey, 1.5 * size)
self.keyboard.walk(rightkey, (6 + hwfdc + hwalign) * size)
self.keyboard.press(rotleft)
sleep(0.05)
self.keyboard.multiWalk([backkey, leftkey], (6 + dwfdc) * size)
self.keyboard.multiWalk([fwdkey, leftkey], 1.5 * size)
self.keyboard.multiWalk([fwdkey, rightkey], 6 * size)
self.keyboard.multiWalk([fwdkey, leftkey], 1.5 * size)
self.keyboard.multiWalk([backkey, leftkey], (3 + dwfdc) * size)
self.keyboard.press(rotright)
sleep(0.05)
self.keyboard.walk(backkey, (3 + dwfdc) * size)
self.keyboard.walk(leftkey, 1.5 * size)
self.keyboard.walk(fwdkey, 6 * size)
self.keyboard.walk(leftkey, 1.5 * size)
self.keyboard.walk(backkey, (6 + dwfdc) * size)
sleep(0.05)
if dwalign > 0:
    self.keyboard.walk(backkey, (dwalign + 2) * size)
    self.keyboard.walk(fwdkey, dwalign * size)
self.keyboard.press(rotleft)
self.keyboard.press(rotleft)
sleep(0.05)
self.keyboard.walk(backkey, (6 + hwfdc) * size + 0.16)
self.keyboard.walk(rightkey, 1.5 * size)
self.keyboard.walk(fwdkey, 6 * size)
self.keyboard.walk(rightkey, 1.5 * size)
self.keyboard.walk(backkey, (3 + hwfdc) * size + 0.5)
self.keyboard.press(rotright)
self.keyboard.press(rotright)
sleep(0.05)
self.keyboard.multiWalk([fwdkey, rightkey], 3 * size)
self.keyboard.multiWalk([fwdkey, leftkey], 1.5 * size)
self.keyboard.multiWalk([backkey, leftkey], 6 * size)
self.keyboard.multiWalk([fwdkey, leftkey], 1.5 * size)
self.keyboard.multiWalk([fwdkey, rightkey], 6 * size)
self.keyboard.press(rotleft)
sleep(0.05)
self.keyboard.walk(backkey, (6 + crfdc) * size)
self.keyboard.walk(leftkey, 1.5 * size)
self.keyboard.walk(fwdkey, 6 * size)
self.keyboard.walk(leftkey, 1.5 * size)
self.keyboard.walk(backkey, (3 + crfdc) * size)
self.keyboard.press(rotright)
sleep(0.05)
self.keyboard.multiWalk([backkey, rightkey], (3 + crfdc) * size)
self.keyboard.multiWalk([backkey, leftkey], 1.5 * size)
self.keyboard.multiWalk([fwdkey, leftkey], 6 * size)
self.keyboard.multiWalk([backkey, leftkey], 1.5 * size)
self.keyboard.multiWalk([backkey, rightkey], (6 + crfdc) * size)
self.keyboard.press(rotleft)
self.keyboard.press(rotleft)
sleep(0.05)
self.keyboard.multiWalk([backkey, rightkey], 6 * size)
self.keyboard.multiWalk([fwdkey, rightkey], 1.5 * size)
self.keyboard.multiWalk([fwdkey, leftkey], 5 * size)
self.keyboard.multiWalk([fwdkey, rightkey], 1.5 * size)
self.keyboard.multiWalk([backkey, rightkey], 2.5 * size)
self.keyboard.press(rotright)
self.keyboard.press(rotright)

self.keyboard.press(rotdown)
self.keyboard.press(rotdown)
self.keyboard.press(rotdown)
self.keyboard.press(rotdown)

#whatever made dully make that :sob: