import time
import interfaces.shipControl as shipControl
from interfaces.navigation import Navigation
import utils.utils as utils
import commands.commands as commands
import interfaces.waypoints as waypoints

from typing import List
from chosenObject.chosenObject import ChosenObjects
from items.items import Items
from finder.finder import Finder
from shipControl.shipControl import ShipControls
from navigation.navigation import Navigations
from windows.windows import Windows


class Module:
    Commands: List[commands.Command]

    def __init__(self, name, commands):
        self.name = name
        self.Commands = commands

    def execute(self):
        for action in self.Actions:
            action()

class ModuleJsonBuilder:
    def __init__(self, name, json):
        self.name = name
        self.parse_actions(json)

    def name(self, name):
        self.name = name

    def parse_actions(self, json: dict) -> callable:
        self.Actions = []



def FSM_MINING() -> callable:
    Windows_v1.Storage.open()

    utils.left_click(Navigations.Filters.Aims)

    finder = Finder()

    finder.add_not_found_trigger(ChosenObjects.Unlock.images, FSM_FIND_ORE)
    finder.add_found_trigger(Windows.Storage.FullStorage, FSM_SET_HOME_DESTINATION)
    finder.add_found_trigger(Navigations.Icons.Enemy, FSM_NEXT_ASTEROID_BELT)

    return finder.wait_for_triggers()

def FSM_JUMP_UNTIL_HOME() -> callable:
    utils.wait_for_img_v1(Navigations_v1.GatesFilter.img, period=0.1)
    utils.left_click_v1(Navigations_v1.GatesFilter)

    while utils.wait_for_img_v1(Navigations_v1.GoalGates.img, period=1):
        utils.right_click_v1(Navigations_v1.GoalGates)
        
        utils.wait_for_img_v1(Navigations_v1.MakeJump.img, period=1)
        utils.left_click_v1(Navigations_v1.MakeJump)

        while utils.wait_for_img_v1(Navigations_v1.GoalGates.img, period=0.5):
            continue

        utils.wait_for_imgs_v1((Navigations_v1.EnterTheDock.img, Navigations_v1.GoalGates.img), period=15)
        utils.left_click_v1(Navigations_v1.EnterTheDock)

        
    utils.wait_for_img_v1(Buttons.ExitDock.img, period=60)

    return FSM_STORAGE_EMPTY_MINERALS



def FSM_SET_HOME_DESTINATION() -> callable:
    Windows.Storage.close()
    Windows_v1.Profile.open()

    utils.wait_for_img_v1(Navigations_v1.HomeStation.img, period=4)
    utils.left_click_v1(Navigations_v1.HomeStation)

    utils.wait_for_img_v1(Buttons.SetDestination.img, period=4)
    utils.left_click_v1(Buttons.SetDestination)

    Windows_v1.Profile.close()

    return FSM_JUMP_UNTIL_HOME()

def FSM_NEXT_ASTEROID_BELT() -> callable:
    utils.wait_for_img_v1(Navigations_v1.AsteroidBeltsIcon.img, period=0.1)
    utils.right_click_v1(Navigations_v1.AsteroidBeltsIcon)

    utils.wait_for_img_v1(Navigations_v1.EnterWarpModeContext.img, period=1)
    utils.left_click_v1(Navigations_v1.EnterWarpModeContext)


    utils.wait_for_img(ShipControls.Speed.Active, period=10)
    utils.wait_for_img(ShipControls.Speed.Inactive, period=50, must_find=True)

    return FSM_FIND_ORE

def FSM_FIND_ORE() -> callable:
    print('FSM_FIND_ORE')

    Windows.Storage.close()

    if not utils.wait_for_img_v1(Navigations_v1.Asteroids, period=0):
        utils.left_click_v1(Navigations_v1.Asteroids)

    if not utils.wait_for_img_v1(Navigations_v1.DistanceSorted.img, period=0, threshold=0.8):
        utils.wait_for_img_v1(Navigations_v1.Distance.img, period=0)
        utils.left_click_v1(Navigations_v1.Distance)

    utils.move_to_v1(Navigations_v1.DistanceSorted)
    utils.scrollTop()

    while not utils.wait_for_img_v1(Navigations_v1.Omber.img, period=0.1):
        if utils.wait_for_img_v1(Navigations_v1.AsteroidBeltsIcon, period=0):
            return FSM_NEXT_ASTEROID_BELT
        
        utils.scroll()
    
    utils.left_click_v1(Navigations_v1.Omber)

    FSM_ORBIT_AND_LOCK_TARGET()

    FSM_ACTIVATE_ALL_MINERS()

    return FSM_MINING

