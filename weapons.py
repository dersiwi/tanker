import json

from gameobject import GameObject, GameObjectHandler
from pygame.draw import circle, rect
from pygame.mouse import get_pos
from fpsConstants import Globals
from utilities import Colors, DegreeCnvt
from explosions import Explosion, AdvancedExplosion

import math
import random


PATH = "data\\weapons.json"

class Weapon_Executor:
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
        print(vX, vY)
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
        print("Projcetile collided with : %s"%gameobject)
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
    
    def get_bounding_box(self) -> tuple[int, int, int, int]:
        return GameObject.BoundingBox.create_bounding_box(self.x, self.y, 1, 1)
    
    def collision(self, gameobject) -> bool:
        print("Vulcano-bomb collided with : %s"%gameobject)
        self._finish_projectile()
        for i in range(self.weapon.n_cluster_projectiles):
            xSpeed, ySpeed = Projectile.calculate_xy_speed(angle = random.randint(190,350), v0 = self.weapon.v0)
            p = Projectile(self.x, self.y - i * 5, xSpeed, ySpeed, weapon = WeaponsManager.get_instance().get_weapon_by_id(weaponid = 0)) 
            GameObjectHandler.get_instance().add_gameobject(p)
 
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
            print("dropoff shifted by : %s"%shift)
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
            print("Planned_y %i"%planned_y)
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
           #print("Air plane done, duration left : %i"%self.airplane.duration)


    def draw(self, win):
        if self.stage == Airstrike.PLANNING_STAGE:
            circle(win, Colors.red, get_pos(), radius=5)


class Weapon:
    TYPE_0 = 0
    TYPE_1 = 1
    TYPE_2 = 2
    TYPES : list[int]= [TYPE_0, TYPE_1, TYPE_2]
    def __init__(self, name, weapon_id, w_type, amount):
        self.name = name
        self.weapon_id = weapon_id
        self.amount = amount
        self.w_type = w_type

    def get_copy(self):
        pass

    def decrementAmount(self):
        self.amount -= 1

    def hasAmmoLeft(self):
        return self.amount >= 1
    
    def get_weapons_executor(self, tpos : tuple[int, int] = (-1, -1), tendpos : tuple[int, int] = (-1, -1), tankv0 : float = 0, tankAngle : float = 0) -> Weapon_Executor:
        """
        @param x,y cordinate of tank, v0 of tank and the current turret-angle
        @return an instance of WeaponExecutor
        """
        pass

class TypeZeroWeapon(Weapon):
    def __init__(self, name, weapon_id, w_type, damage, amount, explosion_radius):
        super().__init__(name, weapon_id, w_type, amount)
        self.damage = damage
        self.explosion_radius = explosion_radius

    def get_copy(self):
        return TypeZeroWeapon(self.name, self.weapon_id, self.w_type, self.damage, self.amount, self.explosion_radius)

    def get_weapons_executor(self, tpos : tuple[int, int] = (-1, -1), 
                             tendpos : tuple[int, int] = (-1, -1), 
                             tankv0 : float = 0, 
                             tankAngle : float = 0) -> Weapon_Executor:
        """
        @param x,y cordinate of tank, v0 of tank and the current turret-angle
        @return an instance of WeaponExecutor
        """
        vX, vY = Projectile.calculate_xy_speed(tankAngle, tankv0)
        print("Projectile : %s, %s, %s, %s, tpos = %s, %s"%(tendpos[0], tendpos[1], vX, vY, tpos[0], tpos[1]))
        return Projectile(tendpos[0], tendpos[1], vX, vY, self)

class TypeOneWeapon(Weapon):
    def __init__(self, name, weapon_id, w_type, amount, accuracy, weaponweapon_id_to_drop, n_drops, cooldown):
        super().__init__(name, weapon_id, w_type, amount)
        self.accuracy = accuracy
        self.weaponweapon_id_to_drop = weaponweapon_id_to_drop
        self.n_drops = n_drops
        self.cooldown = cooldown

    def get_copy(self):
        return TypeOneWeapon(self.name, self.weapon_id, self.w_type, self.amount, self.accuracy, self.weaponweapon_id_to_drop, self.n_drops, self.cooldown)
    
    def get_weapons_executor(self, tpos : tuple[int, int] = (-1, -1), tendpos : tuple[int, int] = (-1, -1), tankv0 : float = 0, tankAngle : float = 0) -> Weapon_Executor:
        """
        @param x,y cordinate of tank, v0 of tank and the current turret-angle
        @return an instance of WeaponExecutor
        """
        return Airstrike(self)


