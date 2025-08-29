import time
import cv2 as cv
import numpy as np
import pyautogui
#import pytesseract


class ActiveComponent:
    previous_time: float
    cycle_time: float = 1

    is_active: bool

    def __init__(self, name):
        self.name = name
        self.img = cv.imread('shipControl/' + name + '/disabled.png', cv.IMREAD_COLOR)
        self.img_active = cv.imread('shipControl/' + name + '/enabled.png', cv.IMREAD_COLOR)

        self.previous_time = time.time()
        self.is_active = False
        self.cycle_time = 1

    def update_status(self, found):
        if found:
            self.is_active = True
            self.previous_time = time.time()
            return
        if self.previous_time + self.cycle_time < time.time():
            self.is_active = False

class ControlComponent:
    def __init__(self, name):
        self.name = name
        self.img = cv.imread('shipControl/' + name + '/disabled.png', cv.IMREAD_COLOR)
        self.img_active = cv.imread('shipControl/' + name + '/enabled.png', cv.IMREAD_COLOR)

class StatusComponent:
    def __init__(self, name):
        self.name = name
        self.img = cv.imread('shipControl/' + name + '/disabled.png', cv.IMREAD_COLOR)
        self.img_active = cv.imread('shipControl/' + name + '/enabled.png', cv.IMREAD_COLOR)

class ShipControl:
    def __init__(self):
        self.img = cv.imread('templates/warp_status.png', cv.IMREAD_COLOR)
        self.ActiveComponents = {
            'artillery': ActiveComponent('artillery'),
            'armor_repairer': ActiveComponent('armor_repairer'),
        }
        self.ControlComponents = {
            'speed': ControlComponent('speed'),
        }
        self.StatusComponents = {
            'warp': StatusComponent('warp'),
            'armor': ControlComponent('armor'),
        }

    def find(self, screenshot):
        result = cv.matchTemplate(screenshot, self.img, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        
        if max_val < 0.8:
            return None
        
        return max_loc
    
    def move(self):
        warp = self.find()

        if warp is None:
            print('warp is None')
            return
        
        pyautogui.moveTo(warp[0], warp[1])

    
    def is_artillery_enabled(self):
        screenshot = np.array(pyautogui.screenshot(allScreens=True))
        result = cv.matchTemplate(screenshot, self.img, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        
        if max_val < 0.8:
            return False
        
        return True

    
