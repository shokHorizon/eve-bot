#import cv2 as cv
#import keras_ocr
#import numpy as np
import os
#import pytesseract
import pyautogui
import time

import interfaces.shipControl as shipControl
from interfaces.navigation import Navigation
import utils.utils as utils
import interfaces.waypoints as waypoints

from chosenObject.chosenObject import ChosenObjects
from items.items import Items, Item
from finder.finder import Finder
from shipControl.shipControl import ShipControls
from navigation.navigation import Navigations
from windows.windows import Windows


#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#keras = keras_ocr.pipeline.Pipeline()

def FSM_JUMP_UNTIL_HOME() -> callable:
    print('FSM_JUMP_UNTIL_HOME')

    utils.wait_for_img(Navigations.Tabs.GatesTabs.images, must_find=True)
    utils.left_click(Navigations.Tabs.GatesTabs.images)

    while not utils.wait_for_img(Navigations.Dock.Buttons.Exit.images, period=0):
        if utils.wait_for_img(Navigations.Icons.GoalGates, period=0):
            utils.right_click(Navigations.Icons.GoalGates)
            
            utils.wait_for_img(Navigations.Actions.MakeJump.images, period=15)
            utils.left_click(Navigations.Actions.MakeJump.images)

            continue

        if utils.wait_for_img(Navigations.Actions.Dock, period=0):
            utils.left_click(Navigations.Actions.Dock)

            continue

    return FSM_STORAGE_EMPTY_MINERALS



def FSM_SET_HOME_DESTINATION() -> callable:
    print('FSM_SET_HOME_DESTINATION')
    Windows.Storage.close()
    Windows.Profile.open()

    utils.wait_for_img(Windows.Profile.Tabs.Pilot, period=4, must_find=True)
    utils.left_click(Windows.Profile.Tabs.Pilot)

    utils.wait_for_img(Windows.Profile.Tabs.Tabs.HomeStation.Buttons.SetDestinationPoint, period=4, must_find=True)
    utils.left_click(Windows.Profile.Tabs.Tabs.HomeStation.Buttons.SetDestinationPoint)

    Windows.Profile.close()

    return FSM_JUMP_UNTIL_HOME()

def FSM_NEXT_ASTEROID_BELT() -> callable:
    print('FSM_NEXT_ASTEROID_BELT')

    utils.left_click(Navigations.Filters.Aims)

    Windows.Agency.open()
    utils.wait_for_img(Windows.Agency.Tabs.ResourceGathering, period=5, must_find=True)
    utils.left_click(Windows.Agency.Tabs.ResourceGathering)

    utils.wait_for_img(Windows.Agency.Buttons.AsteroidBelts, period=5, must_find=True)
    utils.left_click(Windows.Agency.Buttons.AsteroidBelts)

    utils.wait_for_img(Navigations.Objects.Resources.Types.AsteroidBelt.images, period=5, must_find=True)

    while True:
        if utils.wait_for_img(Navigations.Objects.Resources.Types.AsteroidBelt.images, period=0):
            utils.left_click(Navigations.Objects.Resources.Types.AsteroidBelt.images)
            if utils.wait_for_img(Windows.Agency.Buttons.EnterWarpMode, period=2):
                utils.left_click(Windows.Agency.Buttons.EnterWarpMode)
                break
            utils.scroll()

    Windows.Agency.close()

    utils.left_click(Navigations.Filters.Aims)

    finder = Finder()

    finder.add_found_trigger(ShipControls.Speed.Inactive, FSM_FIND_ORE)
    finder.add_found_trigger(Navigations.Icons.Enemy, FSM_SET_HOME_DESTINATION)

    return finder.wait_for_triggers()

