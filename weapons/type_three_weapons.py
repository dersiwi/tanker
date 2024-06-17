
from utils.utilities import ConsolePrinter
from utils.core_object_utilities import TankGlobals

from weapons.type_one_weapons import Projectile
from weapons.weapons import Weapon_Executor, Weapon

class TypeThreeWeapon(Weapon):
    def __init__(self, w_dict):
        super().__init__(w_dict)
        self.tank = None

    def get_copy(self):
        return TypeThreeWeapon(self.w_dict)
    
    def get_weapons_executor(self, tank) -> Weapon_Executor:
        self.tank = tank
        tendpos = tank.get_turret_end_pos()
        vX, vY = Projectile.calculate_xy_speed(tank.turretAngle, tank.v0)
        return TeleportationGranade(tendpos[0], tendpos[1], vX, vY, self, tank)

 
class TeleportationGranade(Projectile):
    def __init__(self, x, y, xSpeed, ySpeed, weapon, tank):
        super().__init__(x, y, xSpeed, ySpeed, weapon)
        self.weapon : TypeThreeWeapon = weapon
        self.hasCollided = False
        self.tank = tank

    def projectile_iteration(self, pos) -> bool:
        """
        @return True, if projectile iteration is done. False If there are still iterations to coem
        """
        return self.hasCollided
    
    def collision(self, gameobject) -> bool:
        ConsolePrinter.print("Teleportation-granade collided with : %s"%gameobject, print_level=ConsolePrinter.VERBOSE)

        self.tank.x = self.x - int(TankGlobals.WIDTH / 2)
        self.tank.y = self.y - TankGlobals.HEIGHT - 5
        self.tank.ySpeed = 0
        self.tank.xSpeed = 0
        self._finish_projectile()
