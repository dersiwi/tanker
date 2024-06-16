
import json, math, random
from utils.fpsConstants import Globals
from pygame.draw import ellipse, line


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

#from mines import Mines


class TankGlobals:
    class TankInitValues:
        FUEL = 5000
        LP = 100
        TURRET_ANGLE = 45
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

class TankGraphics:
    def __init__(self, width : int, height : int, color) -> None:
        self.turretThickness = 2
        self.turretwidth = 10
        self.turretheight = 8
        self.tcolor = color
        TankGlobals.WIDTH = width                    #used for drawing the tank: width of the bottom ellipse
        TankGlobals.HEIGHT = height                    #used for drawing the tank: height of the bottom ellipse
        pass


    
    def draw(self, window, tx, ty, turret_end_pos):
        #all pyame functions, see import
        ellipse(window, self.tcolor, (tx, ty, TankGlobals.WIDTH, TankGlobals.HEIGHT), 0)
        ellipse(window, self.tcolor, (int(tx + (TankGlobals.WIDTH - self.turretwidth)/2), ty - self.turretheight + 5 ,self.turretwidth, self.turretheight),0)
        line(window, self.tcolor, ((tx + int(TankGlobals.WIDTH/2), ty)), turret_end_pos, self.turretThickness)

