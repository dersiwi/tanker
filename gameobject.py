from fpsConstants import Globals
from utilities import ExplosionData



class GameObject:

    NO_BOUNDING_BOX = (-1, -1, -1, -1)

    class BoundingBox:
        X = 0
        Y = 1
        WIDTH = 2
        HEIGHT = 3

        def create_bounding_box(x, y, width, height):
            return (x, y, width, height)

    def __init__(self, x=0,y=0,xSpeed=0,ySpeed=0,
                  has_duration : bool = False, duration : int = 0, 
                 affected_by_gravity : bool = False, 
                 collision_class : int = Globals.CollisionClass.NO_COLLISION,
                 affected_by_explosion : bool = False) -> None:
        """
        @param x
        @param y
        @param xSpeed
        @param ySpeed
        @param has_duration
        @param duration
        @param affected_by_gravity
        @param collision_class
        @param affected_by_explosion
        """
        self.show = True
        self.x = x
        self.y = y

        self.hasSpeed = True
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed

        self.has_duration : bool = has_duration
        self.duration : int = duration

        self.collision_class = collision_class

        self.affected_by_gravity : bool = affected_by_gravity
        self.affected_by_explosion : bool = affected_by_explosion

    def update(self):
        self.x += int(self.xSpeed * Globals.FPS.dt)
        self.y += int(self.ySpeed * Globals.FPS.dt)

        if self.affected_by_gravity:
            self.ySpeed += Globals.GRAVITY * Globals.FPS.dt

    def get_bounding_box(self) -> tuple[int, int, int, int]:
        """"
        @return a rect of upper left x and y corner and the lower left x and y corner
        For some objects a simple bounding box is not possible, in this case, they return GameObject.NO_BOUNDING_BOX
        """
        return GameObject.NO_BOUNDING_BOX

    def explosion(self, expl : ExplosionData):
        """
        This method is called when an explosion happend and this gameobject is inside the explosion-radius.
        @param x : x-coordinate of the explosion
        @param y : y-coordinate of the explosion
        @param radius : radius of the explosion
        """
        pass

    def collision_detecetion(self, gameobject) -> bool:
        """
        This method is only implemented by objects that do not have bounding boxes. 
        Passed gamobjects are gameobjects with collision_class == 2 and the method
        @return true if the given gameobject collides with this.
        """
        raise NotImplementedError("An object with collison class 1 has to implemenet this method.")
    

    def collision(self, gameobject):
        """
        This method is called when a gameobject collided with another gameobject
        @param gameobject is the gmaeobjbcet that just collided with this.gameobject
        """
        pass

    def draw(self, window):
        """
        Draw method every gameobject has to have.
        @param window is the pygame window this gameobject is supposed to draw to 
        """
        raise NotImplementedError("Do not use this class directly, but only create subclasses from it")
    

"""
Collision detection;
The problem is to detect arbitrary collisions between objects. To somehow detect collisions
i implemenetd bounding-boxes, such that two object with bounding boxes can detect if they
collide with each other.

An object that DOES NOT HAVE a bounding box (i.e. terrain) is collision_class_1, 

"""
class GameObjectHandler:

    handler = None

    def get_instance():
        """
        Singleton pattern. This method always returns the same instance of the GameObjectHandler
        """
        if GameObjectHandler.handler == None:
            GameObjectHandler.handler = GameObjectHandler()
        return GameObjectHandler.handler
    
    def destroy_instance():
        """Destroys the instance and makes get_instance return a new instance."""
        GameObjectHandler.handler = None

    def __init__(self) -> None:
        self.gameObjects : list[GameObject] = []
        self.collision_classes : list[list[GameObject]] = [[] for collision_class in Globals.CollisionClass.CLASSES]
    

    def add_gameobject(self, gameobject : GameObject):
        self.gameObjects.append(gameobject)
        self.collision_classes[gameobject.collision_class].append(gameobject)

    def remove_gameobject(self, gameobject : GameObject):
        try:
            self.collision_classes[gameobject.collision_class].remove(gameobject)
            self.gameObjects.remove(gameobject)
        except Exception as e:
            print(gameobject)
            print(e.args)



    def explosion(self, expl : ExplosionData):
        for gameobject in self.gameObjects:
            if gameobject.affected_by_explosion:
                gameobject.explosion(expl)

    def update(self):
        """
        This method updates all gameobjects,
        i.e. applies gravity, checks for collisions and valid-durations
        """
        for gameobject in self.gameObjects:

            #handle duration-stuff
            if gameobject.has_duration:
                if gameobject.duration <= 0:
                    self.gameObjects.remove(gameobject)
                    continue
                if gameobject.has_duration:
                        gameobject.duration -= 1

            #gravity etc is handled here
            gameobject.update()
        
        for i in range(len(self.collision_classes[Globals.CollisionClass.CLASS_TWO])):
            if i >= len(self.collision_classes[Globals.CollisionClass.CLASS_TWO]):
                #its possible that during a collision event a gameobject removed itself and therefore the list shrank
                break
            go1 = self.collision_classes[Globals.CollisionClass.CLASS_TWO][i]
            
            #check for collisions with collision class one 
            for go in self.collision_classes[Globals.CollisionClass.CLASS_ONE]:
                if go.collision_detecetion(go1):
                    go.collision(go1)
                    go1.collision(go)
            

            #check for collision with other collision class-two objects
            for j in range(i+1, len(self.collision_classes[Globals.CollisionClass.CLASS_TWO])):
                if j >= len(self.collision_classes[Globals.CollisionClass.CLASS_TWO]):
                #its possible that during a collision event a gameobject removed itself and therefore the list shrank
                    break
                go2 = self.collision_classes[Globals.CollisionClass.CLASS_TWO][j]
                
                if GameObjectHandler.collision_detection(go1, go2):
                    go1.collision(go2)
                    go2.collision(go1)
            
    def collision_detection(go1 : GameObject, go2 : GameObject) -> bool:
        """
        Given two gameobejcts @param go1, go2 : gameobjects with collision_class 2
        this method returns true if the gameobjects collided and false if they didn't
        """
        #this is the gameobject with the smaller x-coordinate 
        gameobject_furthest_left, gameobject_furthest_right = (go1, go2) if go1.x < go2.x else (go2, go1)

        if gameobject_furthest_right.x - gameobject_furthest_left.x <= gameobject_furthest_left.get_bounding_box()[GameObject.BoundingBox.WIDTH]:
            #collection in x-direction is possible
            gameobject_lowest, gameobject_highest = (go1, go2) if go1.y < go2.y else (go2, go1)
            #because the "lower" it gets on the screen, the higher the y-coordinate gets, thats why this has to be an aboslute value
            #as the gameobject_lowest.y - gameobject_highest.y is negative
            if abs(gameobject_lowest.y - gameobject_highest.y)  <= gameobject_lowest.get_bounding_box()[GameObject.BoundingBox.HEIGHT]:
                return True
        return False

    def draw_gameobjects(self, win):
        for gameObject in self.gameObjects:
            gameObject.draw(win)