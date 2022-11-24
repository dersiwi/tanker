import math
import random
from fpsConstants import FPS
from pygame.draw import line, circle

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


class Terrain:

    WOODS = 0
    DESERT = 1
    RANDOM = 2
    def __init__(self, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.yWerte = []

        #terrainColors:
        #(34, 139, 34)
        self.forest_green = (0, 153, 0)
        
        #self.sand = (76,70,50)
        self.sand = (219,209,180)
        
        self.color = self.sand      #the terrain color   
        self.explosions = []        #list of explosion objects, that have to be drawn

        
    def generate(self, terrainType):
        if terrainType == Terrain.RANDOM or terrainType == 404:
            terrainType = random.randint(0,2)
        '''
        Der Plan ist es ein Terrain zu generieren, das aussieht wie x^2.
        Diese Funktion kann ja dann nach lieben vareiert werden.
        
        '''
        if terrainType == Terrain.WOODS:
            self.color = self.forest_green
        if terrainType == Terrain.DESERT:
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
            line(window, self.color, (x, self.screenHeight), (x, self.screenHeight-self.yWerte[x]), 1)

        #draw any explosions on the terrain
        for explosion in self.explosions:
            explosion.draw(window)
            explosion.frames -= 1
            if explosion.frames <= 0:
                self.explosions.remove(explosion)


#-------------------------------------------------------------_TERRAIN AND SUN------------------------------------

class Sun(PlayerObject):
    def __init__(self, screenWidth, screenHeight):

        self.screenHeight = screenHeight
        self.screenWidth = screenWidth

        self.sunColor = (252,208,70)
        self.sunX = int(screenWidth*8/10)
        self.sunY = int(screenHeight*3/10)
        self.sunRadius = 50

        
        self.angleSpeed = 0
        self.movementRadius = int(screenWidth * 3 / 5)
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
        self.angleSpeed = (math.pi / 24) * FPS.dt

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

