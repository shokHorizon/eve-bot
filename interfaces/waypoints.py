import time
import cv2 as cv
import numpy as np
import pyautogui


class Waypoints:
    img = None
    parent = None

    def __init__(self):
        self.img = cv.imread('templates/waypoints.png', cv.IMREAD_COLOR)

    def find(self):
        screenshot = np.array(pyautogui.screenshot(allScreens=True))
        
        result = cv.matchTemplate(screenshot, self.img, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        if max_val < 0.9:
            return (0, 0)

        return max_loc
    
    def next_location(self):
        loc = self.find()

        if loc == (0, 0):
            return (0, 0)

        return (loc[0] + 150, loc[1] + 10)
    