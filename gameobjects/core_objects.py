from gameobjects.gameobject import GameObject, GameObjectHandler
from utils.utilities import DegreeCnvt, ExplosionData, Colors, ConsolePrinter
from weapons.weapons import Weapon, Weapon_Executor
from utils.fpsConstants import Globals
from utils.core_object_utilities import TerrainType, TankGlobals, TankGraphics
from gameobjects.explosions import Explosion
from pygame.draw import circle, line


import random
import math


class Terrain(GameObject):

    """
    Gameobject terrain. For each pixel on the broad-side of the screen (so for each pixel from 0 to SCREEN_WIDTH), 
    there is a heigh associated with it. 
    This gameobject then
        1. draws a line from the bottom of the screen to the specified height
        2. detects if something collides with it and then puts it ontop of itself
        3. handles explosions when they occurr.

    """

    def __init__(self, terrain_id : int ):
        super().__init__(collision_class=Globals.CollisionClass.CLASS_ONE, affected_by_explosion = True)

        _, self.terrain_color, simple_height = TerrainType.get_instance().get_terrain(terrain_id)

        self.height : list[list[tuple[int, int]]] = []
        """
        self.height is a list of list of line-segements. For each pixel x from 0 to SCREEN_WIDTH - 1, 
        self.height[x] == [(line_max1, line_min1), (line_max2, line_min2)] where each of those 
        two tuples is a height. For each tuple; line_max > line_min.
        """
        for height in simple_height:
            self.height.append([(Globals.SCREEN_HEIGHT, Globals.SCREEN_HEIGHT - height)])

        


    def collision(self, gameobject : GameObject) -> bool:
        #When collidinth with the terrain the terrain sets the gamobject ontop of itself and its ySpeed to zero
        bb = gameobject.get_bounding_box()
        lowest_y = gameobject.y + bb[GameObject.BoundingBox.HEIGHT]
        collision_x = int(gameobject.x + bb[GameObject.BoundingBox.WIDTH] / 2)
        if collision_x < 0 or collision_x >= len(self.height):
            return

        for (line_max, line_min) in self.height[collision_x]:
            if line_max > lowest_y and line_min <= lowest_y and type(gameobject) == Tank:
                gameobject.y = line_min - bb[GameObject.BoundingBox.HEIGHT]
                falldamage = self.__calculate_falldamage(gameobject.ySpeed)
                #gameobject.tLp -= self.__calculate_falldamage()                

        gameobject.ySpeed = 0

    def __calculate_falldamage(self, ySpeed):
        #find out maximal possible ySpeed - then interpolate between min_ySpeed to get damage and a value for maximal falldamage
        falldamage = abs(int(5 / 4000 * ySpeed**2))
        if ySpeed >10:
            ConsolePrinter.print("Gameobject y-Speed : %i, resulting falldamage : %i"%(ySpeed, falldamage), print_level=ConsolePrinter.REGULAR)
        return falldamage
    
    def collision_detecetion(self, gameobject: GameObject):
        """If an object collides with the terrain, the terrain sets its ySpeed to zero 
        and its y-value such that the object sits ontop of the terrain
        There is a bug, becuase this functoin only looks at the lowest point at the left and right corner
        
        so if the object is falls ontop of the terrain like this:
            ____
            /\
        The terrain will place the object like this : /\__ (ontop of it)
        """

        bb = gameobject.get_bounding_box()
        if gameobject.x < 0 or gameobject.x + bb[GameObject.BoundingBox.WIDTH] >= len(self.height) or bb == GameObject.NO_BOUNDING_BOX:
            return False

        #check if "lowest" y-values of object are below highest value of self.height.
        lowest_y = gameobject.y + bb[GameObject.BoundingBox.HEIGHT]
        collision_x = int(gameobject.x + bb[GameObject.BoundingBox.WIDTH] / 2)
            #do collision detection for multiple heights
        for (line_max, line_min) in self.height[collision_x]:
            if line_max > lowest_y and line_min <= lowest_y:
                return True
        return False
                
    def explosion(self, expl : ExplosionData):
        x :int = expl.x
        y = expl.y
        r = expl.radius
        
        for xV in range(x-r, x+r):
            if xV < 0 or xV > len(self.height):
                continue
            xV_explosion = abs(x-xV)
            yV_explosion = int(round(math.sqrt(r**2 - xV_explosion**2)))

            ymax = y + yV_explosion
            ymin = y - yV_explosion
            
            
            new_lines = []
            for idx, (line_max, line_min) in enumerate(self.height[xV]):
                #if ymin > line_max or ymax < line_min:
                    #in this case the explosion is either below or above the height line
                #    continue


                #case 0: - explosion line completely swallows line-segemtn
                if ymin <= line_min and ymax >= line_max:                    
                    continue

                #Case 1: - explosion-line is completly within the current linesegemnt
                if ymin >= line_min and ymax <= line_max:
                    new_lines.append((line_max, ymax))
                    new_lines.append((ymin, line_min))
                    continue

                #Case 2: - explosion-line shaves off upper part of the current line-segement 
                if ymax <= line_max and ymax >= line_min: # and ymin <= line_min
                    new_lines.append((line_max, ymax))
                    continue

                #Case 3: - explosion-line shaves off lower part of current line-segment
                if line_min <= ymin and ymin <= line_max: # and ymax >= line_max
                    new_lines.append((ymin, line_min))
                    continue
                
                #caes 4 : the explosion happend above the line, in this case assert idx == len(self.height[xV]) - 1
                new_lines.append((line_max, line_min))
                
            self.height[xV] = new_lines
        

    def draw(self, window):
        for x, lines in enumerate(self.height):
            for (beginY, endY) in lines:
                line(window, self.terrain_color, (x, beginY), (x, endY), 1)

