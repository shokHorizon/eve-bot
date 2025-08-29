import time
import cv2 as cv
import numpy as np
import pyautogui
import utils.utils


class Navigation:
    img = None
    parent = None
    goal_gates = None
    abyssal_trace_img = None
    activate_gates_img = None

    def __init__(self, parent: None):
        self.img = parent.img
        self.parent = parent
        self.abyssal_trace_img = cv.imread('templates/abyssal_trace.jpg', cv.IMREAD_COLOR)
        self.activate_gates_img = cv.imread('templates/activate_gates.jpg', cv.IMREAD_COLOR)

    def find_abyssal_trace(self):
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)

        result = cv.matchTemplate(screenshot_np, self.abyssal_trace_img, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        if max_val < 0.8:
            return

        return max_loc
    
    def activate_gates(self):
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)

        result = cv.matchTemplate(screenshot_np, self.activate_gates_img, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        if max_val < 0.8:
            return False

        pyautogui.moveTo(max_loc[0] + 5, max_loc[1] + 5)
        time.sleep(0.1)
        pyautogui.click(max_loc[0] + 5, max_loc[1] + 5)
        time.sleep(0.1)

    def jump_to_abyssal_trace(self):
        abyssal_trace = utils.utils.TryFindUntil(self.find_abyssal_trace, 10)

        if abyssal_trace is None:
            print('abyssal_trace is None')
            return False

        pyautogui.moveTo(abyssal_trace[0] + 5, abyssal_trace[1] + 5)
        time.sleep(0.1)
        pyautogui.rightClick(abyssal_trace[0] + 5, abyssal_trace[1] + 5)
        time.sleep(0.1)

        if not self.activate_gates():
            return False

        return True