def FSM_ACTIVATE_ALL_MINERS() -> callable:
    print('FSM_ACTIVATE_ALL_MINERS')

    ShipControls.Miner.deactivate()
    time.sleep(1)
    ShipControls.Miner.deactivate()
    time.sleep(1)
    ShipControls.Miner.activate()

    return

def FSM_ORBIT_AND_LOCK_TARGET(fun: callable = FSM_ACTIVATE_ALL_MINERS) -> callable:
    print('FSM_ORBIT_AND_LOCK_TARGET')

    utils.wait_for_img(ChosenObjects.Orbit.images, period=0, threshold=0.99, must_find=True)
    utils.left_click(ChosenObjects.Orbit.images, threshold=0.99)
    while not utils.wait_for_img(ChosenObjects.Unlock.images, period=5, threshold=0.98):
        utils.wait_for_img(ChosenObjects.Lock.images, period=1, threshold=0.99)
        utils.left_click(ChosenObjects.Lock.images, threshold=0.99)

    return fun


def FSM_NAVIGATION_TO_POINT() -> callable:
    utils.wait_for_img_v1(Navigations_v1.GatesFilter.img, period=0)
    utils.left_click_v1(Navigations_v1.GatesFilter)

    while utils.wait_for_img_v1(Navigations_v1.GoalGates.img, period=1):
        utils.right_click_v1(Navigations_v1.GoalGates)
        
        utils.wait_for_img_v1(Navigations_v1.MakeJump.img, period=1)
        utils.left_click_v1(Navigations_v1.MakeJump)

        while utils.wait_for_img_v1(Navigations_v1.GoalGates.img, period=0.5):
            continue

        utils.wait_for_img_v1(Navigations_v1.GoalGates.img, period=10)

    return FSM_JUMP_TO_AGENCY_GOAL

def FSM_JUMP_TO_AGENCY_GOAL() -> callable:
    Windows.Agency.open()

    utils.wait_for_img_v1(Navigations_v1.EnterWarpMode.img, period=5)
    utils.left_click_v1(Navigations_v1.EnterWarpMode)

    Windows.Agency.close()

    utils.left_click(Navigations.Filters.Aims)

    finder = Finder()

    finder.add_found_trigger(ShipControls.Speed.Inactive, FSM_FIND_ORE)
    finder.add_found_trigger(Navigations.Icons.Enemy, FSM_SET_HOME_DESTINATION)

    return finder.wait_for_triggers()

def FSM_DOCK_EXIT() -> callable:
    utils.left_click_v1(Buttons.ExitDock)

    utils.wait_for_img_v1(Navigations_v1.GoalGates.img, period=15)

    return FSM_NAVIGATION_TO_POINT

def FSM_AGENCY_FIND_PYROXERES() -> callable:
    Windows.Agency.open()

    utils.wait_for_img(Windows.Agency.Tabs.ResourceGathering, period=10, must_find=True)
    utils.left_click(Windows.Agency.Tabs.ResourceGathering)

    utils.wait_for_img(Windows.Agency.Buttons.AsteroidBelts, period=10, must_find=True)
    utils.left_click(Windows.Agency.Buttons.AsteroidBelts, threshold=0.9)

    utils.wait_for_img(Windows.Agency.Buttons.SetDestination, period=10,  must_find=True)
    utils.left_click(Windows.Agency.Buttons.SetDestination)

    Windows.Agency.close()

    return FSM_DOCK_EXIT

def FSM_STORAGE_EMPTY_MINERALS() -> callable:
    Windows.Storage.open()

    utils.left_click(Windows.Storage.Tabs.CurrentShip)
    utils.left_click(Windows.Storage.Tabs.Ore)

    while utils.wait_for_imgs([Items.Pyroxeres.logo, Items.Omber.logo], [], period=2, threshold=0.8) is not None:
        utils.left_drag(Items.Pyroxeres.logo, Windows.Storage.Tabs.Storage, offset=20)
        utils.left_drag(Items.Omber.logo, Windows.Storage.Tabs.Storage, offset=20)

    Windows.Storage.close()

    return FSM_AGENCY_FIND_PYROXERES



    
