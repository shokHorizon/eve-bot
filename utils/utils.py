from typing import List
import cv2 as cv
#import keras_ocr
from PIL import ImageGrab, Image
import numpy as np
import pyautogui
import time

from images.image_pool_wrapper import ImagePoolWrapper


def TryFindUntil(f, limit):
    t = time.time()

    while time.time() - t < limit:
        res = f()

        if res is not None:
            return res
        
        time.sleep(0.1)

    return None



# Получает имя и путь к папке с изображениямии добавляет в них новое изображение от пользователя
def update_image_pool(ImageWrapper) -> bool:

    # Получение сигнала от пользователя
    key = input(f'Напишите что-либо и отправьте, чтобы добавить изображение в пул {ImageWrapper.name} из буфера обмена')
    if key == '':
        return False

    # Получение изображения из буфера обмена
    new_image = ImageGrab.grabclipboard()

    ImageWrapper.add_image(new_image)

    return True

def right_click_position(x, y):
    pyautogui.moveTo(x + 5, y + 5)
    pyautogui.rightClick(x + 5, y + 5)

def left_click(img: ImagePoolWrapper, threshold=0.95, offset = 5):
    print(f'try left click {img.name}')
    screenshot = cv.cvtColor(np.array(pyautogui.screenshot()), cv.COLOR_RGB2BGR)

    for image in img.images:
        result = cv.matchTemplate(screenshot, image, cv.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv.minMaxLoc(result)

        if max_val < threshold:
            continue
        
        pyautogui.moveTo(max_loc[0] + offset, max_loc[1] + offset)
        pyautogui.leftClick(max_loc[0] + offset, max_loc[1] + offset)
        pyautogui.moveTo(10, 10)

        return True

    print(f'img {img.name} not found')
    
    return False

def left_click_all(img: ImagePoolWrapper, threshold=0.95, offset = 5):
    print(f'try left click {img.name}')
    screenshot = cv.cvtColor(np.array(pyautogui.screenshot()), cv.COLOR_RGB2BGR)

    for image in img.images:
        result = cv.matchTemplate(screenshot, image, cv.TM_CCOEFF_NORMED)
        
        # Поиск всех совпадений
        loc = np.where(result >= threshold)
        # Вывод координат совпадений
        for pt in zip(*loc[::-1]):
            pyautogui.moveTo(pt[0] + offset, pt[1] + offset)
            pyautogui.leftClick(pt[0] + offset, pt[1] + offset)
            pyautogui.moveTo(10, 10)

    return True
    
def right_click(img: ImagePoolWrapper, threshold=0.95, offset = 5):
    print(f'try right click {img.name}')
    screenshot = cv.cvtColor(np.array(pyautogui.screenshot()), cv.COLOR_RGB2BGR)

    for image in img.images:
        result = cv.matchTemplate(screenshot, image, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        if max_val < threshold:
            continue
        
        pyautogui.moveTo(max_loc[0] + offset, max_loc[1] + offset)
        pyautogui.rightClick(max_loc[0] + offset, max_loc[1] + offset)
        pyautogui.moveTo(10, 10)

        return True

    print(f'img {img.name} not found')
    return False

def wait_for_img(image_wrapper: ImagePoolWrapper, period=None, threshold=0.95, must_find=False):
    t = time.time()

    print(f'waiting for img {image_wrapper.name}')

    while period is None or time.time() - t < period or period == 0:
        screenshot = cv.cvtColor(np.array(pyautogui.screenshot()), cv.COLOR_RGB2BGR)

        for img in image_wrapper.images:
            result = cv.matchTemplate(screenshot, img, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

            if max_val > threshold:
                return True
            
        if period == 0:
            break

    if must_find:
        if update_image_pool(image_wrapper):
            return wait_for_img(image_wrapper, period, threshold, must_find)
            
    return None

def wait_for_imgs(imgs: List[ImagePoolWrapper], imgs_must_find:List[ImagePoolWrapper], period=None, threshold=0.95) -> ImagePoolWrapper | None:
    t = time.time()

    while period is None or time.time() - t < period or period == 0:
        screenshot = cv.cvtColor(np.array(pyautogui.screenshot()), cv.COLOR_RGB2BGR)

        for imgWrapper in imgs:
            for img in imgWrapper.images:
                result = cv.matchTemplate(screenshot, img, cv.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

                if max_val > threshold:
                    return imgWrapper
                
        for imgWrapper in imgs_must_find:
            for img in imgWrapper.images:
                result = cv.matchTemplate(screenshot, img, cv.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
                
                if max_val > threshold:
                    break
            else:
                return imgWrapper
            
        if period == 0:
            return None

    return None

def left_drag(targetImage: ImagePoolWrapper, destinationImage: ImagePoolWrapper, threshold=0.95, offset = 5):
    print(f'try left drag {targetImage.name} to {destinationImage.name}')
    screenshot = cv.cvtColor(np.array(pyautogui.screenshot()), cv.COLOR_RGB2BGR)

    target_max_val = 0
    target_max_loc = None
    
    destination_max_val = 0
    destination_max_loc = None

    for target_img in targetImage.images:
        result = cv.matchTemplate(screenshot, target_img, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        if max_val > threshold:
            target_max_val = max_val
            target_max_loc = max_loc
            break
    else:
        print(f'image {targetImage.name} not found')
        return False
    
    for destination_img in destinationImage.images:
        result = cv.matchTemplate(screenshot, destination_img, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        
        if max_val > threshold:
            destination_max_val = max_val
            destination_max_loc = max_loc
            break
    else:
        print(f'image {destinationImage.name} not found')
        return False

    pyautogui.moveTo(target_max_loc[0] + offset, target_max_loc[1] + offset)
    time.sleep(0.1)
    pyautogui.mouseDown()
    pyautogui.dragTo(destination_max_loc[0] + offset, destination_max_loc[1] + offset, duration=0.5, tween=pyautogui.easeInOutQuad)
    time.sleep(0.1)
    pyautogui.mouseUp()

    return True


def move_to(images: ImagePoolWrapper, threshold=0.95, offset = 5):
    screenshot = cv.cvtColor(np.array(pyautogui.screenshot()), cv.COLOR_RGB2BGR)

    for image in images.images:
        result = cv.matchTemplate(screenshot, image, cv.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv.minMaxLoc(result)

        if max_val < threshold:
            continue
        
        pyautogui.moveTo(max_loc[0] + offset, max_loc[1] + offset)

        return True

    print(f'image {images.name} not found')
    
    return False


def move_to_v1(object, threshold=0.95, offset = 5):
    print(f'try move to {object.name}')
    screenshot = cv.cvtColor(np.array(pyautogui.screenshot()), cv.COLOR_RGB2BGR)

    result = cv.matchTemplate(screenshot, object.img, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    if max_val < threshold:
        print(f'object {object.name} not found')
        return False
    
    pyautogui.moveTo(max_loc[0] + offset, max_loc[1] + offset)

    return True

def left_click_v1(object, threshold=0.95, offset = 5):
        print(f'try left click {object.name}')
        screenshot = cv.cvtColor(np.array(pyautogui.screenshot()), cv.COLOR_RGB2BGR)
    
        result = cv.matchTemplate(screenshot, object.img, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        if max_val < threshold:
            print(f'object {object.name} not found')
            return False
        
        pyautogui.moveTo(max_loc[0] + offset, max_loc[1] + offset)
        pyautogui.leftClick(max_loc[0] + offset, max_loc[1] + offset)
        pyautogui.moveTo(10, 10)

        return True
    
def right_click_v1(object, threshold=0.95, offset = 5):
    print(f'try right click {object.name}')
    screenshot = cv.cvtColor(np.array(pyautogui.screenshot()), cv.COLOR_RGB2BGR)

    result = cv.matchTemplate(screenshot, object.img, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    if max_val < threshold:
        print(f'object {object.name} not found')
        return False
    
    pyautogui.moveTo(max_loc[0] + offset, max_loc[1] + offset)
    pyautogui.rightClick(max_loc[0] + offset, max_loc[1] + offset)
    pyautogui.moveTo(10, 10)

    return True

def left_drag_v1(target, destination, threshold=0.95, offset = 5):
    print(f'try left drag {target.name} to {destination.name}')
    screenshot = cv.cvtColor(np.array(pyautogui.screenshot()), cv.COLOR_RGB2BGR)

    target_result = cv.matchTemplate(screenshot, target.img, cv.TM_CCOEFF_NORMED)
    _, target_max_val, _, target_max_loc = cv.minMaxLoc(target_result)

    if target_max_val < threshold:
        print(f'object {target.name} not found')
        return False
    
    destination_result = cv.matchTemplate(screenshot, destination.img, cv.TM_CCOEFF_NORMED)
    _, destination_max_val, _, destination_max_loc = cv.minMaxLoc(destination_result)

    if destination_max_val < threshold:
        print(f'object {destination.name} not found')
        return False
    
    pyautogui.moveTo(target_max_loc[0] + offset, target_max_loc[1] + offset)
    time.sleep(0.1)
    pyautogui.mouseDown()
    pyautogui.moveTo(destination_max_loc[0] + offset, destination_max_loc[1] + offset)
    time.sleep(0.1)
    pyautogui.mouseUp()

    return True

def wait_for_img_v1(img, period=None, threshold=0.95):
    t = time.time()

    while period is None or time.time() - t < period:
        screenshot = cv.cvtColor(np.array(pyautogui.screenshot()), cv.COLOR_RGB2BGR)

        result = cv.matchTemplate(screenshot, img, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        if max_val > threshold:
            return True
        
        if period == 0:
            return None
        

    return None

def wait_for_imgs_v1(imgs, period=None, threshold=0.95):
    t = time.time()
    print(f'waiting for imgs')

    while period is None or time.time() - t < period:
        screenshot = cv.cvtColor(np.array(pyautogui.screenshot()), cv.COLOR_RGB2BGR)

        for img in imgs:
            result = cv.matchTemplate(screenshot, img, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

            if max_val > threshold:
                return True

        if period == 0:
            return None
            
    return None

def press_keys(keys):
    for key in keys:
        pyautogui.keyDown(key)
        time.sleep(0.1)
    for key in reversed(keys):
        pyautogui.keyUp(key)
        time.sleep(0.1)

    time.sleep(0.1)

    return True

def scrollTop():
    pyautogui.scroll(3600)

def scroll():
    pyautogui.scroll(-200)
