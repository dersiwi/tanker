import math
import random
from fpsConstants import FPS
from gameobject import GameObject
from pygame.draw import line, circle



class TerrainType:

    WOODS = 0
    DESERT = 1
    RANDOM = 2
    def __init__(self, terrain_type : int) -> None:
        self.type = terrain_type
        if terrain_type == TerrainType.RANDOM:
            self.type = random.randint(0,1)


    def get_color(self):
        if self.type == TerrainType.WOODS:
            return (0, 153, 0)  #forrest green
        if self.type == TerrainType.DESERT:
            return (219,209,180) # sand
        

    def generate_height_map(self, screen_width : int) -> list[int]:
        """
        @param screen_width -> width of the screen
        This method generates a height for each pixel on the screen
        @return a list  L of integers, such that  L[i] is the height ax pixel i
        """
        height = []
        for x in range(screen_width):
            y = int(round(30*math.sin(x/100)+175))
            height.append(y)
        return height

class Terrain(GameObject):

    WOODS = 0
    DESERT = 1
    RANDOM = 2
    def __init__(self, screenWidth, screenHeight, terrain_type : TerrainType):
        super().__init__()
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self.terrain_type = terrain_type
        self.height = self.terrain_type.generate_height_map(screenWidth)



    def explosion(self,x,r):
        #explosion takes the x koordinate of the center of the explosion and the radius of the explosion
        #The y-Value is taken off the yWertre-Liste.
        #newHeiht = explosionHeight - math.sqrt(r^2-distance from explosion^2)

        #x -= 1 muss sein, da die Liste 0-799 elemente enthält, die Pixel aber von 1-800 gezählt werden
        x -= 1
        yExplosion = self.height[x]
        if x - r > 0 and x + r < self.screenWidth:
            #calculating heights "left of the explosion"
            for xV in range(x-r, x+r):
                distance_to_center = abs(x-xV)
                self.height[xV] = int(yExplosion - round(math.sqrt(r**2 - distance_to_center**2)))

        if x + r > self.screenWidth:
            for xV in range(x-r, self.screenWidth):
                distance_to_center = abs(x-xV)
                self.height[xV] = int(yExplosion - round(math.sqrt(r**2 - distance_to_center**2)))
        if x - r < 0:
            for xV in range(0, x+r):
                distance_to_center = abs(x-xV)
                self.height[xV] = int(yExplosion - round(math.sqrt(r**2 - distance_to_center**2)))

    def draw(self, window):
        for x in range(self.screenWidth):
            line(window, self.terrain_type.get_color(), (x, self.screenHeight), (x, self.screenHeight-self.height[x]), 1)



#-------------------------------------------------------------_TERRAIN AND SUN------------------------------------

class Sun(GameObject):
    def __init__(self, screenWidth, screenHeight):
        super().__init__(x = int(screenWidth*8/10), y = int(screenHeight*3/10))

        self.screenHeight = screenHeight
        self.screenWidth = screenWidth

        self.sunColor = (252,208,70)
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

