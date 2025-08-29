from images.image_pool_wrapper import ImagePoolWrapper


class ChosenObject:
    def __init__(self, name):
        self.name = name
        self.images = ImagePoolWrapper('chosenObject/' + name, name)

class ChosenObjects:
    Lock = ChosenObject('Lock')
    Unlock = ChosenObject('Unlock')
    Orbit = ChosenObject('Orbit')
    Dock = ChosenObject('Dock')
