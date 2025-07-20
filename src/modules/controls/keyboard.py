import sys
import os
if sys.platform == "win32":
    import pydirectinput as pag
    pag.PAUSE = 0.1
else:
    import pyautogui as pag
import time
from modules.submacros.hasteCompensation import HasteCompensationRevamped
import threading
from collections import deque


class keyboard:
    def __init__(self, walkspeed, enableHasteCompensation, hasteCompensation: HasteCompensationRevamped):
        self.ws = walkspeed
        self.enableHasteCompensation = enableHasteCompensation
        self.hasteCompensation = hasteCompensation

        self.detection_interval = 0.01
        
        #drift compensation
        self.accumulated_error = 0
        self.error_correction_factor = 0.1
    
    
    def predictiveTimeWait(self, duration):
        base_speed = 28
        target_distance = base_speed * duration
        corrected_target = target_distance - self.accumulated_error
        
        traveled_distance = 0
        start_time = time.perf_counter()
        last_time = start_time
        
        #safety distance, just in case of infinite drifting
        max_time = duration * 1.2

        #sleep_interval = 0.01  # Or even 0.02 would probably work fine
        
        while traveled_distance < corrected_target:
            current_time = time.perf_counter()
            elapsed = current_time - start_time
            
            # Safety timeout
            if elapsed >= max_time:
                break

            speed = self.getMoveSpeed()
            
            delta_t = current_time - last_time
            distance_increment = speed * delta_t
            traveled_distance += distance_increment
            
            last_time = current_time
            #time.sleep(sleep_interval)
        
        #calculate drift and update accumulated error
        distance_error = traveled_distance - target_distance
        
        #self.accumulated_error = (self.accumulated_error * 0.9 + distance_error * self.error_correction_factor)
    
    
    def walk(self, k, t, applyHaste=True, method='predictive'):
        if applyHaste and self.enableHasteCompensation:
            keyboard.keyDown(k, False)
            
            if method == 'predictive':
                self.predictiveTimeWait(t)
            else:
                self.timeWait(t)  # Original method
                
            keyboard.keyUp(k, False)
        else:
            self.press(k, t * 28 / self.ws)
    
    def multiWalk(self, keys, t, applyHaste=True, method='predictive'):
        for k in keys:
            pag.keyDown(k, _pause=False)
        
        if applyHaste and self.enableHasteCompensation:
            if method == 'predictive':
                self.predictiveTimeWait(t)
            else:
                self.timeWait(t)
        else:
            time.sleep(t * 28 / self.ws)
        
        for k in keys:
            pag.keyUp(k, _pause=False)

    @staticmethod
    #call the press function of the pag library
    def pagPress(k):
        pag.press(k)
    @staticmethod
    def keyDown(k, pause = True):
        #for some reason, the function key is sometimes held down, causing it to open the dock or enable dictation
        if sys.platform == "darwin":
            keyboard.keyUp('fn', False)
        pag.keyDown(k, _pause = pause)

    @staticmethod
    def keyUp(k, pause = True):
        pag.keyUp(k, _pause = pause)

    #pyautogui without the pause
    def press(self,key, delay = 0.02):
        keyboard.keyDown(key, False)
        time.sleep(delay)
        keyboard.keyUp(key, False)

    def write(self, text, interval = 0.1):
        pag.typewrite(text, interval)
    #pyautogui with the pause
    def slowPress(self,k):
        pag.keyDown(k)
        time.sleep(0.08)
        pag.keyUp(k)

    def getMoveSpeed(self):
        movespeed = self.hasteCompensation.getHaste()
        return movespeed
    
    def timeWaitNoHasteCompensation(self, duration):
        time.sleep(duration* 28 / self.ws)

    def timeWait(self, duration):

        baseSpeed = 28
        target_distance = baseSpeed * duration  # Total distance the player should travel
        traveledDistance = 0
        maxTime = baseSpeed/24*duration

        st = time.perf_counter()
        prevTime = st
        prevSpeed = self.getMoveSpeed()

        while traveledDistance < target_distance and prevTime-st < maxTime:
            currentTime = time.perf_counter()
            speed = self.getMoveSpeed()

            delta_t = currentTime - prevTime

            # Apply trapezoidal integration to calculate traveled distance
            traveledDistance += ((prevSpeed + speed) / 2) * delta_t

            # Update previous values
            prevTime = currentTime
            prevSpeed = speed

        elapsed_time = time.perf_counter() - st
        #print(f"current speed: {speed}, original time: {duration}, actual travel time: {elapsed_time}")

    #recreate natro's walk function
    def tileWait(self, n, hasteCap=0):
        #self.getMoveSpeed takes too fast to run
        def a():
            st = time.perf_counter()
            a = self.hasteCompensation.getHaste()
            et = time.perf_counter()
            return st, et, a
        freq = 1  # Simulated frequency constant
        d = freq / 8
        l = n * freq * 4

        s, f, v = a()
        d += v * (f - s) 

        st = time.time()
        while d < l:
            prev_v = v
            s, f, v = a()
            d += ((prev_v + v) / 2) * (f - s) 
        
    
    def tileWalk(self, key, tiles, applyHaste = True):
        if applyHaste:
            self.keyDown(key, False)
            self.tileWait(tiles)
            self.keyUp(key, False)
        else:
            self.press(key,(tiles/8.3)*28/self.haste.value)

    #release all movement keys (wasd, space)
    @staticmethod
    def releaseMovement():
        keys = ["w","a","s","d","space"]
        for k in keys:
            keyboard.keyUp(k, False)