class Sun(GameObject):


    NORMAL_MOVING_SPEED = (math.pi / 24) * Globals.FPS.dt
    def __init__(self, angleSpeed : float = 0):
        """
        Sun-object is completely decorational in the background. If you set the sun to move by calling Sun.move() after initialization
        the sun moves itself by Sun.angleSpeed each iteration.
        @param angleSpeed describes the speed of the angle when it moves.
        """
        super().__init__(x = int(Globals.SCREEN_WIDTH*8/10), y = int(Globals.SCREEN_HEIGHT*3/10))

        self.screenHeight = Globals.SCREEN_HEIGHT
        self.screenWidth = Globals.SCREEN_WIDTH

        self.sunColor = (252,208,70)
        self.sunRadius = 50

        self.angleSpeed = angleSpeed
        self.movementRadius = int(Globals.SCREEN_WIDTH * 3 / 5)
        self.angle = math.pi / 4

    """
        if the sun moves, it moves in a circular motion aound the frame;

        __________________________________
        |                                 |
        |                    /            |
        |                   /             |
        |               r  /              |
        |                 /               |
        |________________/________________|
    """
    def move(self):
        self.angleSpeed = (math.pi / 24) * Globals.FPS.dt

    def updatePosition(self):
        if self.angleSpeed == 0:
            return
        self.angle += self.angleSpeed
        if self.angle > math.pi:
            self.angle = 0

    def calculatePosition(self):
        sunX = (self.screenWidth / 2) + int(math.cos(self.angle) * self.movementRadius)
        sunY = self.screenHeight - int(math.sin(self.angle) * self.movementRadius)
        return (sunX, sunY)

    def draw(self, window):
        self.updatePosition()
        circle(window, self.sunColor, self.calculatePosition(), self.sunRadius)

