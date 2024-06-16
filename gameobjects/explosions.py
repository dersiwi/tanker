
from gameobjects.gameobject import GameObject
from pygame.draw import circle
from utils.utilities import Colors, DegreeCnvt, ExplosionData
import math



class Explosion(GameObject):
    def __init__(self, x, y, radius, damage):
        super().__init__(x=x, y=y, has_duration=True, duration=2)
        self.radius = radius
        self.damage = damage

    def get_data(self) -> ExplosionData:
        return ExplosionData(self.x, self.y, self.radius, self.damage)
    
    def draw(self, win):
        circle(win, Colors.red, (self.x, self.y), self.radius)
        circle(win, Colors.orange, (self.x, self.y), int(self.radius/2))


class AdvancedExplosion(GameObject):
    def __init__(self, x, y, radius, damage):
        self.colors = [Colors.yellow, Colors.orange, Colors.red, Colors.black]
        super().__init__(x=x, y=y, has_duration=True, duration=len(self.colors) * 10)
        self.radius = radius
        self.damage = damage
        self.timer = 0


    def get_data(self) -> ExplosionData:
        return ExplosionData(self.x, self.y, self.radius, self.damage)
    
    def update(self):
        self.timer += 1
        self.timer = (self.timer + 1) % len(self.colors)


    def draw(self, win):            
        #circle(win, Colors.red, (self.x, self.y), self.radius)
        #circle(win, Colors.orange, (self.x, self.y), int(self.radius/2))
        circle(win, self.colors[self.timer], (self.x, self.y), int(self.radius/2))



class MushroomCloud(GameObject):
    def __init__(self, x, y, radius, damage):
        super().__init__(x=x, y=y, has_duration=True, duration=20)
        
        self.damage = damage
        self.expl_radius = 10

        self.height = 50
        self.mushroom_width = 50
        self.radius = int(self.mushroom_width/2)

    def get_data(self) -> ExplosionData:
        return ExplosionData(self.x, self.y, self.expl_radius, self.damage)

    def draw_expl(self, win, x, y):
        circle(win, Colors.red, (x, y), self.expl_radius)
        circle(win, Colors.orange, (x, y), int(self.expl_radius/2))
    
    def draw(self, win):
        
        for i in range(0, int(self.height / 10)):
            self.draw_expl(win, self.x, self.y- i * 10)

        #drwa the mushroom
        for i  in range(0, int(self.mushroom_width / 10) + 1):
            self.draw_expl(win, self.x- self.mushroom_width / 2 + i * 10 , self.y - self.height)
        base_x = self.x
        base_y = self.y - self.height
        
        for alpha in range(90, 270, 5):
            alpha = DegreeCnvt.degree_to_radians(alpha)
            center_x = base_x + math.sin(alpha) * self.radius
            center_y = base_y + math.cos(alpha) * self.radius
            self.draw_expl(win, center_x, center_y)
            center_x = base_x + math.sin(alpha) * self.radius / 2
            center_y = base_y + math.cos(alpha) * self.radius / 2
            self.draw_expl(win, center_x, center_y)

        


