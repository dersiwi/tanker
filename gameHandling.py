from playerObjects import Terrain, TerrainType, Sun
from projectile import Projectile
from utilities import message_to_screen, Colors, TextButton
from fpsConstants import FPS
from gameobject import GameObject, GameObjectHandler
from player import Player
from tank import Tank

import pygame
import math




"""
    This class is supposed to run the game-loop
    Meaning it generates the terrain for one round, handles drawing and game objects for this round

    However, it does not know about the start-menu or the shop. Player (Tanks) are created somewhere else and only given to 
    the Game-class.

    The game-class has a run method which actually runs the game-loop, draws all objcets
"""
class Game:

    clock = pygame.time.Clock()

    STAGE_ONE = 1
    STAGE_TWO = 2


    def __init__(self, window, w_width, w_height, tanks : list[Tank], terrainType):

        self.window = window
        self.w_width = w_width
        self.w_height = w_height

        self.runGameLoop = True

        #-------------gameplay variables
        self.playerTanks : list[Tank] = tanks
        self.gameObjects : list[GameObject] = []
        self.go_handler : GameObjectHandler = GameObjectHandler()
        self.playerTurn  : int = 0
        self.currentPlayer : Tank = self.playerTanks[self.playerTurn]

        #-------------------------------initialize static game objects Sun, Terrain, MenuBar
        self.sun = Sun(w_width, w_height)
        self.terrain = Terrain(w_width, w_height, TerrainType(terrainType))

        self.go_handler.add_gameobject(self.sun)
        self.go_handler.add_gameobject(self.terrain)

        self.menuBar = MenuBar(screenWidth=w_width, screenHeight=w_height)
        self.currentPlayerHasFired = False
        self.projectile = None
        #--------------constants

        self.gravity = 1.5 * FPS.FPS
    
    """
        Return the next player in playerObjects. A player can only be chosen, if he has > 0 LP
        This method also removes all 'dead' players from playerObjects

        If <= 1 player are alive this method sets self.runGameLoop to false
    """
    def nextPlayer(self):
        if len(self.playerTanks) <= 1:
            self.runGameLoop = False
            return
        
        self.playerTurn = (self.playerTurn + 1) % len(self.playerTanks)
        self.currentPlayer = self.playerTanks[self.playerTurn]
        self.currentPlayerHasFired = False
        self.stage = Game.STAGE_ONE

        #this ensures that no dead player can have turns
        if self.currentPlayer.tLp <= 0:
            self.playerTanks.remove(self.currentPlayer)
            self.nextPlayer()


    def checkMouseClickGame(self, pos):

        if self.menuBar.changeWeaponButton.isClicked(pos):
            self.currentPlayer.changeWeapon()

        elif self.menuBar.moreForceButton.isClicked(pos):
            self.currentPlayer.changeV(1)

        elif self.menuBar.lessForceButton.isClicked(pos):
            self.currentPlayer.changeV(-1)

        elif self.menuBar.fireButton.isClicked(pos):
            self.fire()

    def fire(self):
        if not self.currentPlayerHasFired:
            self.stage = Game.STAGE_TWO
            self.currentPlayer.fire()
            pos = self.currentPlayer.get_turret_end_pos()
            

            angle = self.currentPlayer.turretAngle
            SpeedRoundY = self.currentPlayer.v0
            SpeedRoundX = int(round(self.currentPlayer.v0 * math.cos(angle*180/math.pi)))
            self.projectile = Projectile(pos[0], pos[1], SpeedRoundX, SpeedRoundY, self.terrain, self.gravity, self.currentPlayer.getCurrentWeapon(), self.playerTanks, self.go_handler)
            self.go_handler.add_gameobject(self.projectile)
            self.currentPlayerHasFired = True

    """
        Handle all key-pressed events that are happening
    """
    def handleKeyPressed(self, keys):
        #checks for keys being pressed

        if keys[pygame.K_SPACE]:
            self.fire()

        if keys[pygame.K_0]:
            self.nextPlayer()
            
        if keys[pygame.K_LEFT]:
            self.currentPlayer.move(-1, self.terrain.height)
                
        if keys[pygame.K_RIGHT]:
            self.currentPlayer.move(1, self.terrain.height)
            
        if keys[pygame.K_UP]:
            self.currentPlayer.turretAngle += 1
            
        if keys[pygame.K_DOWN]:
            self.currentPlayer.turretAngle -= 1
            #change player)

    def redrawGame(self):
        #GAME LOOP DRAWING
        #--------------------terrain drawing
        self.go_handler.draw_gameobjects(self.window)
        self.menuBar.draw(self.window, self.currentPlayer)
        

        for tank in self.playerTanks:
            if tank.tLp > 0:
                tank.draw(self.window)    
        pygame.display.update()
    


    def __stage_one_iteration(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.runGameLoop = False
                self.quitGame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.checkMouseClickGame(pygame.mouse.get_pos())

        self.handleKeyPressed(keys = pygame.key.get_pressed())

    def __stage_two_iteration(self):
        self.projectile.projectile_iteration()


    def gameLoop(self):
        """
        Runs the game-loop. This method works in two stages for ecah player
            Stage 1 - Adjusting Stage:
                The player can drive around, change weapons, adjust force etc.
                As soon as the player fires, this switches to stage two
            Stage 2 - Projectile Stage:
                The player has fired and the projcetile is in the air. During this phase the projectile of the player is 
                Flying and the phase (and thereby the player turn) ends when the projectile has expoloded and all damage etc. is dealt with.
        """
        self.runGameLoop = True
        self.quitGame = False
        self.stage = Game.STAGE_ONE
        while self.runGameLoop:
            
            if self.stage == Game.STAGE_ONE:
                self.__stage_one_iteration()
            elif self.stage == Game.STAGE_TWO:
                self.__stage_two_iteration()
            else:
                raise ValueError("Unknown stage %i."%self.stage)

                
            if not self.projectile == None and self.projectile.hasCollided:
                self.go_handler.remove_gameobject(self.projectile)
                self.projectile = None
                self.nextPlayer()

            self.window.fill(Colors.skyblue)
            self.__check_gravity()            
            Game.clock.tick(FPS.FPS)

            #das ist nur eine Provisorische Abfrage um bugs uz vermeiden
            if self.currentPlayer.tLp == 0:
                self.nextPlayer()
            self.redrawGame()

        if self.quitGame:
            pygame.quit()


    def __check_gravity(self):
        """
        For each tank, this function checks if a tank is floating in the air and then applies gravity (changes the tank's) y-velocity
        """
        for tank in self.playerTanks:
            if tank.ty < self.w_height:
                if tank.ty < self.w_height-(self.terrain.height[tank.tx] + tank.theight -5):
                    tank.ty += tank.ySpeed
                    tank.ySpeed += int(self.gravity * FPS.dt)
                else:
                    tank.ty = self.w_height-(self.terrain.height[tank.tx] + tank.theight - 5)
                    #Tank.tLp -= Tank.ySpeed
                    tank.ySpeed = 0
            else:
                tank.tLp = 0

class MenuBar:
    def __init__(self, screenWidth, screenHeight):
        self.menuBarColor = (230,238,240)
        self.width = screenWidth
        self.height = int(screenHeight*1.5/10)

        #(x, y, width, height, text=None, fontSize=12, color=Colors.black
        self.changeWeaponButton = TextButton(x=410, y=25, text="Change Weapon", fontSize=20, color=Colors.grey)
        self.moreForceButton = TextButton(x=600, y=10, text="More", fontSize=20)
        self.lessForceButton = TextButton(x=600, y=40, text="Less", fontSize=20)
        self.fireButton = TextButton(x=750, y=25, text="FIRE", fontSize=25, color=Colors.red)

        self.buttons = [self.changeWeaponButton, self.moreForceButton, self.lessForceButton, self.fireButton]

    def draw(self, win, currentPlayer : Tank):
        #-------------------Controlbar and contents of controlbar
        pygame.draw.rect(win, self.menuBarColor, (0,0, self.width, self.height))
        pygame.draw.line(win, (240,248,255), (0,self.height+1), (self.width, self.height+1), 0)

        #--drawing the current player
        currentPlayer.tank_graphics.draw(win, 0, currentPlayer.tank_graphics.turretheight, Tank.calculateTurretEndPos(0,currentPlayer.tank_graphics.turretheight, currentPlayer.turretAngle))
        #pygame.draw.ellipse(win, currentPlayer.tcolor, (0, currentPlayer.turretheight, currentPlayer.twidth, currentPlayer.theight), 0)
        #pygame.draw.ellipse(win, currentPlayer.tcolor, (int((currentPlayer.twidth-currentPlayer.turretwidth)/2), 5,currentPlayer.turretwidth,currentPlayer.turretheight),0)

        message_to_screen(win, str(currentPlayer.playerNumber), Colors.black, 20, (currentPlayer.twidth+5,0))

        #--the fuel and the left and right buttons
        message_to_screen(win, str("Fuel: " + str(currentPlayer.fuel)), Colors.black, 20, (currentPlayer.twidth+5, 15))
        #left button is missing
        #right button is missing

        #--Livepoints
        message_to_screen(win, str("LP: " + str(currentPlayer.tLp)), Colors.black, 20, (currentPlayer.twidth+5, 30))

        #--Weapons and Amount
        stringWeapons = str(currentPlayer.getCurrentWeapon().amount) + " : "
        stringWeapons += str(currentPlayer.getCurrentWeapon().name)
        message_to_screen(win, stringWeapons, Colors.black, 20, (400,5))

        #change v0-Projectile Buttons
        message_to_screen(win, str("Force: " + str(currentPlayer.v0)), Colors.black, 20,(600, 25))

        for button in self.buttons:
            button.draw(win)
