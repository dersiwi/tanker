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
        self.weapon : TypeTwoWeapon = weapon
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
    



