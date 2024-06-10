import pygame
from utilities import message_to_screen, TextButton,Colors
from core_objects import Tank, Terrain, Sun
from core_object_utilities import TerrainType
from fpsConstants import Globals
from gameobject import GameObject
import math, random
from gameobject import GameObjectHandler



class Animation():
    def __init__(self, w_width, w_height):
        self.x = 0
        self.y = int(w_height / 2)

        self.width = 50
        self.height = 20

        self.xSpeed = 200

        self.maxX = w_width - self.width
    
    def updatePosition(self):
        self.x += int(self.xSpeed * Globals.FPS.dt)
        if self.x > self.maxX:
            self.x = 0
    
    def draw(self, win):
        pygame.draw.rect(win, (0,50,0), pygame.Rect(self.x, self.y, self.width, self.height))
        self.updatePosition()


class StartMenuBackground:
    def __init__(self, screenWidth, screenHeight):
        self.screenHeight = screenHeight
        self.go_handler = GameObjectHandler.get_instance()
        
        self.backgroundTerrain = Terrain(TerrainType.RANDOM)
        self.go_handler.add_gameobject(self.backgroundTerrain)

        self.backgroundSun = Sun(angleSpeed = Sun.NORMAL_MOVING_SPEED)
        #birng life into the game 

        self.tanks = []
        for x in range(random.randint(2, 4)):
            t = Tank(tx = random.randint(10, screenWidth - 10), ty = 50, color = Colors.black, initial_weapons=None)
            self.go_handler.add_gameobject(t)
            self.tanks.append(t)

        #self, tx, ty, color, screenwidth, playerNumber
        self.action = -1
        self.actionDuration = 0
        self.projectile = None
        self.actingTank : Tank = None

    def chooseRandomAction(self):
        if random.randint(0, 100) < 10:
            self.actingTank = self.tanks[random.randint(0, len(self.tanks) - 1)]
            self.action = random.randint(0,2)
            
            if self.action == 0 or self.action == 1: # drive around
                self.actionDuration = 20


    def randomAction(self):
        if self.actionDuration > 0:
            if self.action == 0:
                self.actingTank.move(1)
            if self.action == 1:
                self.actingTank.move(-1)
                
            self.actionDuration -= 1
        else:
            self.chooseRandomAction()

    def draw(self, win):
        win.fill(Colors.skyblue)
        self.backgroundSun.draw(win)
        self.go_handler.draw_gameobjects(win)
        self.go_handler.update()

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
        self.terrainTypeSelected = TerrainType.RANDOM


        for idx, name in enumerate(TerrainType.get_instance().get_all_terrain_names()):
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
    """
    This class is resposible for choosing the amount and type of players.
    It dynamically adds buttons, such that the amount of buttons always equals the amount of players.
    
    """

    class PlayerType:
        HUMAN = 0
        AI = 1
        RANDOM = 2
        IDXS = [HUMAN, AI, RANDOM]
        STRINGS = ["Human", "Computer", "Random"]

    MAX_PLAYER = 4
    def __init__(self, x : int, y : int, fontsize : int) -> None:
        super().__init__(x, y)
        
        self.player_buttons : list[TextButton] = []
        self.player_type : list[int] = []

        self.fontsize = fontsize
        self.currY = 0
        self.__create_player_button()
        self.__create_player_button()

        self.__create_add_and_remove_button()

    def __create_add_and_remove_button(self):
        self.addPlayer = TextButton(
            x = int(self.x+150),
            y = int(self.y+50),
            text = "add player",fontSize = self.fontsize,color=Colors.green,border=True,margin=10)
        self.addPlayer.addBackground()
        self.removePlayer = TextButton(
            x = int(self.x+150),
            y = int(self.y+100),
            text = "remove player",fontSize = self.fontsize,color=Colors.red,border=True,margin=10)
        self.removePlayer.addBackground()


    def __create_player_button(self):
        if len(self.player_buttons) >= PlayerSelector.MAX_PLAYER:
            return
        self.player_buttons.append(TextButton(x = self.x, y = int(self.y + 2 * self.fontsize * (self.currY + 2)), text = "Human", fontSize=self.fontsize, border=True, margin=int(self.fontsize / 5)))
        self.player_type.append(PlayerSelector.PlayerType.HUMAN)
        self.currY += 1

    def __remove_player_button(self):
        if len(self.player_buttons) > 2:
            self.player_buttons.pop(-1)
            self.player_type.pop(-1)
            self.currY -= 1

    def __change_player_type(self, button_index : int):
        self.player_type[button_index] = (self.player_type[button_index] + 1) % len(PlayerSelector.PlayerType.IDXS)
        self.player_buttons[button_index].setText(PlayerSelector.PlayerType.STRINGS[self.player_type[button_index]])
    
    def checkForButtonBlick(self, pos):
        if self.addPlayer.isClicked(pos):
            self.__create_player_button()
        if self.removePlayer.isClicked(pos):
            self.__remove_player_button()

        for button_idx, button in enumerate(self.player_buttons):
            if button.isClicked(pos):
                self.__change_player_type(button_idx)

    def get_n_players(self):
        return len(self.player_buttons)
    
    def get_player_types(self) -> list[int]:
        """
        @return a list of player_types @see PlayerSelector.PlayerType for information
        """
        return self.player_type

    
    def draw(self, win):
        for button in self.player_buttons:
            button.draw(win)
        self.addPlayer.draw(win)
        self.removePlayer.draw(win)

