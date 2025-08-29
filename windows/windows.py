import utils.utils as utils
from images.image_pool_wrapper import ImagePoolWrapper

class Window:
    def __init__(self, name, keys = None):
        self.name = name
        self.window_title = ImagePoolWrapper('windows/' + name, name)

        self.keys = keys

    def is_opened(self) -> bool:
        return utils.wait_for_img(self.window_title, period=0)
    
    def open(self) -> bool:
        if self.is_opened():
            return True

        if len(self.keys) == 0:
            utils.left_click(self.window_title)
        else:
            utils.press_keys(self.keys)

        return utils.wait_for_img(self.window_title, period=2, must_find=True)

    def close(self) -> bool:
        if not self.is_opened():
            return True

        if len(self.keys) == 0:
            utils.left_click(self.window_title)
        else:
            utils.press_keys(self.keys)

        return not utils.wait_for_img(self.window_title, period=0.1)

class StorageWindow(Window):
    def __init__(self):
        super().__init__('Storage', ('alt', 'c'))

    class Tabs:
        CurrentShip = ImagePoolWrapper('windows/Storage/CurrentShip', 'CurrentShip')
        Ore = ImagePoolWrapper('windows/Storage/Ore', 'Ore')
        Storage = ImagePoolWrapper('windows/Storage/Storage', 'Storage')
    
    FullStorage = ImagePoolWrapper('windows/Storage/FullStorage', 'FullStorage')

class AgencyWindow(Window):
    def __init__(self):
        super().__init__('Agency', ('alt', 'm'))

    class Tabs:
        ResourceGathering = ImagePoolWrapper('windows/Agency/ResourcesGathering', 'ResourceGathering')

    class Buttons:
        AsteroidBelts = ImagePoolWrapper('windows/Agency/Buttons/AsteroidBelts', 'AsteroidBelts')
        EnterWarpMode = ImagePoolWrapper('windows/Agency/Buttons/EnterWarpMode', 'EnterWarpMode')
        SetDestination = ImagePoolWrapper('windows/Agency/Buttons/SetDestination', 'SetDestination')

class DockWindow(Window):
    def __init__(self):
        super().__init__('Dock')

    class Buttons:
        ExitDock = ImagePoolWrapper('windows/Dock/ExitDock', 'ExitDock')

class ProfileWindow(Window):
    def __init__(self):
        super().__init__('Profile', ('alt', 'a'))

    class Tabs:
        Pilot = ImagePoolWrapper('windows/Profile/Pilot', 'Pilot')

        class Tabs:
            class HomeStation(ImagePoolWrapper):
                def __init__(self):
                    super().__init__('windows/Profile/HomeStation', 'HomeStation')

                class Buttons:
                    SetDestinationPoint = ImagePoolWrapper('windows/Profile/HomeStation/SetDestinationPoint', 'SetDestinationPoint')

class Windows:
    Agency = AgencyWindow()
    Storage = StorageWindow()
    Dock = DockWindow()
    Profile = ProfileWindow()
