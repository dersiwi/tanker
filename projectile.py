from gameobject import GameObject, GameObjectHandler
from pygame.draw import circle
from fpsConstants import FPS
from utilities import Colors
from playerObjects import Terrain

class Explosion(GameObject):
    def __init__(self, x, y, radius):
        super().__init__(x=x, y=y, has_duration=True, duration=2)
        self.x = x
        self.y = y
        self.radius = radius
        self.color = Colors.red
    
    def draw(self, win):
        circle(win, Colors.red, (self.x, self.y), self.radius)
        circle(win, Colors.orange, (self.x, self.y), int(self.radius/2))

class Projectile(GameObject):
    #collisionObjects are added in here, such that later on the bullet can perform collision detection on these objects as well (e.g. trees or something)
    def __init__(self, x, y, xSpeed, ySpeed, terrain, gravity, weapon, collisionObjects, go_handler, owner=None):
        super().__init__(x, y, xSpeed, ySpeed)
        self.projectileColor = Colors.black
        self.terrain : Terrain = terrain  #the terrain object, which the bullet could collide with
        self.weapon = weapon    #the weapon from which the bullet was fired
        self.gravity = gravity

        self.go_handler : GameObjectHandler = go_handler

        self.owner = owner      #the player who fired the missile 

        self.collisionObjects = collisionObjects #for now this HAS to be all the tanks (=playerObjects), in the future this can become an abstract interface
        self.collision = False

        self.hasCollided = False

    
    def projectile_iteration(self) -> bool:
        """
        @return True, if projectile iteration is done. False If there are still iterations to coem
        """
        return self.hasCollided
    

    def updatePosition(self):
        self.x += int(self.xSpeed * FPS.dt)
        self.y -= int(self.ySpeed * FPS.dt)
        self.ySpeed -= self.gravity
        if(self.collisionDetection()):
            self.hasCollided = True

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
        if self.y >= self.terrain.screenHeight - self.terrain.height[self.x]:
            explosionRadius = self.weapon.explosionRadius
            self.terrain.explosion(self.x, explosionRadius)

            #schadensverwaltung für panzer im umkreis der Explosion
            for Tank in self.collisionObjects:
                if Tank.tx > self.x - explosionRadius and Tank.tx < self.x + explosionRadius:
                    Tank.tLp -= int(self.weapon.damage/2)
            self.go_handler.add_gameobject(Explosion(self.x, self.y, explosionRadius))
            return True


    def draw(self, window):
        if not self.hasCollided:
            self.updatePosition()
            circle(window, self.projectileColor, (self.x, self.y), 1)   #pygame function, see import