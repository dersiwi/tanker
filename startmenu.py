import pygame
from utilities import message_to_screen, TextButton,Colors
from tank import Tank
from playerObjects import Terrain, TerrainType, Sun
from fpsConstants import FPS
from random import randrange
from gameobject import GameObject
import math



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
        self.screenHeight = screenHeight
        self.backgroundTerrain = Terrain(screenWidth, screenHeight, TerrainType(TerrainType.RANDOM))
        self.backgroundSun = Sun(screenWidth, screenHeight)
        self.backgroundSun.move()
        

        #birng life into the game 
        amountTanks = randrange(2, 5)
        self.tanks = []
        for x in range(amountTanks):
            tankX = randrange(10, screenWidth - 10)
            tankNUmber = 0
            self.tanks.append(Tank(tankX, self.backgroundTerrain.height[tankX], Colors.black, screenWidth, tankNUmber))

        #self, tx, ty, color, screenwidth, playerNumber
        self.gravity = 3
        self.action = -1
        self.actionDuration = 0
        self.projectile = None
        self.actingTank = None


    def updatePositions(self):
        for tank in self.tanks:
            if tank.ty < self.screenHeight-(self.backgroundTerrain.height[tank.tx] + tank.theight -5):
                tank.ty += tank.ySpeed
                tank.ySpeed += int(math.ceil(self.gravity * FPS.dt))
            else:
                tank.ty = self.screenHeight-(self.backgroundTerrain.height[tank.tx] + tank.theight - 5)
                #Tank.tLp -= Tank.ySpeed
                tank.ySpeed = 0

    def chooseRandomAction(self):
        actionChance = randrange(0, 100)

        if actionChance < 10:
            self.actingTank = self.tanks[randrange(0, len(self.tanks))]
            self.action = randrange(0,3)
            
            if self.action == 0 or self.action == 1: # drive around
                self.actionDuration = 20
                

    def randomAction(self):
        if self.actionDuration > 0:
            if self.action == 0:
                self.actingTank.move(1, self.backgroundTerrain.height)
            if self.action == 1:
                self.actingTank.move(-1, self.backgroundTerrain.height)
                
            self.actionDuration -= 1
        else:
            self.chooseRandomAction()

    def draw(self, win):
        self.backgroundTerrain.draw(win)
        self.backgroundSun.draw(win)
        for t in self.tanks:
            t.draw(win)
        self.updatePositions()
        self.randomAction()


class TerrainSelector(GameObject):
    """
    This class creates buttons for each terrain type in TerrainType.NAMES and draws those buttons below each other

    """

    def __init__(self, x : int, y : int, fontsize : int) -> None:

        super().__init__(x, y)
        self.fontsize = fontsize
        self.dterrainBlock = 2 * fontsize
        self.terrainButtons : list[TextButton] = []
        
        self.colorSelected = Colors.red 
        self.terrainTypeSelected = None


        for idx, name in enumerate(TerrainType.NAMES):
            terrainButton = TextButton(x = self.x, y = int(self.y + self.dterrainBlock * (idx + 2)), text = name, fontSize=self.fontsize, border=True, margin=int(self.fontsize / 5))
            terrainButton.addBackground()
            self.terrainButtons.append(terrainButton)

    def resetTerrainButtonColors(self):
        """Rest all the background colors of all buttons to white"""
        for button in self.terrainButtons:
            button.setBackgroundColor(Colors.white)

    def checkForTerrainButtonClick(self, pos):
        """
        Checks if one of the buttons was clicked and if so, sets its background color to self.selected and also sets the terrainTypeSelected
        """
        for idx, button in enumerate(self.terrainButtons):
            if button.isClicked(pos):
                self.resetTerrainButtonColors()
                button.setBackgroundColor(self.colorSelected)
                self.terrainTypeSelected = idx
        
    def draw(self, window):
        for button in self.terrainButtons:
            button.draw(window)


class PlayerSelector(GameObject):
    def __init__(self, x : int, y : int, fontsize : int) -> None:
        super().__init__(x, y)

    def draw(self, win):
        pass

class StartMenu:
    """
    The menu-calss basically has two modes
    1. Choosing terrain and 
    2. Choosing the player and playertype
    """
    TERRAIN_SELECTION_MODE = -1
    PLAYER_SELECTION_MODE = 1

    clock = pygame.time.Clock()
    def __init__(self, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.terrain_selector : TerrainSelector = TerrainSelector(x = self.screenWidth * 1.5/10, y = int(self.screenHeight * 2/10), fontsize = 35)
        self.player_selector : PlayerSelector = PlayerSelector(x = self.screenWidth * 1.5/10, y = int(self.screenHeight * 2/10), fontsize = 35)
        self.mode_switch_button = TextButton(x = int(self.screenWidth * 4/10), y = int(self.screenHeight * 6/10), text="Choose Players", fontSize=35,
                                             color=Colors.red,border=True,margin=10)
        
        self.runMenuBool = True
        self.gotoGame = True

        self.mode = StartMenu.TERRAIN_SELECTION_MODE
        
        self.create_playbutton()
        #self.animation = Animation(screenWidth, screenHeight)
        self.background = StartMenuBackground(screenWidth, screenHeight)

    def create_playbutton(self):
        self.playButton = TextButton(
            x = int(self.screenWidth * 8/10),
            y = int(self.screenHeight * 6/10),
            text = "PLAY",fontSize = 40,color=Colors.green,border=True,margin=10)
        

        self.playButton.addBackground()
    def checkMouseClick(self, pos):
        #this function checks if the mouse clicked any buttons and executes the corresponding action
        self.terrain_selector.checkForTerrainButtonClick(pos)
        if self.playButton.isClicked(pos):
            self.runMenuBool = False
        
        if self.mode_switch_button.isClicked(pos):
            self.mode *= (-1)

    def drawMenu(self, win):
        self.background.draw(win)
        message_to_screen(win, "TANKER", Colors.red, 50, (int(self.screenWidth/2-80),int(self.screenHeight/5)))

        self.playButton.draw(win)
        self.mode_switch_button.draw(win)
        if self.mode == StartMenu.TERRAIN_SELECTION_MODE:
            self.terrain_selector.draw(win)
        elif self.mode == StartMenu.PLAYER_SELECTION_MODE:
            self.player_selector.draw(win)
            print("DWro")
        else:
            raise ValueError("Illegal mode %i in startmenu"%self.mode)
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

    