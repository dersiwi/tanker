import pygame
import math
import random
from weapons import Weapon

class PlayerObject:
    def __init__(self, x, y, xSpeed, ySpeed):
        self.show = True
        self.x = x
        self.y = y

        self.hasSpeed = True
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
    

    
    def draw(self, window):
        pass


#------------------------------------------------------___TANK

class Tank:
    def __init__(self, tx, ty, color, screenwidth, playerNumber):
        self.tx = tx
        self.ty = ty                        #tx and ty are the x and y position of the tank
        self.playerNumber = playerNumber    #the player placement wothin the round (when his turn is)
        self.twidth = 20                    #used for drawing the tank: width of the bottom ellipse
        self.theight = 8                    #used for drawing the tank: height of the bottom ellipse
        self.tcolor = color                 #the tanks color
        self.ySpeed = 0                     #the tanks vertical speed, only used for gravity
        self.tSpeed = 5                     #the tanks speedS
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
        self.v0 = 50
        self.v0ChangePerClick = 5
        self.v0Max = 70

        self.maximumSlopeCrossable = 5

        self.screen_width = screenwidth

        
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
                self.tx +=  int(self.tSpeed * leftRight)
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
        pygame.draw.ellipse(window, self.tcolor, (self.tx,self.ty,self.twidth,self.theight), 0)
        pygame.draw.ellipse(window, self.tcolor, (int(self.tx + (self.twidth-self.turretwidth)/2), self.ty-self.turretheight+5 ,self.turretwidth,self.turretheight),0)
        pygame.draw.line(window, self.tcolor, ((self.tx+int(self.twidth/2), self.ty)), self.calculateTurretEndPos(), self.turretThickness)
    



class Projectile(PlayerObject):
    #collisionObjects are added in here, such that later on the bullet can perform collision detection on these objects as well (e.g. trees or something)
    def __init__(self, x, y, xSpeed, ySpeed, terrain, gravity, weapon, collisionObjects=None):
        super().__init__(x, y, xSpeed, ySpeed)
        self.projectileColor = (0,0,0) # black
        self.terrain = terrain  #the terrain object, which the bullet could collide with
        self.weapon = weapon    #the weapon from which the bullet was fired
        self.gravity = gravity


        self.collisionObjects = collisionObjects #for now this HAS to be all the tanks (=playerObjects), in the future this can become an abstract interface

    

    def updatePosition(self):
        self.x += self.xSpeed
        self.y -= self.ySpeed
        self.ySpeed -= self.gravity

    def getProjectilePosition(self):
        return (self.x, self.y)

    """
        Does calculations for collision detection of the bullet with other game objects
    """
    def collisionDetection(self):
        #Kollisoinskontrolle für die Kanonenkugel mit dem terrain und anderen Pnazern
        if self.x > self.terrain.screenWidth or self.x < 0:
            return True


        #kollisionskontrolle mit dem terrain
        if self.y >= self.terrain.screenHeight - self.terrain.yWerte[self.x]:
            explosionRadius = self.weapon.explosionRadius
            self.terrain.explosion(self.x, explosionRadius)

            #schadensverwaltung für panzer im umkreis der Explosion
            for Tank in self.collisionObjects:
                if Tank.tx > self.x - explosionRadius and Tank.tx < self.x + explosionRadius:
                    Tank.tLp -= int(self.weapon.damage/2)
            return True


    def draw(self, window):
        self.updatePosition()
        pygame.draw.circle(window, self.projectileColor, (self.x, self.y), 1)

#-------------------------------------------------------------_TERRAIN AND SUN------------------------------------

class Sun(PlayerObject):
    def __init__(self, screenWidth, screenHeight):
        self.sunColor = (252,208,70)
        self.sunCoordinates = (int(screenWidth*8/10), int(screenHeight*3/10))
        self.sunRadius = 50

    def draw(self, window):
        pygame.draw.circle(window, self.sunColor, self.sunCoordinates, self.sunRadius)


class Terrain:
    def __init__(self, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.yWerte = []

        #terrainColors:
        self.forest_green = (34,139,34)
        #self.sand = (76,70,50)
        self.sand = (219,209,180)
        
        self.color = self.sand      #the terrain color   

        
    def generate(self, terrainType):
        if terrainType == 3 or terrainType == 404:
            terrainType = random.randint(0,2)
        '''
        Der Plan ist es ein Terrain zu generieren, das aussieht wie x^2.
        Diese Funktion kann ja dann nach lieben vareiert werden.
        
        '''
        if terrainType == 0:
            self.color = self.forest_green
        if terrainType == 1:
            self.color = self.sand

        for x in range(self.screenWidth):
            y = int(round(30*math.sin(x/100)+175))
            self.yWerte.append(y)
        return self.yWerte



    def explosion(self,x,r):
        #explosion takes the x koordinate of the center of the explosion and the radius of the explosion
        #The y-Value is taken off the yWertre-Liste.
        #newHeiht = explosionHeight - math.sqrt(r^2-distance from explosion^2)

        #x -= 1 muss sein, da die Liste 0-799 elemente enthält, die Pixel aber von 1-800 gezählt werden
        x -= 1
        yExplosion = self.yWerte[x]
        if x - r > 0 and x + r < self.screenWidth:
            #calculating heights "left of the explosion"
            for xV in range(x-r, x+r):
                distance_to_center = abs(x-xV)
                self.yWerte[xV] = int(yExplosion - round(math.sqrt(r**2 - distance_to_center**2)))

        if x + r > self.screenWidth:
            for xV in range(x-r, self.screenWidth):
                distance_to_center = abs(x-xV)
                self.yWerte[xV] = int(yExplosion - round(math.sqrt(r**2 - distance_to_center**2)))
        if x - r < 0:
            for xV in range(0, x+r):
                distance_to_center = abs(x-xV)
                self.yWerte[xV] = int(yExplosion - round(math.sqrt(r**2 - distance_to_center**2)))

    def draw(self, window):
        if not self.yWerte:
            raise ValueError("Y-Values have not been calculated yet. Call Terrain.generate() beforehand.")

        for x in range(self.screenWidth):
            pygame.draw.line(window, self.color, (x, self.screenHeight), (x, self.screenHeight-self.yWerte[x]), 1)