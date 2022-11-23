
from weapons import Weapon
import math

from pygame.draw import ellipse, line

class Tank:
    def __init__(self, tx, ty, color, screenwidth, playerNumber):
        self.tx = tx
        self.ty = ty                        #tx and ty are the x and y position of the tank
        self.playerNumber = playerNumber    #the player placement wothin the round (when his turn is)
        self.twidth = 20                    #used for drawing the tank: width of the bottom ellipse
        self.theight = 8                    #used for drawing the tank: height of the bottom ellipse
        self.tcolor = color                 #the tanks color
        self.ySpeed = 0                     #the tanks vertical speed, only used for gravity
        self.tSpeed = 150                     #the tanks speedS
        self.tLp = 100                      #the tanks livepoints
        self.fuel = 500                     #the fuel for each round
        self.scorePoints = 0                #you can buy stuff with those, also they represent your score
        self.fuelPerMove = 5
        self.weapons = [Weapon.getSmallMissile(), Weapon.getVulcanoBomb(), Weapon.getBall(), Weapon.getBigBall()]
        self.currentWeapon = 0
        #self.weapons = ("Name", explosionRadius, amount, damage)
        #self.currentWeapon: index of current seleycted weapon
        
        self.turretwidth = 10
        self.turretheight = 8
        self.turretAngle = 90   #math.sin() returns radians, NOT degrees
        #self.turretStartingPosition = (self.tx+int(self.twidth/2), self.ty)    da die x und y posiition ständig verändert wird ist diese variable irrelevant
        self.turretLength = 15
        self.turretThickness = 2
        self.v0 = 50*30
        self.v0ChangePerClick = 100
        self.v0Max = 70*30

        self.maximumSlopeCrossable = 100000

        self.screen_width = screenwidth

        self.dt = 1  

        
    def movementPossible(self, yWerte):
        #this function calculates if the slope is too high for a tank to move to
        if self.tx + self.tSpeed > len(yWerte)-1 or self.tx + self.tSpeed < 0:
            return False
        else:
            if yWerte[self.tx] - yWerte[self.tx+self.tSpeed] <= self.maximumSlopeCrossable:
                return True
            else:
                return False
    
    def move(self, leftRight, yWerteTerrain):
        #leftRight is either 1 or -1 to multiply the movement
        if self.movementPossible(yWerteTerrain) and self.tx + self.tSpeed <= self.screen_width - self.twidth and self.fuel >= self.fuelPerMove:
                self.tx +=  int(self.tSpeed * leftRight * self.dt)
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

    def calculateTurretEndPos(self):
        endPosX = int(round(self.tx + self.twidth/2 + self.turretLength * math.cos(self.turretAngle*180/math.pi)))
        endPosY = int(round(self.ty + self.turretLength * math.sin(self.turretAngle*180/math.pi)))
        return (endPosX, endPosY)
                
        
    def resetValues(self):
        #this function is used if a new round begins, all basic values need to be resetted.
        self.tLp = 100
        self.fuel = 200
        self.turretAngle = 45

    def changeV(self, n):
        if self.v0 + self.v0ChangePerClick * n < 0 or self.v0 + self.v0ChangePerClick * n > self.v0Max:
            return
        else:
            self.v0 += n * self.v0ChangePerClick
        
        
    def draw(self, window):
        #all pyame functions, see import
        ellipse(window, self.tcolor, (self.tx,self.ty,self.twidth,self.theight), 0)
        ellipse(window, self.tcolor, (int(self.tx + (self.twidth-self.turretwidth)/2), self.ty-self.turretheight+5 ,self.turretwidth,self.turretheight),0)
        line(window, self.tcolor, ((self.tx+int(self.twidth/2), self.ty)), self.calculateTurretEndPos(), self.turretThickness)