from gameobject import GameObject, GameObjectHandler
from pygame.draw import circle, rect
from pygame.mouse import get_pos
from fpsConstants import Globals
from utilities import Colors, DegreeCnvt
from weapons import Weapon, TypeOneWeapon, TypeZeroWeapon, WeaponsManager, TypeTwoWeapon
from explosions import Explosion

import math
import random

class Projectile(GameObject):

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

    def __init__(self, x, y, xSpeed, ySpeed, weapon : TypeZeroWeapon):
        super().__init__(x, y, xSpeed, ySpeed, affected_by_gravity=True, collision_class=Globals.CollisionClass.CLASS_TWO)
        self.projectileColor = Colors.black
        self.weapon : TypeZeroWeapon = weapon    #the weapon from which the bullet was fired
        self.hasCollided = False

    
    def projectile_iteration(self, pos) -> bool:
        """
        @return True, if projectile iteration is done. False If there are still iterations to coem
        """
        return self.hasCollided
    
    def get_bounding_box(self) -> tuple[int, int, int, int]:
        return GameObject.BoundingBox.create_bounding_box(self.x, self.y, 1, 1)
    
    def collision(self, gameobject) -> bool:
        print("Projcetile collided with : %s"%gameobject)
        expl = Explosion(self.x, self.y, self.weapon.explosion_radius, self.weapon.damage)
        #expl = MushroomCloud(self.x, self.y, self.weapon.explosion_radius, self.weapon.damage)
        GameObjectHandler.get_instance().add_gameobject(expl)
        GameObjectHandler.get_instance().explosion(expl.get_data())
        self._finish_projectile()
        
    def getProjectilePosition(self):
        return (self.x, self.y)
    
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

    def __init__(self, x, y, xSpeed, ySpeed, weapon : TypeTwoWeapon):
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
 

class Airstrike(GameObject):
    PLANNING_STAGE = 0
    EXECUTING_STAGE = 1
    """
    Airstrike consists of two phases
    1. Plan the airstrike 
    2. Airstrike being executed 
    """

    DROPOFFS = 10

    class Airplane(GameObject):
        HEIGHT = 200
        WIDTH = 20

        SPEED = 60

        ACCURACY_PLAY = 150
        def __init__(self, x, x_speed_direction, dropoff_x) -> None:
            super().__init__(x, Airstrike.Airplane.HEIGHT, xSpeed = Airstrike.Airplane.SPEED * x_speed_direction)
            self.dropoff_x = dropoff_x
            self.dropoff_phase = False

        def set_weapon_parameters(self, weapon_to_dropoff : Weapon, n_drops : int, accuracy : float, cooldown : int):
            self.weapon_to_dropoff = weapon_to_dropoff
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



    def __init__(self, weapon : TypeOneWeapon) -> None:
        super().__init__(x=0, y=0, xSpeed=0, ySpeed=0, has_duration=False)
        self.stage = Airstrike.PLANNING_STAGE

        self.airplane : Airstrike.Airplane = None
        self.dropoff_weapon = WeaponsManager.get_instance().get_weapon_by_id(weapon.weaponweapon_id_to_drop)
        self.weapon = weapon
        self.hasCollided = False

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

