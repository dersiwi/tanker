import math
import random
import pygame

class Terrain:
    def __init__(self, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.yWerte = []

        #terrainColors:
        self.forest_green = (34,139,34)
        #self.sand = (76,70,50)
        self.sand = (219,209,180)
        
        self.color = self.sand      #the terrain color

        self.sunColor = (252,208,70)
        self.sunCoordinates = (int(screenWidth*8/10), int(screenHeight*3/10))
        self.sunRadius = 50

        
    def generate(self, terrainType):
        if terrainType == 3 or terrainType == 404:
            terrainType = random.randint(0,2)
        '''
        Der Plan ist es ein Terrain zu generieren, das aussieht wie x^2.
        Diese Funktion kann ja dann nach lieben vareiert werden.
        
        '''
        if terrainType == 0:
            self.color = self.forest_green
        if terrainType == 1:
            self.color = self.sand

            
        for x in range(self.screenWidth):
            y = int(round(30*math.sin(x/100)+175))
            self.yWerte.append(y)
        return self.yWerte



    def explosion(self,x,r):
        #explosion takes the x koordinate of the center of the explosion and the radius of the explosion
        #The y-Value is taken off the yWertre-Liste.
        #newHeiht = explosionHeight - math.sqrt(r^2-distance from explosion^2)

        #x -= 1 muss sein, da die Liste 0-799 elemente enthält, die Pixel aber von 1-800 gezählt werden
        x -= 1
        yExplosion = self.yWerte[x]
        if x - r > 0 and x + r < self.screenWidth:
            #calculating heights "left of the explosion"
            for xV in range(x-r, x+r):
                distance_to_center = abs(x-xV)
                self.yWerte[xV] = int(yExplosion - round(math.sqrt(r**2 - distance_to_center**2)))

        if x + r > self.screenWidth:
            for xV in range(x-r, self.screenWidth):
                distance_to_center = abs(x-xV)
                self.yWerte[xV] = int(yExplosion - round(math.sqrt(r**2 - distance_to_center**2)))
        if x - r < 0:
            for xV in range(0, x+r):
                distance_to_center = abs(x-xV)
                self.yWerte[xV] = int(yExplosion - round(math.sqrt(r**2 - distance_to_center**2)))
    

    def drawSun(self, window):
        pygame.draw.circle(window, self.sunColor, self.sunCoordinates, self.sunRadius)
            
