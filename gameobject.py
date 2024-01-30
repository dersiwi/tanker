

class GameObject:
    def __init__(self, x=0,y=0,xSpeed=0,ySpeed=0, has_duration : bool = False, duration : int = 0) -> None:
        """
        @param has_duration
        @param duration
        """
        self.show = True
        self.x = x
        self.y = y

        self.hasSpeed = True
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed

        self.has_duration : bool = has_duration
        self.duration : int = duration

    def draw(self, window):
        """
        Draw method every gameobject has to have.
        @param window is the pygame window this gameobject is supposed to draw to 
        """
        raise NotImplementedError("Do not use this class directly, but only create subclasses from it")
    

class GameObjectHandler:

    def __init__(self) -> None:
        self.gameObjects : list[GameObject] = []

    def add_gameobject(self, gameobject : GameObject):
        self.gameObjects.append(gameobject)

    def remove_gameobject(self, gameobject : GameObject):
        self.gameObjects.remove(gameobject)

    def draw_gameobjects(self, win):
        for gameObject in self.gameObjects:
            if gameObject.has_duration:
                if gameObject.duration <= 0:
                    self.gameObjects.remove(gameObject)
                    continue
                if gameObject.has_duration:
                    gameObject.duration -= 1
            gameObject.draw(win)