
from weapons import Weapon
import math
from fpsConstants import Globals
from pygame.draw import ellipse, line
from utilities import ExplosionData, DegreeCnvt
from gameobject import GameObject
import random


class TankInitValues:
    FUEL = 5000
    LP = 100
    TURRET_ANGLE = 45

class TankGraphics(GameObject):
    def __init__(self, width : int, height : int, color) -> None:
        self.turretThickness = 2
        self.turretwidth = 10
        self.turretheight = 8
        self.tcolor = color
        self.twidth = width                    #used for drawing the tank: width of the bottom ellipse
        self.theight = height                    #used for drawing the tank: height of the bottom ellipse
        pass


    
    def draw(self, window, tx, ty, turret_end_pos):
        #all pyame functions, see import
        ellipse(window, self.tcolor, (tx, ty, self.twidth, self.theight), 0)
        ellipse(window, self.tcolor, (int(tx + (self.twidth - self.turretwidth)/2), ty - self.turretheight + 5 ,self.turretwidth, self.turretheight),0)
        line(window, self.tcolor, ((tx + int(self.twidth/2), ty)), turret_end_pos, self.turretThickness)

class Tank(GameObject):
    TURRET_LENGTH = 15
    TURRET_WIDTH = 10

    WIDTH = 20
    HEIGHT = 8


    SPEED = 90

    MIN_ANGLE = 170
    MAX_ANGLE = 370

    MIN_V0 = 25
    MAX_V0 = 600
    V0CHANGE_PER_CLICK = 25

    def calculateTurretEndPos(tx, ty, angle) -> tuple[int, int]:
        angle = DegreeCnvt.degree_to_radians(angle)
        endPosX = int(round(tx + Tank.WIDTH/2 + Tank.TURRET_LENGTH * math.cos(angle)))
        endPosY = int(round(ty + Tank.TURRET_LENGTH * math.sin(angle)))
        return (endPosX, endPosY)
    

    def __init__(self, tx, ty, color, playerNumber, initial_weapons : list[Weapon]):
        super().__init__(x = tx, y = ty, affected_by_gravity=True, collision_class=Globals.CollisionClass.CLASS_TWO, affected_by_explosion=True)
        self.playerNumber = playerNumber    #the player placement wothin the round (when his turn is)
        self.twidth = 20                    #used for drawing the tank: width of the bottom ellipse
        self.theight = 8                    #used for drawing the tank: height of the bottom ellipse
        self.tcolor = color                 #the tanks color

        self.tLp = TankInitValues.LP             #the tanks livepoints
        self.fuel = TankInitValues.FUEL          #the fuel for each round
        self.scorePoints = 0                #you can buy stuff with those, also they represent your score
        self.fuelPerMove = 5
        self.weapons = initial_weapons
        self.currentWeapon = 0


        self.turretAngle = random.randint(Tank.MIN_ANGLE, Tank.MAX_ANGLE)   #math.sin() returns radians, NOT degrees
        #self.turretStartingPosition = (self.x+int(self.twidth/2), self.y)    da die x und y posiition ständig verändert wird ist diese variable irrelevant

        self.v0 = 250


        self.maximumSlopeCrossable = 10000
        self.points = 0
        self.tank_graphics = TankGraphics(self.twidth, self.theight, color)


    def adjust_turret_angle(self, adjustment : int):
        newAngle = self.turretAngle + adjustment
        if newAngle >= Tank.MIN_ANGLE and newAngle <= Tank.MAX_ANGLE:
            self.turretAngle = newAngle

            
    def get_bounding_box(self) -> tuple[int, int, int, int]:
        return GameObject.BoundingBox.create_bounding_box(self.x, self.y, self.twidth, self.theight)
    
    def explosion(self, expl : ExplosionData):
        if expl.is_in_radius(self.x, self.y) or expl.is_in_radius(self.x+Tank.WIDTH, self.y):
            self.tLp -= expl.damage

           
    def move(self, leftRight):
        #leftRight is either 1 or -1 to multiply the movement
        if self.x + Tank.SPEED <= Globals.SCREEN_WIDTH - self.twidth and self.fuel >= self.fuelPerMove:
            self.x +=  int(Tank.SPEED * leftRight * Globals.FPS.dt)
            self.fuel -= self.fuelPerMove
    
    def fire(self):
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
        self.tLp = TankInitValues.LP
        self.fuel = TankInitValues.FUEL
        self.turretAngle = TankInitValues.TURRET_ANGLE

    def changeV(self, n):
        new_v0 = self.v0 + Tank.V0CHANGE_PER_CLICK * n
        if new_v0 >= Tank.MIN_V0 or new_v0 <= Tank.V0CHANGE_PER_CLICK:
            self.v0 = new_v0
            

    def get_turret_end_pos(self) -> tuple[int, int]:
        """Calculates the current end-position of the turret of this tank"""
        return Tank.calculateTurretEndPos(self.x, self.y, self.turretAngle)
       
    def draw(self, window):
        self.tank_graphics.draw(window, self.x, self.y, self.get_turret_end_pos())
