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
from weapons.weapons import *
from weapons.type_zero_weapons import Projectile


class TypeOneWeapon(Weapon):
    def __init__(self, w_dict):
        super().__init__(w_dict)
        self.accuracy = w_dict["accuracy"]
        self.weaponweapon_id_to_drop = w_dict["weapon_id_to_drop"]
        self.n_drops = w_dict["n_drops"]
        self.cooldown = w_dict["cooldown"]

    def get_copy(self):
        return TypeOneWeapon(self.w_dict)
    
    def get_weapons_executor(self, tank) -> Weapon_Executor:
        """
        @param x,y cordinate of tank, v0 of tank and the current turret-angle
        @return an instance of WeaponExecutor
        """
        return Airstrike(self)
    


class Airstrike(Weapon_Executor, GameObject):
    PLANNING_STAGE = 0
    EXECUTING_STAGE = 1
    """
    Airstrike consists of two phases
    1. Plan the airstrike 
    2. Airstrike being executed 
    """
    
    class Airplane(GameObject):
        HEIGHT = 200
        WIDTH = 20

        SPEED = 60

        ACCURACY_PLAY = 150
        def __init__(self, x, x_speed_direction, dropoff_x) -> None:
            super().__init__(x, Airstrike.Airplane.HEIGHT, xSpeed = Airstrike.Airplane.SPEED * x_speed_direction)
            self.dropoff_x = dropoff_x
            self.dropoff_phase = False

        def set_weapon_parameters(self, weapon_to_dropoff, n_drops : int, accuracy : float, cooldown : int):
            self.weapon_to_dropoff : Weapon = weapon_to_dropoff
            self.dropoffs = n_drops
            self.accuracy = accuracy
            self.cooldown = cooldown
            self.cooldown_count = cooldown

            self.adjust_dropoff()

    
        def adjust_dropoff(self):
            """Adjusts the dropoff-point to simulate accuracy"""
            shift_direction = 1 if random.random() > 0.5 else -1
            shift = shift_direction * random.randint(0, int((1 - self.accuracy) * Airstrike.Airplane.ACCURACY_PLAY))
            ConsolePrinter.print("dropoff shifted by : %s"%shift, print_level=ConsolePrinter.VERBOSE)

            self.dropoff_x = self.dropoff_x +  shift


        def update(self):
            super().update()
            if abs(self.x - self.dropoff_x) <= 10:
                self.dropoff_phase = True
            
            self.cooldown_count -= 1
            
            if self.dropoff_phase and self.dropoffs > 0 and self.cooldown_count <= 0:
                self.dropoffs -= 1
                GameObjectHandler.get_instance().add_gameobject(Projectile(self.x, Airstrike.Airplane.HEIGHT, xSpeed = self.xSpeed, ySpeed = 0, 
                                                                           weapon = self.weapon_to_dropoff))
                self.cooldown_count = self.cooldown


        def draw(self, win):
            rect(win, Colors.black, (self.x, self.y, Airstrike.Airplane.WIDTH, 10))



    def __init__(self, weapon):
        GameObject.__init__(self)
        Weapon_Executor.__init__(self)
        self.stage = Airstrike.PLANNING_STAGE
        self.weapon : TypeOneWeapon = weapon
        self.airplane : Airstrike.Airplane = None
        self.dropoff_weapon = WeaponsManager.get_instance().get_weapon_by_id(self.weapon.weaponweapon_id_to_drop)
        
    def projectile_iteration(self, pos) -> bool:
        if self.stage == Airstrike.PLANNING_STAGE and not pos == (-1, -1):
            #do airstrike
            self.stage = Airstrike.EXECUTING_STAGE
            planned_x, planned_y = pos
            if planned_y < Airstrike.Airplane.HEIGHT:
                planned_y = Airstrike.Airplane.HEIGHT + 50
            ConsolePrinter.print("Planned y by airplane : %i"%planned_y)
            xfall = int(Airstrike.Airplane.SPEED * math.sqrt( 2 * (planned_y - Airstrike.Airplane.HEIGHT) / Globals.GRAVITY))
            if planned_x > Globals.SCREEN_WIDTH / 2:
                self.airplane = Airstrike.Airplane(x = Globals.SCREEN_WIDTH + Airstrike.Airplane.WIDTH,
                                                   x_speed_direction = -1,
                                                   dropoff_x=planned_x + xfall)
            else:
                self.airplane = Airstrike.Airplane(x = - Airstrike.Airplane.WIDTH,
                                                   x_speed_direction= 1,
                                                   dropoff_x=planned_x - xfall)
                
            self.airplane.set_weapon_parameters(self.dropoff_weapon,
                                                n_drops=self.weapon.n_drops,
                                                accuracy=self.weapon.accuracy,
                                                cooldown = self.weapon.cooldown)
            GameObjectHandler.get_instance().add_gameobject(self.airplane)

    def update(self):
        if not self.airplane == None and self.airplane.dropoffs <= 0:
            self.hasCollided = True
            if not self.airplane.has_duration:
                self.airplane.has_duration = True
                self.airplane.duration = 200


    def draw(self, win):
        if self.stage == Airstrike.PLANNING_STAGE:
            circle(win, Colors.red, get_pos(), radius=5)