def FSM_FIND_ORE() -> callable:
    print('FSM_FIND_ORE')

    utils.left_click(Navigations.Tabs.Asteroids.images)

    Windows.Storage.close()

    if utils.wait_for_img(Navigations.Tabs.Asteroids.images, period=0):
        utils.left_click(Navigations.Tabs.Asteroids.images)

    if utils.wait_for_img(Navigations.Filters.Distance.Unsorted.images, period=0):
        utils.wait_for_img(Navigations.Filters.Distance.Unsorted.images, period=0, must_find=True)
        utils.left_click(Navigations.Filters.Distance.Unsorted.images)

    utils.move_to(Navigations.Filters.Distance.Asc.images)
    utils.scrollTop()     

    start_time = time.time()
    timeout = 15

    while not utils.wait_for_imgs((Navigations.Objects.Resources.Types.Pyroxeres.images, Navigations.Objects.Resources.Types.Scordite.images), (), period=0.1):
        if time.time() - start_time > timeout:
            return FSM_NEXT_ASTEROID_BELT
        utils.scroll()
    
    if utils.wait_for_img(Navigations.Objects.Resources.Types.Veldspar.images, period=0):
        utils.left_click(Navigations.Objects.Resources.Types.Veldspar.images)
    elif not utils.wait_for_img(Navigations.Objects.Resources.Types.Pyroxeres.images, period=0):
        utils.left_click(Navigations.Objects.Resources.Types.Pyroxeres.images)
    else:
        return FSM_NEXT_ASTEROID_BELT

    FSM_ORBIT_AND_LOCK_TARGET()

    FSM_ACTIVATE_ALL_MINERS()

    return FSM_MINING

def FSM_ACTIVATE_ALL_MINERS() -> callable:
    print('FSM_ACTIVATE_ALL_MINERS')

    while utils.wait_for_img(ShipControls.Miner.Active, period=2, threshold=0.99):
        utils.left_click(ShipControls.Miner.Active, threshold=0.98)

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
        
def FSM_MINING() -> callable:
    print('FSM_MINING')

    Windows.Storage.open()

    utils.left_click(Navigations.Filters.Aims)

    finder = Finder()

    finder.add_found_trigger(Navigations.Icons.Enemy, FSM_NEXT_ASTEROID_BELT)
    finder.add_found_trigger(Windows.Storage.FullStorage, FSM_SET_HOME_DESTINATION)
    finder.add_not_found_trigger(ChosenObjects.Unlock.images, FSM_FIND_ORE)
    
    return finder.wait_for_triggers()


def FSM_NAVIGATION_TO_POINT() -> callable:
    print('FSM_NAVIGATION_TO_POINT')
    utils.wait_for_img(Navigations.Tabs.GatesTabs.images, period=10, must_find=True)
    while not utils.left_click(Navigations.Tabs.GatesTabs.images):
        continue

    while utils.wait_for_img(Navigations.Icons.GoalGates, period=5):
        utils.right_click(Navigations.Icons.GoalGates)
        
        utils.wait_for_img(Navigations.Actions.MakeJump.images, period=1, must_find=True)
        utils.left_click(Navigations.Actions.MakeJump.images)

        while utils.wait_for_img(Navigations.Icons.GoalGates, period=0):
            continue

        utils.wait_for_img(Navigations.Tabs.GatesTabs.images, period=20)

    return FSM_NEXT_ASTEROID_BELT

def FSM_DOCK_EXIT() -> callable:
    print('FSM_DOCK_EXIT')
    utils.left_click(Windows.Dock.Buttons.ExitDock)

    utils.wait_for_img(Navigations.Tabs.GatesTabs.images, period=15)

    return FSM_NAVIGATION_TO_POINT

def FSM_AGENCY_FIND_PYROXERES() -> callable:
    print('FSM_AGENCY_FIND_PYROXERES')
    Windows.Agency.open()

    utils.wait_for_img(Windows.Agency.Tabs.ResourceGathering, period=10, must_find=True)
    utils.left_click(Windows.Agency.Tabs.ResourceGathering)

    utils.wait_for_img(Windows.Agency.Buttons.AsteroidBelts, period=10, must_find=True)
    utils.left_click(Windows.Agency.Buttons.AsteroidBelts, threshold=0.9)

    utils.wait_for_img(Windows.Agency.Buttons.SetDestination, period=1)
    utils.left_click(Windows.Agency.Buttons.SetDestination)

    Windows.Agency.close()

    return FSM_DOCK_EXIT

