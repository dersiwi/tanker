import json

from gameobjects.gameobject import GameObject, GameObjectHandler
from pygame.draw import circle, rect
from pygame.mouse import get_pos
from utils.fpsConstants import Globals
from utils.utilities import Colors, DegreeCnvt, ConsolePrinter
from gameobjects.explosions import Explosion, AdvancedExplosion
from utils.core_object_utilities import TankGlobals

import math
import random
import os.path as path


PATH = path.join("data", "weapons.json")

class Weapon_Executor:
    """The weapon Executor is a parent-class for weapons like projectiles, which provides the 
    projectile_iteration interface. The projectile_iteration is called in each gameloop-iteration, after a player fires.
    As soon as self.hasCollided is set to false this class is discarded."""
    def __init__(self) -> None:
        self.hasCollided : bool = False
        """
        hasCollided tells the gameloop when the projectile is done 
        """

    def projectile_iteration(self, pos): 
        """
        When a player fires the gameloop-inputs change. In the second-stage of a players turn @see GameHandling,
        the Projectile is able to read player inputs - mousepositions to be precise.
        @param pos is the position of the mouse, if the user pressed the moues. If he didn't, pos == (-1, -1)
        """
        pass

    def draw(self, win):
        raise NotImplementedError("Do not use this class directly, initialize sublcass and implement it there.")

#----------------------weapons and weapon-classes 

class Weapon:
    TYPE_0 = 0
    TYPE_1 = 1
    TYPE_2 = 2
    TYPE_3 = 3
    TYPES : list[int]= [TYPE_0, TYPE_1, TYPE_2, TYPE_3]
    def __init__(self, w_dict):
        self.w_dict = w_dict
        self.name = w_dict["name"]
        self.weapon_id = w_dict["weapon_id"]
        self.amount = w_dict["initial_amount"]
        self.w_type = w_dict["weapon_type"]

    def get_copy(self):
        pass

    def decrementAmount(self):
        """Decrements self.amount by one"""
        self.amount -= 1

    def hasAmmoLeft(self) -> bool:
        """True, if self.amount >= 1"""
        return self.amount >= 1
    
    def get_weapons_executor(self, tank) -> Weapon_Executor:
        """
        @param tank - Tank object from which this weapon was fired 
        @return an instance of WeaponExecutor
        """
        pass

#-----------------------------weapons manager

class WeaponsManager:

    instance = None


    def get_instance():
        if WeaponsManager.instance == None:
            WeaponsManager.instance = WeaponsManager(PATH)
        return WeaponsManager.instance

    def __init__(self, path) -> None:
        with open(path, "r") as file:
            data = json.load(file)

        self.weapons : dict[int, list[Weapon]] = {}
        for w_type in Weapon.TYPES:
            self.weapons[w_type] = []
            for weapondict in data[str(w_type)]:
                if w_type == Weapon.TYPE_0:
                    self.weapons[Weapon.TYPE_0].append(TypeZeroWeapon(weapondict))
                elif w_type == Weapon.TYPE_1:
                    self.weapons[Weapon.TYPE_1].append(TypeOneWeapon(weapondict))
                elif w_type == Weapon.TYPE_2:
                    self.weapons[Weapon.TYPE_2].append(TypeTwoWeapon(weapondict))
                elif w_type == Weapon.TYPE_3:
                    self.weapons[Weapon.TYPE_3].append(TypeThreeWeapon(weapondict))
                
    def get_initial_weapons(self) -> list[Weapon]:
        """Returns a list of weapons that are initial weapons for every player. The weapons added here
        can be configured in weapons.json, where ecah weapon has an initial_amount-attribute."""
        init_weapons = []
        for w_type in self.weapons:
            for weapon in self.weapons[w_type]:
                if weapon.amount > 0:
                    init_weapons.append(weapon.get_copy())
        return init_weapons
    
    def get_weapon_by_id(self, weaponid : int) -> Weapon:
        """return a weapon given its @param weaponid."""
        for w_type in self.weapons:
            for weapon in self.weapons[w_type]:
                if weapon.weapon_id == weaponid:
                    return weapon.get_copy()
        raise ValueError("Could not find weapon with weaponid %s"%weaponid)
    