class StartMenu:
    """
    The menu-calss basically has two modes
    1. Choosing terrain and 
    2. Choosing the player and playertype
    """
    TERRAIN_SELECTION_MODE = -1
    TERRAIN_SELECTION_TEXT = "Choose players"
    PLAYER_SELECTION_MODE = 1
    PLAYER_SELECTION_TEXT = "Choose terrain"

    clock = pygame.time.Clock()
    def __init__(self, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.terrain_selector : TerrainSelector = TerrainSelector(x = self.screenWidth * 1.5/10, y = int(self.screenHeight * 2/10), fontsize = 35)
        self.player_selector : PlayerSelector = PlayerSelector(x = self.screenWidth * 1.5/10, y = int(self.screenHeight * 2/10), fontsize = 35)
        
        self.runMenuBool = True
        self.gotoGame = True

        self.mode = StartMenu.TERRAIN_SELECTION_MODE
        self.mode_switch_button = TextButton(x = int(self.screenWidth * 4/10), y = int(self.screenHeight * 6/10), text=StartMenu.TERRAIN_SELECTION_TEXT, fontSize=35,
                                                    color=Colors.red,border=True,margin=10)
        
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
        if self.mode == StartMenu.TERRAIN_SELECTION_MODE:
            self.terrain_selector.checkForTerrainButtonClick(pos)
        elif self.mode == StartMenu.PLAYER_SELECTION_MODE:
            self.player_selector.checkForButtonBlick(pos)
        if self.playButton.isClicked(pos):
            self.runMenuBool = False
        
        if self.mode_switch_button.isClicked(pos):
            if self.mode == StartMenu.TERRAIN_SELECTION_MODE:
                self.mode = StartMenu.PLAYER_SELECTION_MODE
                self.mode_switch_button.text = StartMenu.PLAYER_SELECTION_TEXT
            elif self.mode == StartMenu.PLAYER_SELECTION_MODE:
                self.mode = StartMenu.TERRAIN_SELECTION_MODE
                self.mode_switch_button.text = StartMenu.TERRAIN_SELECTION_TEXT
            else:
                raise ValueError("Mode %i unknowon"%self.mode)

    def drawMenu(self, win):
        self.background.draw(win)
        message_to_screen(win, "TANKER", Colors.red, 50, (int(self.screenWidth/2-80),int(self.screenHeight/5)))

        self.playButton.draw(win)
        self.mode_switch_button.draw(win)
        if self.mode == StartMenu.TERRAIN_SELECTION_MODE:
            self.terrain_selector.draw(win)
        elif self.mode == StartMenu.PLAYER_SELECTION_MODE:
            self.player_selector.draw(win)
        else:
            raise ValueError("Illegal mode %i in startmenu"%self.mode)
        pygame.display.update()
        #pygame.image.save(win, "images/images_for_startscreen_gif/img%.3i.png"%self.counter)
        #self.counter += 1


    def runMenu(self, win):
        #self.counter = 0
        while self.runMenuBool:
            #pygame.time.delay(100)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runMenuBool = False
                    self.gotoGame = False
                    continue
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.checkMouseClick(pygame.mouse.get_pos())

            win.fill(Colors.white)
            StartMenu.clock.tick(Globals.FPS.FPS)
            self.drawMenu(win)
            
        if not self.gotoGame:
            pygame.quit()

    