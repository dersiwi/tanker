import math
import random
from fpsConstants import Globals
from gameobject import GameObject
from pygame.draw import line, circle
from utilities import ExplosionData

import json

class TerrainType:

    RANDOM = -1

    instance = None
    def get_instance():
        if TerrainType.instance == None:
            TerrainType.instance=TerrainType()
        return TerrainType.instance

    def __init__(self) -> None:
        with open("data/terrains.json", "r") as file:
            self.data = json.load(file)
        self.terrains : list[tuple[str, tuple[int, int, int], list[int]]] = []
        for id in self.data:
            self.terrains.append(self.__load_terrain_from_datadict(int(id)))

    def get_all_terrain_names(self):
        names = []
        for terrain in self.terrains:
            names.append(terrain[0])
        return names
    
    def get_n_terrains(self) -> int:
        return len(self.terrains)
    
    def get_terrain(self, id : int):
        if id == TerrainType.RANDOM:
            id = random.randint(0, len(self.terrains) - 1)
        return self.terrains[id]
    

    def __load_terrain_from_datadict(self, id : int) -> tuple[str, tuple[int, int, int], list[int]]:
        """
        This function loads a terrain form the terrain-json file. 
        A terrain-dict consists of multiple fields;
            - color
            - name 
            - height-functions (that can be evaluated with eval()). 
                - Example of a function can be : 5 * 2.71**x - 10
            - intervals for height functions
                - an array of [a,b] where a and b are integers. The 

        """
        terr = self.data[str(id)]
        color = tuple(terr["rgb-color-value"])
        name = terr["name"]
        heightmap : list[int] = []
        functions = terr["height-functions"]
        intervals = terr["intervals"]
        assert len(functions) == len(intervals)
        curr_func = 0
        for x in range(0, Globals.SCREEN_WIDTH):
            heightmap.append(
                int(eval(functions[curr_func], {"math" : math, "x" : x}))
            )
            if x > intervals[curr_func][1]:
                curr_func += 1
        return name, color, heightmap
class Terrain(GameObject):

    def __init__(self, terrain_id : int ):
        super().__init__(collision_class=Globals.CollisionClass.CLASS_ONE, affected_by_explosion = True)
        self.screenWidth = Globals.SCREEN_WIDTH
        self.screenHeight = Globals.SCREEN_HEIGHT

        _, self.terrain_color, self.simple_height = TerrainType.get_instance().get_terrain(terrain_id)
        self.multiple_height_lines : list[int] = []

        self.height : list[list[tuple[int, int]]] = [[] for i in range(self.screenWidth)]


    def collision(self, gameobject : GameObject) -> bool:

        """When collidinth with the terrain the terrain sets the gamobject ontop of itself and its ySpeed to zero"""
        
        bb = gameobject.get_bounding_box()
        lowest_y = gameobject.y + bb[GameObject.BoundingBox.HEIGHT]
        collision_x = int(gameobject.x + bb[GameObject.BoundingBox.WIDTH] / 2)
        if collision_x < 0 or collision_x >= len(self.height):
            return
        if collision_x in self.multiple_height_lines:
                #do collisiont detection for multiple heights
            for (line_max, line_min) in self.height[collision_x]:
                if line_max > lowest_y and line_min <= lowest_y:
                    gameobject.y = line_min - bb[GameObject.BoundingBox.HEIGHT]
        else:
            gameobject.y = self.screenHeight - self.simple_height[collision_x] - bb[GameObject.BoundingBox.HEIGHT]
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
        collision_x = int(gameobject.x + bb[GameObject.BoundingBox.WIDTH] / 2)
        if collision_x in self.multiple_height_lines:
            #do collision detection for multiple heights
            for (line_max, line_min) in self.height[collision_x]:
                if line_max > lowest_y and line_min <= lowest_y:
                    return True
            return False
        
        return lowest_y >= self.screenHeight - self.simple_height[collision_x]
    
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
                    #if ymin > line_max or ymax < line_min:
                        #in this case the explosion is either below or above the height line
                    #    continue

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
                    line(window, self.terrain_color, (x, beginY), (x, endY), 1)
            else:
                line(window, self.terrain_color, (x, self.screenHeight), (x, self.screenHeight-height), 1)


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