class Tank(GameObject):

    def calculateTurretEndPos(tx, ty, angle) -> tuple[int, int]:
        angle = DegreeCnvt.degree_to_radians(angle)
        endPosX = int(round(tx + TankGlobals.WIDTH/2 + TankGlobals.TURRET_LENGTH * math.cos(angle)))
        endPosY = int(round(ty + TankGlobals.TURRET_LENGTH * math.sin(angle)))
        return (endPosX, endPosY)
    

    def __init__(self, tx, ty, color, initial_weapons : list[Weapon]):
        super().__init__(x = tx, y = ty, affected_by_gravity=True, collision_class=Globals.CollisionClass.CLASS_TWO, affected_by_explosion=True)
        self.tcolor = color                      #the tanks color
        self.tLp = TankGlobals.TankInitValues.LP             #the tanks livepoints
        self.fuel = TankGlobals.TankInitValues.FUEL          #the fuel for each round
        self.fuelPerMove = 5
        self.weapons = initial_weapons
        self.currentWeapon = 0
        self.turretAngle = random.randint(TankGlobals.MIN_ANGLE, TankGlobals.MAX_ANGLE)  
        self.v0 = 250
        self.tank_graphics = TankGraphics(TankGlobals.WIDTH, TankGlobals.HEIGHT, color)
        #shilds
        self.shield : Shield = Shield(self)
        self.mines : int = 1

        self.removed_from_objecthandler = False


    def adjust_turret_angle(self, adjustment : int):
        """
        Adjusts turret angle in degrees
        @param adjustment is added onto current turret angle
        """
        newAngle = self.turretAngle + adjustment
        if newAngle >= TankGlobals.MIN_ANGLE and newAngle <= TankGlobals.MAX_ANGLE:
            self.turretAngle = newAngle


    def get_bounding_box(self) -> tuple[int, int, int, int]:
        return GameObject.BoundingBox.create_bounding_box(self.x, self.y, TankGlobals.WIDTH, TankGlobals.HEIGHT)
    
    def explosion(self, expl : ExplosionData):
        if expl.is_in_radius(self.x, self.y) or expl.is_in_radius(self.x + TankGlobals.WIDTH, self.y):
            if self.shield == None or not self.shield.is_active:
                self.tLp -= expl.damage
           
    def move(self, leftRight):
        #leftRight is either 1 or -1 to multiply the movement
        if self.x + TankGlobals.SPEED <= Globals.SCREEN_WIDTH - TankGlobals.WIDTH and self.fuel >= self.fuelPerMove:
            self.x +=  int(TankGlobals.SPEED * leftRight * Globals.FPS.dt)
            self.fuel -= self.fuelPerMove
    
    def fire(self):
        """Decrements the ammo of the current weaon by one. Pops weapon from self.weapons if no ammo left."""
        self.getCurrentWeapon().decrementAmount()
        if not self.getCurrentWeapon().hasAmmoLeft():
            self.weapons.pop(self.currentWeapon)
            self.changeWeapon()

    def getCurrentWeapon(self) -> Weapon:
        return self.weapons[self.currentWeapon]

            
    def changeWeapon(self):
        self.currentWeapon = (self.currentWeapon + 1) % len(self.weapons)                
        
    def resetValues(self):
        #this function is used if a new round begins, all basic values need to be resetted.
        self.tLp = TankGlobals.TankInitValues.LP
        self.fuel = TankGlobals.TankInitValues.FUEL
        self.turretAngle = TankGlobals.TankInitValues.TURRET_ANGLE

    def changeV(self, n):
        new_v0 = self.v0 + TankGlobals.V0CHANGE_PER_CLICK * n
        if new_v0 >= TankGlobals.MIN_V0 and new_v0 <= TankGlobals.MAX_V0:
            self.v0 = new_v0

    def get_turret_end_pos(self) -> tuple[int, int]:
        """Calculates the current end-position of the turret of this tank"""
        return Tank.calculateTurretEndPos(self.x, self.y, self.turretAngle)
    

    def deploy_shield(self) -> None:
        """Adds self.shield to GameObjectHandler and sets self.shield to None"""
        if not self.shield == None:
            GameObjectHandler.get_instance().add_gameobject(self.shield)
            self.shield.set_active()
            self.shield = None

    def deploy_mine(self):
        if self.mines > 0:
            GameObjectHandler.get_instance().add_gameobject(Mines(self.x, self.y))
            self.mines -= 1
            pass#
       
    def draw(self, window):
        self.tank_graphics.draw(window, self.x, self.y, self.get_turret_end_pos())

    def get_weapon_executor(self) -> Weapon_Executor:
        return self.weapons[self.currentWeapon].get_weapons_executor(self)

