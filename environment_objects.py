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
        self.simple_height, self.slope = self.terrain_type.generate_height_map(self.screenWidth)

        self.multiple_height_lines : list[int] = []

        self.height : list[list[tuple[int, int]]] = [[] for i in range(self.screenWidth)]


    def collision(self, gameobject : GameObject) -> bool:

        """When collidinth with the terrain the terrain sets the gamobject ontop of itself and its ySpeed to zero"""
        
        bb = gameobject.get_bounding_box()
        lowest_y = gameobject.y + bb[GameObject.BoundingBox.HEIGHT]
        for i in [gameobject.x, gameobject.x + gameobject.x + bb[GameObject.BoundingBox.WIDTH]]:
            if i < 0 or i >= len(self.height):
                continue
            if i in self.multiple_height_lines:
                #do collisiont detection for multiple heights
                for (line_max, line_min) in self.height[i]:
                    if line_max > lowest_y and line_min <= lowest_y:
                        gameobject.y = line_min - bb[GameObject.BoundingBox.HEIGHT]

            else:
                gameobject.y = self.screenHeight - max(self.simple_height[gameobject.x], self.simple_height[gameobject.x + bb[GameObject.BoundingBox.WIDTH]]) - bb[GameObject.BoundingBox.HEIGHT]
        gameobject.ySpeed = 0

    def __multiple_height_collision(self, gameobject):
        raise NotImplementedError("Collsions for multiple heights not implemented yet.")
        pass
    
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
        for i in range(gameobject.x, gameobject.x + gameobject.x + bb[GameObject.BoundingBox.WIDTH]):
            if i in self.multiple_height_lines:
                #do collision detection for multiple heights
                for (line_max, line_min) in self.height[i]:
                    if line_max > lowest_y and line_min <= lowest_y:
                        return True
                return False
        
        lowest_y = gameobject.y + bb[GameObject.BoundingBox.HEIGHT]
        if lowest_y >= self.screenHeight - self.simple_height[gameobject.x] or \
            gameobject.y >= self.screenHeight - self.simple_height[gameobject.x + bb[GameObject.BoundingBox.WIDTH]]:
            return True
        return False
    
    def __collision_multiple_height_lines(self, gameobject):
        """perform a collision check if there are multiple height lines."""
        return False
        raise NotImplementedError("Collision-detection for multiple height liens not implemented yet")

        

    def explosion_funky(self, expl : ExplosionData):
        x = expl.x
        y = expl.y
        r = expl.radius
        
        for xV in range(x-r, x+r):
            if xV < 0 or xV > len(self.height):
                continue
            xV_explosion = abs(x-xV)
            yV_explosion = int(round(math.sqrt(r**2 - xV_explosion**2)))
            self.height[xV] = max(y + yV_explosion, Globals.SCREEN_HEIGHT - self.height[xV])

    def explosion(self, expl : ExplosionData):
        x = expl.x
        y = expl.y
        r = expl.radius
        
        for xV in range(x-r, x+r):
            if xV < 0 or xV > len(self.height):
                continue
            xV_explosion = abs(x-xV)
            yV_explosion = int(round(math.sqrt(r**2 - xV_explosion**2)))

            ymax = y + yV_explosion
            ymin = y - yV_explosion
            
            
            if xV in self.multiple_height_lines:
                new_lines = []
                for idx, (line_max, line_min) in enumerate(self.height[xV]):
                    if line_min > ymax:
                        new_lines.append((line_max, line_min))
                        continue

                    if ymin <= line_min and ymax >= line_max:
                        #explosion is bigger than complete line, pop it
                        continue
                    
                    if ymin >= line_min and ymax <= line_max:
                        #explision is right between a line and therefore splits it 
                        new_lines.append((line_max, ymax))
                        new_lines.append((ymin, line_min))
                        continue

                    if ymin < line_min and ymax <= line_max:
                        new_lines.append((line_max, ymax))
                        continue

                    if ymin > line_min and ymax > line_max:
                        new_lines.append((ymin, line_min))
                self.height[xV] = new_lines

            else:
                #implemented explosion for simple height, enable multiple-line splitting
                line_min = self.screenHeight - self.simple_height[xV]
                line_max = self.screenHeight
                if ymin <= line_min and ymax >= line_min:
                    self.simple_height[xV] = self.screenHeight - ymax
                if ymin >= line_min and ymax <= line_max:
                    self.multiple_height_lines.append(xV)
                    self.height[xV].append((line_max, ymax))
                    self.height[xV].append((ymin, line_min))

    def draw(self, window):
        for x, height in enumerate(self.simple_height):
            if x in self.multiple_height_lines:
                for (beginY, endY) in self.height[x]:
                    line(window, self.terrain_type.get_color(), (x, beginY), (x, endY), 1)
            else:
                line(window, self.terrain_type.get_color(), (x, self.screenHeight), (x, self.screenHeight-height), 1)


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

