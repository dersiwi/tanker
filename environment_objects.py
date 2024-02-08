import math
import random
from tank import Tank
from fpsConstants import Globals
from gameobject import GameObject
from pygame.draw import line, circle
from utilities import ExplosionData

import json

class TerrainType:

    """
    This class is a singleton pattern and the only instance of this class loads the perisitently store terrains and makes them
    accessible.
    """

    TERRAIN_PATH = "data/terrains.json"

    RANDOM = -1

    instance = None
    def get_instance():
        """Singleton-pattern. Instead of constructor call this method, returns the only instance of this class."""
        if TerrainType.instance == None:
            TerrainType.instance=TerrainType()
        return TerrainType.instance

    def __init__(self) -> None:
        with open(TerrainType.TERRAIN_PATH, "r") as file:
            self.data = json.load(file)
        self.terrains : list[tuple[str, tuple[int, int, int], list[int]]] = []
        for id in self.data:
            self.terrains.append(self.__load_terrain_from_datadict(int(id)))

    def get_all_terrain_names(self) -> list[str]:
        """
        @return all the names of the terrains 
        """
        names = []
        for terrain in self.terrains:
            names.append(terrain[0])
        return names
    
    def get_n_terrains(self) -> int:
        return len(self.terrains)
    
    def get_terrain(self, id : int) -> tuple[str, tuple[int, int, int], list[int]]:
        """
        @return a triple of name, color and a height_map.
        The height map is a list of integers that for each pixel from 0, SCREEN_WIDTH, contains a height
        """
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
                - an array of [a,b] where a and b are integers. 
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



















#-------------------------------------------------------------_TERRAIN AND SUN------------------------------------

class Sun(GameObject):
    """
    Sun-object is completely decorational in the background. If you set the sun to move by calling Sun.move() after initialization
    the sun moves itself by Sun.angleSpeed each iteration.
    """
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