class Shield(GameObject):

    TOLERANCE = 10

    def __init__(self, ownertank : Tank) -> None:
        super().__init__(affected_by_explosion=True, collision_class = Globals.CollisionClass.CLASS_ONE)
        self.radius = 50
        self.ownertank : Tank = ownertank
        self.health = 100
        self.is_active = False


    def set_active(self) -> None:
        """sets self.is_active to true. Is automatically set to False once shield has no hitpoints left"""
        self.is_active = True

    def collision_detecetion(self, gameobject: GameObject):
        if type(gameobject) == Tank:
            return False
        if self.__is_inside(gameobject.x, gameobject.y) and self.__is_inside(gameobject.prev_x, gameobject.prev_y):
            return False
        return self.__is_inside(gameobject.x, gameobject.y) 
    
    def explosion(self, expl : ExplosionData):
        if abs(expl.x - self.x) <= self.radius + Shield.TOLERANCE and abs(expl.y - self.y) <= self.radius + Shield.TOLERANCE:
            ConsolePrinter.print("shield health : %s"%self.health, print_level=ConsolePrinter.REGULAR)
            self.health -= expl.damage
        
        if self.health <= 0:
            GameObjectHandler.get_instance().remove_gameobject(self)
            self.is_active = False
        
    def __is_inside(self, x, y):
        return abs(x - self.x) <= self.radius and abs(y - self.y) <= self.radius

    def collision(self, gameobject : GameObject):
        gameobject.x = gameobject.prev_x
        gameobject.y = gameobject.prev_y
        pass

    
    def update(self):
        self.x = int(self.ownertank.x + TankGlobals.WIDTH / 2)
        self.y = int(self.ownertank.y + TankGlobals.HEIGHT / 2)


    def draw(self, window):
        circle(window, (0,0, 255), (self.x, self.y), self.radius, width = 1)

class Mines(GameObject):
    COLOR_DURATION = 20
    def __init__(self, x,y) -> None:
        super().__init__(x, y, 0, 0, affected_by_explosion=True, affected_by_gravity = True, collision_class=Globals.CollisionClass.CLASS_TWO)
        self.duration_until_hot = 20

        self.colorSwitchAfter = Mines.COLOR_DURATION

        self.explosion_ = Explosion(self.x, self.y, radius = 20, damage=20)

        self.color_idx = 0
        self.colors = [Colors.black, Colors.red]


    def update(self):
        super().update()
        self.duration_until_hot -= 1
        self.colorSwitchAfter -= 1
        if self.colorSwitchAfter <= 0:
            self.color_idx = (self.color_idx + 1) % len(self.colors)
            self.colorSwitchAfter = Mines.COLOR_DURATION


    def get_bounding_box(self) -> tuple[int, int, int, int]:
        return GameObject.BoundingBox.create_bounding_box(self.x, self.y - 5, 1, 5)
    
    def collision(self, gameobject) -> bool:
        if type(gameobject) == Terrain or self.duration_until_hot > 0:
            return False
        
        self.__exploide_mine()
        
    def __exploide_mine(self):
        GameObjectHandler.get_instance().add_gameobject(self.explosion_)
        GameObjectHandler.get_instance().remove_gameobject(self)
        GameObjectHandler.get_instance().explosion(self.explosion_.get_data())

    def explosion(self, expl: ExplosionData):
        if expl.is_in_radius(self.x, self.y):
            self.__exploide_mine()

    def draw(self, window):
        circle(window, self.colors[self.color_idx], (self.x, self.y), radius = 1)

