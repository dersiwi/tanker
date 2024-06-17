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





PATH = path.join("data", "weapons.json")



class TypeZeroWeapon(Weapon):
    def __init__(self, w_dict):
        super().__init__(w_dict)
        self.damage = w_dict["damage"]
        self.explosion_radius = w_dict["explosion_radius"]

    def get_copy(self):
        return TypeZeroWeapon(self.w_dict)

    def get_weapons_executor(self, tank) -> Weapon_Executor:
        """
        @param x,y cordinate of tank, v0 of tank and the current turret-angle
        @return an instance of WeaponExecutor
        """
        tendpos = tank.get_turret_end_pos()
        vX, vY = Projectile.calculate_xy_speed(tank.turretAngle, tank.v0)
        return Projectile(tendpos[0], tendpos[1], vX, vY, self)

class Projectile(GameObject, Weapon_Executor):

    @staticmethod
    def calculate_xy_speed(angle : float, v0 : float) -> tuple[float, float]:
        """
        Calculates vX and vY components of the vector given an anlge in degrees and a force v0 

          /       |
         / angle  | vX
        /         |
        ---------->
            vY
        @return vX, vY
        """
        angle = DegreeCnvt.degree_to_radians(angle)

        vY = v0 * math.sin(angle)
        vX = v0 * math.cos(angle)
        ConsolePrinter.print("Calculated vX = %.2f, vY = %.2f for projectile"%(vX, vY), print_level= ConsolePrinter.VERBOSE)
        return vX, vY

    def __init__(self, x, y, xSpeed, ySpeed, weapon):
        GameObject.__init__(self, x, y, xSpeed, ySpeed, affected_by_gravity=True, collision_class=Globals.CollisionClass.CLASS_TWO)
        Weapon_Executor.__init__(self)
        #super().__init__()
        self.projectileColor = Colors.black
        self.weapon : TypeZeroWeapon = weapon    #the weapon from which the bullet was fired

    
    def get_bounding_box(self) -> tuple[int, int, int, int]:
        return GameObject.BoundingBox.create_bounding_box(self.x, self.y, 1, 1)
    
    def collision(self, gameobject) -> bool:
        ConsolePrinter.print("Projcetile collided with : %s"%gameobject, print_level=ConsolePrinter.VERBOSE)
        expl = Explosion(self.x, self.y, self.weapon.explosion_radius, self.weapon.damage)
        #expl = MushroomCloud(self.x, self.y, self.weapon.explosion_radius, self.weapon.damage)
        GameObjectHandler.get_instance().add_gameobject(expl)
        GameObjectHandler.get_instance().explosion(expl.get_data())
        self._finish_projectile()
        
    
    def _finish_projectile(self):
        GameObjectHandler.get_instance().remove_gameobject(self)
        self.hasCollided = True

    def update(self):
        super().update()
        if self.x < 0 or self.x > Globals.SCREEN_WIDTH:
            self._finish_projectile()


    def draw(self, window):
        if not self.hasCollided:
            circle(window, self.projectileColor, (self.x, self.y), 1)   #pygame function, see import

 