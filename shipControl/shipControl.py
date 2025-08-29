import utils.utils as utils
from images.image_pool_wrapper import ImagePoolWrapper

class ShipControl:
    def __init__(self, name, keys = None):
        self.name = name
        self.Active = ImagePoolWrapper('shipControl/' + name + '/active', name)
        self.Inactive = ImagePoolWrapper('shipControl/' + name + '/inactive', name)

        self.keys = keys

    def is_active(self):
        return utils.wait_for_img(self.Active, period=1)
    
    def is_inactive(self):
        return utils.wait_for_img(self.Inactive, period=1)
    
    def activate(self):
        utils.left_click_all(self.Inactive)
    
    def deactivate(self):
        if utils.wait_for_img(self.Active, period=2):
            utils.left_click(self.Active)
        

class ShipControls:
    Speed = ShipControl('Speed')
    Miner = ShipControl('Miner')