class TypeTwoWeapon(Weapon):
    def __init__(self, name, weapon_id, w_type, amount, n_cluster_projectiles, v0, cluster_weapon_id):
        super().__init__(name, weapon_id, w_type, amount)
        self.n_cluster_projectiles = n_cluster_projectiles
        self.v0 = v0
        self.cluster_weapon_id = cluster_weapon_id

    def get_copy(self):
        return TypeTwoWeapon(self.name, self.weapon_id, self.w_type, self.amount, self.n_cluster_projectiles, self.v0, self.cluster_weapon_id)
    
    def get_weapons_executor(self, tpos : tuple[int, int] = (-1, -1), tendpos : tuple[int, int] = (-1, -1), tankv0 : float = 0, tankAngle : float = 0) -> Weapon_Executor:
        """
        @param x,y cordinate of tank, v0 of tank and the current turret-angle
        @return an instance of WeaponExecutor
        """
        vX, vY = Projectile.calculate_xy_speed(tankAngle, tankv0)
        return VulcanoBomb(tendpos[0], tendpos[1], vX, vY, self)
    

class WeaponsManager:

    instance = None


    def get_instance():
        if WeaponsManager.instance == None:
            WeaponsManager.instance = WeaponsManager(PATH)
        return WeaponsManager.instance

    def __init__(self, path) -> None:
        with open(path, "r") as file:
            data = json.load(file)

        self.weapons : dict[int, list[Weapon]] = {Weapon.TYPE_0 : [],
                                                  Weapon.TYPE_1 : [],
                                                  Weapon.TYPE_2 : []}
    
        for typezero in data[str(Weapon.TYPE_0)]:
            self.weapons[Weapon.TYPE_0].append(TypeZeroWeapon(name = typezero["name"],
                                                        weapon_id = typezero["weapon_id"],
                                                        w_type = typezero["weapon_type"],
                                                       damage = typezero["damage"],
                                                       amount = typezero["initial_amount"],
                                                       explosion_radius = typezero["explosion_radius"]))
        for typezero in data[str(Weapon.TYPE_1)]:
            self.weapons[Weapon.TYPE_1].append(TypeOneWeapon(name = typezero["name"],
                                            amount = typezero["initial_amount"],
                                            weapon_id = typezero["weapon_id"],
                                            w_type = typezero["weapon_type"],
                                            accuracy=typezero["accuracy"],
                                            weaponweapon_id_to_drop=typezero["weapon_id_to_drop"],
                                            n_drops=typezero["n_drops"],
                                            cooldown=typezero["cooldown"]))

        for typetwo in data[str(Weapon.TYPE_2)]:
            self.weapons[Weapon.TYPE_2].append(TypeTwoWeapon(name = typetwo["name"],
                                            amount = typetwo["initial_amount"],
                                            weapon_id = typetwo["weapon_id"],
                                            w_type = typetwo["weapon_type"],
                                            n_cluster_projectiles=typetwo["n_cluster_projectiles"],
                                            v0 = typetwo["v0"],
                                            cluster_weapon_id=typetwo["cluster_weapon_id"]))
            
    def get_initial_weapons(self) -> list[Weapon]:
        init_weapons = []
        for w_type in self.weapons:
            for weapon in self.weapons[w_type]:
                if weapon.amount > 0:
                    init_weapons.append(weapon.get_copy())
        return init_weapons
    
    def get_weapon_by_id(self, weaponid : int) -> Weapon:
        for w_type in self.weapons:
            for weapon in self.weapons[w_type]:
                if weapon.weapon_id == weaponid:
                    return weapon.get_copy()
        raise ValueError("Could not find weapon with weaponid %s"%weaponid)
    



