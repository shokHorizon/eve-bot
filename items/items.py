import utils.utils as utils
from images.image_pool_wrapper import ImagePoolWrapper

class Item:
    def __init__(self, name):
        self.name = name
        self.logo = ImagePoolWrapper('items/' + name, name)
    
class Items:
    TranquilFirestormFilament = Item('TranquilFirestormFilament')
    TranquilExoticFilament = Item('TranquilExoticFilament')
    TranquilGammaFilament = Item('TranquilGammaFilament')
    AntimatterChargeS = Item('AntimatterChargeS')
    Pyroxeres = Item('Pyroxeres')
    Omber = Item('Omber')
