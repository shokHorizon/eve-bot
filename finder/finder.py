from images.image_pool_wrapper import ImagePoolWrapper
import utils.utils as utils

from typing import List, Mapping


class Finder:
    Triggers : Mapping[str, callable]
    Images: List[ImagePoolWrapper]
    ImagesMustFind: List[ImagePoolWrapper]

    def __init__(self):
        self.Triggers = {}
        self.Images = []
        self.ImagesMustFind = []

    def add_found_trigger(self, imageWrapper: ImagePoolWrapper, effect: callable):
        self.Triggers[imageWrapper.name] = effect
        self.Images.append(imageWrapper)

    def add_not_found_trigger(self, imageWrapper: ImagePoolWrapper, effect: callable):
        self.Triggers[imageWrapper.name] = effect
        self.ImagesMustFind.append(imageWrapper)

    def wait_for_triggers(self, period: float, threshold: float) -> callable:
        while True:
            found_image = utils.wait_for_imgs(self.Images, self.ImagesMustFind, period=period, threshold=threshold)
                
            return self.Triggers[found_image.name]
