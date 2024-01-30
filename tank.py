
from weapons import Weapon
import math
from fpsConstants import FPS
from pygame.draw import ellipse, line

from gameobject import GameObject


class TankInitValues:
    FUEL = 500
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

class Tank:
    TURRET_LENGTH = 15
    TURRET_WIDTH = 10

    WIDTH = 20
    HEIGHT = 8


    SPEED = 3*FPS.FPS

    def calculateTurretEndPos(tx, ty, angle, width : int = TURRET_WIDTH) -> tuple[int, int]:
        endPosX = int(round(tx + width/2 + Tank.TURRET_LENGTH * math.cos(angle*180/math.pi)))
        endPosY = int(round(ty + Tank.TURRET_LENGTH * math.sin(angle*180/math.pi)))
        return (endPosX, endPosY)
    

    def __init__(self, tx, ty, color, screenwidth, playerNumber):
        self.tx = tx
        self.ty = ty                        #tx and ty are the x and y position of the tank
        self.playerNumber = playerNumber    #the player placement wothin the round (when his turn is)
        self.twidth = 20                    #used for drawing the tank: width of the bottom ellipse
        self.theight = 8                    #used for drawing the tank: height of the bottom ellipse
        self.tcolor = color                 #the tanks color
        self.ySpeed = 0                     #the tanks vertical speed, only used for gravity

        self.tLp = TankInitValues.LP             #the tanks livepoints
        self.fuel = TankInitValues.FUEL          #the fuel for each round
        self.scorePoints = 0                #you can buy stuff with those, also they represent your score
        self.fuelPerMove = 5
        self.weapons = [Weapon.getSmallMissile(), Weapon.getVulcanoBomb(), Weapon.getBall(), Weapon.getBigBall()]
        self.currentWeapon = 0
        #self.weapons = ("Name", explosionRadius, amount, damage)
        #self.currentWeapon: index of current seleycted weapon
        self.turretAngle = 90   #math.sin() returns radians, NOT degrees
        #self.turretStartingPosition = (self.tx+int(self.twidth/2), self.ty)    da die x und y posiition ständig verändert wird ist diese variable irrelevant

        self.v0 = 15 * FPS.FPS
        self.v0ChangePerClick = 100
        self.v0Max = 50 * FPS.FPS
        self.maximumSlopeCrossable = 10000
        self.screen_width = screenwidth
        self.points = 0
        self.tank_graphics = TankGraphics(self.twidth, self.theight, color)


        
    def movementPossible(self, yWerte):
        #this function calculates if the slope is too high for a tank to move to
        if self.tx + Tank.SPEED > len(yWerte)-1 or self.tx + Tank.SPEED < 0:
            return False
        else:
            if yWerte[self.tx] - yWerte[self.tx+Tank.SPEED] <= self.maximumSlopeCrossable:
                return True
            else:
                return False
    
    def move(self, leftRight, yWerteTerrain):
        #leftRight is either 1 or -1 to multiply the movement
        if self.movementPossible(yWerteTerrain) and self.tx + Tank.SPEED <= self.screen_width - self.twidth and self.fuel >= self.fuelPerMove:
                self.tx +=  int(Tank.SPEED * leftRight * FPS.dt)
                self.fuel -= self.fuelPerMove
    
    def fire(self):
        self.getCurrentWeapon().decrementAmount()
        
        if not self.getCurrentWeapon().hasAmmoLeft():
            self.weapons.pop(self.currentWeapon)
    
    def getCurrentWeapon(self):
        return self.weapons[self.currentWeapon]

            
    def changeWeapon(self):
        if self.currentWeapon == len(self.weapons)-1:
            self.currentWeapon = 0
        else:
            self.currentWeapon += 1
                
        
    def resetValues(self):
        #this function is used if a new round begins, all basic values need to be resetted.
        self.tLp = TankInitValues.LP
        self.fuel = TankInitValues.FUEL
        self.turretAngle = TankInitValues.TURRET_ANGLE

    def changeV(self, n):
        if self.v0 + self.v0ChangePerClick * n < 0 or self.v0 + self.v0ChangePerClick * n > self.v0Max:
            return
        else:
            self.v0 += n * self.v0ChangePerClick

    def get_turret_end_pos(self) -> tuple[int, int]:
        """Calculates the current end-position of the turret of this tank"""
        return Tank.calculateTurretEndPos(self.tx, self.ty, self.turretAngle)
       
    def draw(self, window):
        self.tank_graphics.draw(window, self.tx, self.ty, self.get_turret_end_pos())
