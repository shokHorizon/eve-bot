import utils.utils as utils
from typing import List
from finder.finder import Finder
from images.image_pool_wrapper import ImagePoolWrapper

class Command:
    fun: callable
    args: tuple
    kwargs: dict
    name: str

    def __init__(self):
        return NotImplemented
    
    def execute(self):
        return self.fun(*self.args, **self.kwargs)
    

class CommandLeftClick(Command):
    name = 'left_click'
    fun = utils.left_click

    def __init__(self, img: ImagePoolWrapper, threshold=0.95, offset=5):
        self.args = (img)
        self.kwargs = {'threshold': threshold, 'offset': offset}
    
class CommandRightClickAll(Command):
    name = 'right_click_all'
    fun = utils.left_click_all

    def __init__(self, img: ImagePoolWrapper, threshold=0.95, offset=5):
        self.args = (img)
        self.kwargs = {'threshold': threshold, 'offset': offset}

    
class CommandRightClick(Command):
    name = 'right_click'
    fun = utils.right_click

    def __init__(self, img: ImagePoolWrapper, threshold=0.95, offset=5):
        self.args = (img)
        self.kwargs = {'threshold': threshold, 'offset': offset}
    
class CommandWaitForImg(Command):
    name = 'wait_for_img'
    fun = utils.wait_for_img

    def __init__(self, img: ImagePoolWrapper, period=None, threshold=0.95, must_find=False):
        self.args = (img)
        self.kwargs = {'period': period, 'threshold': threshold, 'must_find': must_find}

class CommandWaitForImgs(Command):
    name = 'wait_for_imgs'
    fun = utils.wait_for_imgs

    def __init__(self, imgs: List[ImagePoolWrapper], imgs_must_find:List[ImagePoolWrapper], period=None, threshold=0.95):
        self.args = (imgs, imgs_must_find)
        self.kwargs = {'period': period, 'threshold': threshold}
    
class CommandLeftDrag(Command):
    name = 'left_drag'
    fun = utils.left_drag

    def __init__(self, targetImage: ImagePoolWrapper, destinationImage: ImagePoolWrapper, threshold=0.95, offset=5):
        self.args = (targetImage, destinationImage)
        self.kwargs = {'threshold': threshold, 'offset': offset}
    
class CommandPressKeys(Command):
    name = 'press_keys'
    fun = utils.press_keys

    def __init__(self, keys: List[str]):
        self.args = (keys)
        self.kwargs = {}
    
class CommandScrollTop(Command):
    name = 'scroll_top'
    fun = utils.scroll_top

    def __init__(self):
        self.args = ()
        self.kwargs = {}
    
class CommandScrollBottom(Command):
    name = 'scroll_bottom'
    fun = utils.scroll_bottom

    def __init__(self):
        self.args = ()
        self.kwargs = {}

class CommandWhile(Command):
    name = 'while'
    condition: callable
    commands: List[Command]

    def __init__(self, condition: callable, commands: List[Command]):
        self.args = (condition, commands)
        self.kwargs = {}

    def execute(self):
        while self.condition():
            for command in self.commands:
                command.execute()

class CommandFinder(Command):
    name = 'finder'
    finder: Finder

    def __init__(self):
        self.finder = Finder()
        self.fun = self.finder.wait_for_triggers

    def add_found_trigger(self, imageWrapper: ImagePoolWrapper, effect: callable):
        self.fun.add_found_trigger(imageWrapper, effect)

    def add_not_found_trigger(self, imageWrapper: ImagePoolWrapper, effect: callable):
        self.fun.add_not_found_trigger(imageWrapper, effect)

    def execute(self):
        self.wait_for_triggers()
