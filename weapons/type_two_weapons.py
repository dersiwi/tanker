
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
from type_one_weapons import Projectile
from weapons.weapons import Weapon_Executor, Weapon, WeaponsManager

class TypeTwoWeapon(Weapon):
    def __init__(self, w_dict):
        super().__init__(w_dict)
        self.n_cluster_projectiles = w_dict["n_cluster_projectiles"]
        self.v0 = w_dict["v0"]
        self.cluster_weapon_id = w_dict["cluster_weapon_id"]

    def get_copy(self):
        return TypeTwoWeapon(self.w_dict)
    
    def get_weapons_executor(self, tank) -> Weapon_Executor:
        """
        @param x,y cordinate of tank, v0 of tank and the current turret-angle
        @return an instance of WeaponExecutor
        """
        tendpos = tank.get_turret_end_pos()
        vX, vY = Projectile.calculate_xy_speed(tank.turretAngle, tank.v0)
        return VulcanoBomb(tendpos[0], tendpos[1], vX, vY, self)


class VulcanoBomb(Projectile):

    def __init__(self, x, y, xSpeed, ySpeed, weapon):
        super().__init__(x, y, xSpeed, ySpeed, None)
        self.projectileColor = Colors.black
        self.weapon : TypeTwoWeapon = weapon    #the weapon from which the bullet was fired
        self.hasCollided = False

    
    def projectile_iteration(self, pos) -> bool:
        """
        @return True, if projectile iteration is done. False If there are still iterations to coem
        """
        return self.hasCollided
    
    def collision(self, gameobject) -> bool:
        ConsolePrinter.print("Vulcano-bomb collided with : %s"%gameobject, print_level=ConsolePrinter.VERBOSE)
        self._finish_projectile()
        for i in range(self.weapon.n_cluster_projectiles):
            xSpeed, ySpeed = Projectile.calculate_xy_speed(angle = random.randint(190,350), v0 = self.weapon.v0)
            p = Projectile(self.x, self.y - i * 5, xSpeed, ySpeed, weapon = WeaponsManager.get_instance().get_weapon_by_id(weaponid = 0)) 
            GameObjectHandler.get_instance().add_gameobject(p)