import pygame
from utilities import message_to_screen, TextButton,Colors
from tank import Tank
from playerObjects import Terrain, Sun
from fpsConstants import FPS



class Animation():
    def __init__(self, w_width, w_height):
        self.x = 0
        self.y = int(w_height / 2)

        

        self.width = 50
        self.height = 20

        self.xSpeed = 200

        self.maxX = w_width - self.width
    
    def updatePosition(self):
        self.x += int(self.xSpeed * FPS.dt)
        if self.x > self.maxX:
            self.x = 0
    
    def draw(self, win):
        pygame.draw.rect(win, (0,50,0), pygame.Rect(self.x, self.y, self.width, self.height))
        self.updatePosition()


class StartMenuBackground:
    def __init__(self, screenWidth, screenHeight):
        self.backgroundTerrain = Terrain(screenWidth, screenHeight)
        self.backgroundTerrain.generate(Terrain.RANDOM)
        self.backgroundSun = Sun(screenWidth, screenHeight)
        self.backgroundSun.move()


    def draw(self, win):
        self.backgroundTerrain.draw(win)
        self.backgroundSun.draw(win)

class StartMenu:

    clock = pygame.time.Clock()
    def __init__(self, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.playButtonCoordinates = (int(screenWidth * 8/10), int(screenHeight * 6/10))        


        self.terrainBlockX = 150
        self.terrainBlockY = 150
        
        self.fontSizeterrains = 35
        self.dterrainBlock = 2 * self.fontSizeterrains
        self.colorSelected = Colors.red 


        self.terrainTypeWoods = TextButton(self.terrainBlockX, y = int(self.terrainBlockY + self.dterrainBlock * 2), text = "Woords", fontSize=self.fontSizeterrains)
        self.terrainTypeDessert = TextButton(self.terrainBlockX, y = int(self.terrainBlockY + self.dterrainBlock * 3), text = "Dessert", fontSize=self.fontSizeterrains)
        self.terrainTypeRandom = TextButton(self.terrainBlockX, y = int(self.terrainBlockY + self.dterrainBlock * 4), text = "Random", fontSize=self.fontSizeterrains)
        self.terrainTypeSelected = None
        self.terrainButtons = [self.terrainTypeWoods, self.terrainTypeDessert, self.terrainTypeRandom]
        
        for button in self.terrainButtons:
            button.addBorder()
            button.addBackground()
            button.setMargin(int(self.fontSizeterrains / 5))
        
        self.runMenuBool = True
        self.gotoGame = True

        self.playButton = TextButton(
            x = int(screenWidth * 8/10),
            y = int(screenHeight * 6/10),
            text = "PLAY",
            fontSize = 40,
            color=Colors.green
            )
        self.playButton.addBorder()
        self.playButton.addBackground()
        self.playButton.setMargin(10)
        
        self.buttons = [self.playButton, self.terrainTypeDessert, self.terrainTypeRandom, self.terrainTypeWoods]

        self.animation = Animation(screenWidth, screenHeight)
        self.background = StartMenuBackground(screenWidth, screenHeight)



    def checkForTerrainButtonClick(self, pos, button, valueIfClicked):
        if button.isClicked(pos):
            self.resetTerrainButtonColors()
            button.setBackgroundColor(self.colorSelected)
            self.terrainTypeSelected = valueIfClicked

    def resetTerrainButtonColors(self):
        for button in self.terrainButtons:
            button.setBackgroundColor(Colors.white)

    def checkMouseClick(self, pos):
        #this function checks if the mouse clicked any buttons and executes the corresponding action

        for i in range(len(self.terrainButtons)):
            self.checkForTerrainButtonClick(pos, self.terrainButtons[i], i)

        if self.playButton.isClicked(pos):
            self.runMenuBool = False
            

    def drawMenu(self, win):
        self.background.draw(win)
        #-----Trying to get an animation to work
        self.animation.draw(win)
        #-----

        message_to_screen(win, "TANKER", Colors.red, 50, (int(self.screenWidth/2-80),int(self.screenHeight/5)))
        
        for button in self.buttons:
            button.draw(win)
        pygame.display.update()


    def runMenu(self, win):
        while self.runMenuBool:
            #pygame.time.delay(100)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runMenuBool = False
                    self.gotoGame = False
                    continue
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #print(pygame.mouse.get_pos())
                    self.checkMouseClick(pygame.mouse.get_pos())

            win.fill(Colors.white)
            StartMenu.clock.tick(FPS.FPS)
            self.drawMenu(win)
            
        if not self.gotoGame:
            pygame.quit()

    