import math
import random
from fpsConstants import Globals
from gameobject import GameObject
from pygame.draw import line, circle
from utilities import ExplosionData



class TerrainType:

    WOODS = 0
    DESERT = 1
    RANDOM = 2

    NAMES = ["Woods", "Desert", "Random"]
    IDXS = [WOODS, DESERT, RANDOM]

    def __init__(self, terrain_type : int) -> None:
        self.type = terrain_type
        if terrain_type == TerrainType.RANDOM:
            self.type = random.randint(0,1)


    def get_color(self):
        if self.type == TerrainType.WOODS:
            return (0, 153, 0)  #forrest green
        elif self.type == TerrainType.DESERT:
            return (219,209,180) # sand
        else:
            raise ValueError("Type %s does not have a color"%(self.type))
        

    def generate_height_map(self, screen_width : int) -> tuple[list[int],list[int]]:
        """
        @param screen_width -> width of the screen
        This method generates a height for each pixel on the screen
        @return two listst L, S where L[i] is the height of the terrain at pixel i and S[i] is the slope of the terrain at pixel i
        @return a list  L of integers, such that  L[i] is the height ax pixel i
        """
        height = []
        slope = []
        for x in range(screen_width):
            y = int(round(30*math.sin(x/100)+175))
            s = int(round(30*math.cos(x/100)))
            height.append(y)
            slope.append(s)
        return height, slope

class Terrain(GameObject):

    WOODS = 0
    DESERT = 1
    RANDOM = 2
    def __init__(self, terrain_type : TerrainType):
        super().__init__(collision_class=Globals.CollisionClass.CLASS_ONE, affected_by_explosion = True)
        self.screenWidth = Globals.SCREEN_WIDTH
        self.screenHeight = Globals.SCREEN_HEIGHT

        self.terrain_type = terrain_type
        self.height, self.slope = self.terrain_type.generate_height_map(self.screenWidth)


    def collision(self, gameobject : GameObject) -> bool:

        """When collidinth with the terrain the terrain sets the gamobject ontop of itself and its ySpeed to zero"""
        
        bb = gameobject.get_bounding_box()
        gameobject.y = self.screenHeight - max(self.height[gameobject.x], self.height[gameobject.x + bb[GameObject.BoundingBox.WIDTH]]) - bb[GameObject.BoundingBox.HEIGHT]
        gameobject.ySpeed = 0
    
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
        if lowest_y >= self.screenHeight - self.height[gameobject.x] or gameobject.y >= self.screenHeight - self.height[gameobject.x + bb[GameObject.BoundingBox.WIDTH]]:
            return True
        return False
        
    def explosion_funky(self, expl : ExplosionData):
        x = expl.x
        y = expl.y
        r = expl.radius
        
        for xV in range(x-r, x+r):
            if xV < 0 or xV > len(self.height):
                continue
            xV_explosion = abs(x-xV)
            yV_explosion = int(round(math.sqrt(r**2 - xV_explosion**2)))
            print("Explosion xV, xY = %s, %s"%(xV_explosion, yV_explosion))
            print("Height at xV : %i, newheight %i"%(Globals.SCREEN_HEIGHT - self.height[xV], y + yV_explosion))

            self.height[xV] = max(y + yV_explosion, Globals.SCREEN_HEIGHT - self.height[xV])
            print(self.height[xV])

    def explosion(self, expl : ExplosionData):
        x = expl.x
        y = expl.y
        r = expl.radius
        
        for xV in range(x-r, x+r):
            if xV < 0 or xV > len(self.height):
                continue
            xV_explosion = abs(x-xV)
            yV_explosion = int(round(math.sqrt(r**2 - xV_explosion**2)))
            print("Explosion xV, xY = %s, %s"%(xV_explosion, yV_explosion))
            print("Height at xV : %i, newheight %i"%(Globals.SCREEN_HEIGHT - self.height[xV], y + yV_explosion))

            self.height[xV] = Globals.SCREEN_HEIGHT - max(y + yV_explosion, Globals.SCREEN_HEIGHT - self.height[xV])
            print(self.height[xV])

    def draw(self, window):
        for x in range(self.screenWidth):
            line(window, self.terrain_type.get_color(), (x, self.screenHeight), (x, self.screenHeight-self.height[x]), 1)



#-------------------------------------------------------------_TERRAIN AND SUN------------------------------------

class Sun(GameObject):
    def __init__(self):
        super().__init__(x = int(Globals.SCREEN_WIDTH*8/10), y = int(Globals.SCREEN_HEIGHT*3/10))

        self.screenHeight = Globals.SCREEN_HEIGHT
        self.screenWidth = Globals.SCREEN_WIDTH

        self.sunColor = (252,208,70)
        self.sunRadius = 50

        self.angleSpeed = 0
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