def FSM_STORAGE_EMPTY_MINERALS() -> callable:
    print('FSM_STORAGE_EMPTY_MINERALS')
    Windows.Storage.open()

    utils.wait_for_img(Windows.Storage.Tabs.CurrentShip, period=0, must_find=True)
    utils.left_click(Windows.Storage.Tabs.CurrentShip)

    utils.wait_for_img(Windows.Storage.Tabs.Ore, period=0, must_find=True)
    utils.left_click(Windows.Storage.Tabs.Ore)

    while True:
        item_to_drag: Item = None

        if utils.wait_for_img(Items.Omber.logo, period=0):
            item_to_drag = Items.Omber
        if utils.wait_for_img(Items.Pyroxeres.logo, period=0):
            item_to_drag = Items.Pyroxeres
        if utils.wait_for_img(Items.Scordite.logo, period=0):
            item_to_drag = Items.Scordite
        if utils.wait_for_img(Items.Veldspar.logo, period=0):
            item_to_drag = Items.Veldspar

        if item_to_drag:
            utils.left_drag(item_to_drag.logo, Windows.Storage.Tabs.Storage)
            continue

        break

    Windows.Storage.close()

    return FSM_AGENCY_FIND_PYROXERES


class Engine:
    def __init__(self):
        self.Items = {
        }
        self.Actions = {
        }
        self.Locations = {
        }
        self.Buttons = {
    
        }

    def left_click_v1(self, object, threshold=0.95, offset = 5):
        return utils.left_click_v1(object, threshold, offset)
    
    def right_click_v1(self, object, threshold=0.95, offset = 5):
        return utils.right_click_v1(object, threshold, offset)
    
    def left_drag_v1(self, target, destination, threshold=0.95, offset = 5):
        return utils.left_drag(target, destination, threshold, offset)
    
    def right_click_position(self, x, y):
        return utils.right_click_position(x, y)

    def left_click_img(self, img):
        return utils.left_click_img(img)

    def wait_for_img_v1(self, img, period=None, threshold=0.95):
        return utils.wait_for_img_v1(img, period, threshold)
    
    def wait_for_imgs_v1(self, imgs, period=None, threshold=0.95):
        return utils.wait_for_imgs_v1(imgs, period, threshold)


    def in_dock(self) -> bool:
        return self.Dock.can_exit()
    
    def WarpUntilFinalGate(self):
        while True:
            loc = self.Waypoints.next_location()
            self.right_click_position(loc[0], loc[1])
            self.left_click_v1(self.Actions['JumpGates'])
            time.sleep(5)

    def jump_to_location(self, location):
        if not self.Map.is_active():
            if not self.Map.activate():
                print('Map activation failed')
        self.wait_for_img_v1(self.Map.title_img)

        self.right_click_v1(self.Locations[location])
        self.left_click_v1(self.Actions['JumpGates'])

        self.Map.activate()

    def is_ready_for_abyss(self):
        if not self.Storage.is_opened():
            self.Storage.open()
        self.left_click_v1(self.Actions['StackItems'])
        enough_ammo = self.Storage.count(self.Items['Antimatter Charge S']) >= 1000
        enough_filament = self.Storage.count(self.Items['Tranquil Gamma Filament']) >= 4

        return all((enough_ammo, enough_filament))

    def fulfill_for_abyss(self):
        if not self.Storage.is_opened():
            self.Storage.open()
        ammo_amount = self.Storage.count(self.Items['Antimatter Charge S'])
        filament_amount = self.Storage.count(self.Items['Tranquil Gamma Filament'])
        self.Storage.open()

        if not self.Market.is_opened():
            self.Market.open()
        self.Market.buy(self.Items['Antimatter Charge S'], 7000 - ammo_amount)
        self.Market.buy(self.Items['Tranquil Gamma Filament'], 3 - filament_amount)
        self.Market.close()

    def go_to_jita_dock(self):
        self.jump_to_location('Jita')
        self.wait_for_img_v1(self.Navigation.objects['Jita Trade Hub'].img)
        self.right_click_v1(self.Navigation.objects['Jita Trade Hub'])
        self.left_click_v1(self.Actions['EnterDock'])
        self.wait_for_img_v1(self.Buttons['ExitDock'].img)

    

    def go_to_abyss_place(self):
        if self.in_dock():
            self.left_click_v1(self.Actions['ExitDock'])

        self.jump_to_location('Muvolaiten')
        pyautogui.press('l')
        self.wait_for_img_v1(self.Navigation.objects['Muvolaiten point'].img)
        self.right_click_v1(self.Navigation.objects['Muvolaiten point'])
        self.left_click_v1(self.Actions['Warp'])
        self.left_click_v1(self.Buttons['Close'])
        self.wait_for_img_v1(self.ShipControl.StatusComponents['Warp'].img)

    def activate_abyss(self):
        self.left_click_img(self.ShipControl.ControlComponents['speed'].img_active)
        self.left_click_img(self.ShipControl.ControlComponents['speed'].img)

        if not self.Storage.is_opened():
            self.Storage.open()

        self.wait_for_img_v1(self.Actions['StackItems'].img)
        self.left_click_v1(self.Actions['StackItems'])

        self.wait_for_img_v1(self.Items['Tranquil Gamma Filament'].img, threshold=0.85)
        self.right_click_v1(self.Items['Tranquil Gamma Filament'], 0.8)
        if self.wait_for_img_v1(self.Actions['UseTranquilGammaFilament'].img) is None:
            raise Exception('Cannot use filament')
        self.left_click_v1(self.Actions['UseTranquilGammaFilament'])
        self.wait_for_img_v1(self.Buttons['ActivateForFleet'].img, threshold=0.95)
        self.left_click_v1(self.Buttons['ActivateForFleet'])
        self.Storage.open()
        self.Storage.open()
        self.wait_for_img_v1(self.Navigation.objects['Abyssal Trace'].img)
        self.right_click_v1(self.Navigation.objects['Abyssal Trace'])
        self.wait_for_img_v1(self.Actions['ActivateGates'].img)
        self.left_click_v1(self.Actions['ActivateGates'], threshold=0.8)
        self.wait_for_img_v1(self.Buttons['Activate'].img)
        self.left_click_v1(self.Buttons['Activate'])

        time.sleep(10)

    def kill_all_enemies(self):
        while True:
            enemies = self.wait_for_imgs_v1((self.Navigation.objects['Enemy'].img, self.Navigation.objects['Epithal'].img), period=0, threshold=0.9)
            captured_enemies = self.wait_for_imgs_v1((self.Navigation.objects['Enemy captured'].img, self.Navigation.objects['Epithal captured'].img), period=0, threshold=0.8)

            if captured_enemies:
                self.ShipControl.ActiveComponents['artillery'].update_status(self.wait_for_img_v1(self.ShipControl.ActiveComponents['artillery'].img_active, period=0))
                print('artillery', self.ShipControl.ActiveComponents['artillery'].is_active)
                if not self.ShipControl.ActiveComponents['artillery'].is_active:
                    self.left_click_v1(self.Navigation.objects['Enemy captured'], offset=10)
                    self.left_click_v1(self.Navigation.objects['Epithal captured'], offset=10)
                    self.ShipControl.ActiveComponents['artillery'].is_active = True
                    pyautogui.press('f1')
                    pyautogui.press('f2')
            elif enemies:
                self.left_click_v1(self.Navigation.objects['Enemy'], offset=10)
                self.left_click_v1(self.Navigation.objects['Epithal'], offset=10)
                pyautogui.press('ctrl')


            if self.wait_for_img_v1(self.ShipControl.StatusComponents['armor'].img, period=0) is not None:
                print('armor is damaged')
                self.ShipControl.ActiveComponents['armor_repairer'].update_status(self.wait_for_img_v1(self.ShipControl.ActiveComponents['armor_repairer'].img_active, period=0))
                print('armor_repairer', self.ShipControl.ActiveComponents['armor_repairer'].is_active)
                if not self.ShipControl.ActiveComponents['armor_repairer'].is_active:
                    self.left_click_v1(self.ShipControl.ActiveComponents['armor_repairer'], threshold=0.8, offset=10)
                    self.ShipControl.ActiveComponents['armor_repairer'].is_active = True
            elif self.ShipControl.ActiveComponents['armor_repairer'].is_active:
                self.left_click_v1(self.ShipControl.ActiveComponents['armor_repairer'], threshold=0.8, offset=10)
                self.ShipControl.ActiveComponents['armor_repairer'].is_active = False

            if not any((enemies, captured_enemies)):
                if self.ShipControl.ActiveComponents['armor_repairer'].is_active:
                    self.left_click_v1(self.ShipControl.ActiveComponents['armor_repairer'], threshold=0.8, offset=10)
                    self.ShipControl.ActiveComponents['armor_repairer'].is_active = False
                return

            

    def fight_in_abyss(self):
        print('waiting for Triglavian Bioco')
        while self.wait_for_img_v1(self.Navigation.objects['Triglavian Bioco'].img, 5) is None:
            print('not found')
            time.sleep(0.1)

        self.right_click_v1(self.Navigation.objects['Triglavian Bioco'])
        self.wait_for_img_v1(self.Actions['Goto'].img)
        self.left_click_v1(self.Actions['Goto'])

        self.kill_all_enemies()

        print('waiting for Triglavian Bioco captured')
        while self.wait_for_img_v1(self.Navigation.objects['Unlock'].img, period=0) is None:
            self.left_click_v1(self.Navigation.objects['Triglavian Bioco'])
            pyautogui.press('ctrl')
            time.sleep(0.1)
        
        print('firing at Triglavian Bioco')
        pyautogui.press('f1')

        self.wait_for_img_v1(self.Navigation.objects['Ostov Triglavian'].img)
        self.right_click_v1(self.Navigation.objects['Ostov Triglavian'])
        self.left_click_v1(self.Actions['Goto'])
        print('trying to open Ostov Triglavian')
        self.right_click_v1(self.Navigation.objects['Ostov Triglavian'], offset=10)
        self.wait_for_img_v1(self.Actions['ShowContainment'].img)
        self.left_click_v1(self.Actions['ShowContainment'])
        
        
        while not self.Storage.is_opened():
            time.sleep(1)
            

        print('take all out of Ostov Triglavian')
        self.wait_for_img_v1(self.Actions['TakeAll'].img)
        self.left_click_v1(self.Actions['TakeAll'])


        print('go to the final gate')
        self.right_click_v1(self.Navigation.objects['Gates'])
        self.wait_for_img_v1(self.Actions['ActivateGates'].img)
        self.left_click_v1(self.Actions['ActivateGates'])

        self.Storage.open()
        self.Storage.open()

        self.right_click_v1(self.ShipControl.ActiveComponents['artillery'], offset=25)
        self.left_click_v1(self.Actions['ReloadAllModules'], threshold=0.8)

        print('waiting for Triglavian Bioco')
        while self.wait_for_img_v1(self.Navigation.objects['Gates'].img, period=5) is not None:
            time.sleep(1)

        time.sleep(10)

    def go_to_home_dock(self):
        # self.Profile.activate()
        # self.left_click_v1(self.Navigation.objects['Home station'])
        
        # self.wait_for_img_v1(self.Buttons['SetDestination'].img)
        # self.left_click_v1(self.Buttons['SetDestination'])

        # self.Profile.deactivate()

        # self.right_click_v1(self.Locations['Jita'], 0.7)
        # self.left_click_v1(self.Actions['UseGates'])

        utils.wait_for_img_v1(Navigations.EnterTheDock.img, 60, 0.8)
        self.left_click_v1(Navigations.EnterTheDock)

        self.wait_for_img_v1(Navigations.ExitTheDock, 120, 0.8)

    def prepare_for_mining(self):
        fun = FSM_STORAGE_EMPTY_MINERALS

        while fun is not None:
            fun = fun()


def LaunchFilamentScenario():
    engine = Engine()
    
    while True:
        
        while engine.wait_for_img_v1(engine.Navigation.objects['Triglavian Bioco'].img, period=0, threshold=0.8) is not None:
            engine.fight_in_abyss()
        if not engine.is_ready_for_abyss():
            engine.go_to_jita_dock()
            engine.fulfill_for_abyss()
            engine.go_to_abyss_place()
        engine.activate_abyss()

def LaunchMineScenario():
    engine = Engine()

    while True:
        #engine.go_to_home_dock()
        engine.prepare_for_mining()

def main():
    #LaunchFilamentScenario()
    LaunchMineScenario()

main()


