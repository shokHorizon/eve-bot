from images.image_pool_wrapper import ImagePoolWrapper
import utils.utils as utils

from typing import List, Mapping

class Navigation:
    def __init__(self, name: str):
        self.name = name
        self.images = ImagePoolWrapper(f'navigation/{name}', name)

class Navigations:
    class Icons:
        Enemy = ImagePoolWrapper('navigation/Icons/Enemy', 'Navigation/Icons/Enemy')
        GoalGates = ImagePoolWrapper('navigation/Goal Gates', 'Goal Gates')
    class Filters:
        Aims = ImagePoolWrapper('navigation/Filters/Aims', 'Navigation/Filters/Aims')
        class Distance:
            Unsorted = Navigation('Distance')
            Asc = Navigation('Distance asc')
    class Dock:
        class Buttons:
            Exit = Navigation('Exit dock')
    class Tabs:
        GatesTabs = Navigation('Gates Filter')
        Asteroids = Navigation('Asteroids')
    class Actions:
        MakeJump = Navigation('Make Jump')
        Dock = ImagePoolWrapper('navigation/Actions/Dock', 'Dock')
        EnterWarpMode = ImagePoolWrapper('navigation/Actions/EnterWarpMode', 'EnterWarpMode')
    class Objects:
        class Resources:
            class Types:
                Pyroxeres = Navigation('Pyroxeres')
                Omber = Navigation('Omber')
                AsteroidBelt = Navigation('Asteroid belt')
