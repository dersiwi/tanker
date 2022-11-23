from playerObjects import PlayerObject
from pygame.draw import circle
from fpsConstants import FPS

class Projectile(PlayerObject):
    #collisionObjects are added in here, such that later on the bullet can perform collision detection on these objects as well (e.g. trees or something)
    def __init__(self, x, y, xSpeed, ySpeed, terrain, gravity, weapon, collisionObjects=None, dt=None):
        super().__init__(x, y, xSpeed, ySpeed)
        self.projectileColor = (0,0,0) # black
        self.terrain = terrain  #the terrain object, which the bullet could collide with
        self.weapon = weapon    #the weapon from which the bullet was fired
        self.gravity = gravity


        self.collisionObjects = collisionObjects #for now this HAS to be all the tanks (=playerObjects), in the future this can become an abstract interface

    

    def updatePosition(self):
        self.x += int(self.xSpeed * FPS.dt)
        self.y -= int(self.ySpeed * FPS.dt)
        self.ySpeed -= self.gravity

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
        if self.y >= self.terrain.screenHeight - self.terrain.yWerte[self.x]:
            explosionRadius = self.weapon.explosionRadius
            self.terrain.explosion(self.x, explosionRadius)

            #schadensverwaltung für panzer im umkreis der Explosion
            for Tank in self.collisionObjects:
                if Tank.tx > self.x - explosionRadius and Tank.tx < self.x + explosionRadius:
                    Tank.tLp -= int(self.weapon.damage/2)
            return True


    def draw(self, window):
        self.updatePosition()
        circle(window, self.projectileColor, (self.x, self.y), 1)   #pygame function, see import