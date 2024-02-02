from environment_objects import Terrain, TerrainType, Sun
from projectile import Projectile, Airstrike
from utilities import message_to_screen, Colors, TextButton
from fpsConstants import Globals
from gameobject import GameObject, GameObjectHandler
from player import Player
from tank import Tank
from weapons import Weapon

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


    def __init__(self, window, tanks : list[Tank], terrainType):

        self.window = window
        self.runGameLoop = True

        #-------------gameplay variables
        self.playerTanks : list[Tank] = tanks
        self.game_object_handler : GameObjectHandler = GameObjectHandler.get_instance()
        for tank in self.playerTanks:
            self.game_object_handler.add_gameobject(tank)

        self.playerTurn  : int = 0
        self.currentPlayer : Tank = self.playerTanks[self.playerTurn]

        #-------------------------------initialize static game objects Sun, Terrain, MenuBar
        self.terrain = Terrain(TerrainType(terrainType))

        self.game_object_handler.add_gameobject(Sun())
        self.game_object_handler.add_gameobject(self.terrain)

        self.menuBar = MenuBar()
        self.projectile = None

    
    """
        Return the next player in playerObjects. A player can only be chosen, if he has > 0 LP
        This method also removes all 'dead' players from playerObjects

        If <= 1 player are alive this method sets self.runGameLoop to false
    """
    def nextPlayer(self):
        self.stage = Game.STAGE_ONE

        for i in range(1, len(self.playerTanks)):
            self.playerTurn = (self.playerTurn + i) % len(self.playerTanks)
            self.currentPlayer = self.playerTanks[self.playerTurn]

            if self.currentPlayer.tLp > 0:
                return
            
        self.runGameLoop = False

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
        if self.stage == Game.STAGE_ONE:
            self.stage = Game.STAGE_TWO
            
            pos = self.currentPlayer.get_turret_end_pos()
            
            weapon_type = self.currentPlayer.getCurrentWeapon().w_type
            if  weapon_type == Weapon.TYPE_1:
                self.projectile = Airstrike(self.currentPlayer.getCurrentWeapon())
            elif weapon_type == Weapon.TYPE_0:
                vX, vY = Projectile.calculate_xy_speed(self.currentPlayer.turretAngle, self.currentPlayer.v0)
                self.projectile = Projectile(pos[0], pos[1], vX, vY, self.currentPlayer.getCurrentWeapon())
            else:
                raise ValueError("Unknown weapon_type %s"%weapon_type)

            self.game_object_handler.add_gameobject(self.projectile)
            self.currentPlayer.fire()

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
            self.currentPlayer.move(-1)
                
        if keys[pygame.K_RIGHT]:
            self.currentPlayer.move(1)
            
        if keys[pygame.K_UP]:
            self.currentPlayer.adjust_turret_angle(5)
            
        if keys[pygame.K_DOWN]:
            self.currentPlayer.adjust_turret_angle(-5)
            #change player)

    def redrawGame(self):
        #GAME LOOP DRAWING
        #--------------------terrain drawing
        self.game_object_handler.draw_gameobjects(self.window)
        self.menuBar.draw(self.window, self.currentPlayer) 
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
        pos = (-1, -1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.runGameLoop = False
                self.quitGame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

        self.projectile.projectile_iteration(pos)
        

    def check_if_live(self) -> bool:
        """this method checks if still more than two players are alive   @return true, if tanks are still alive"""
        for tank in self.playerTanks:
            if tank.tLp <= 0 or tank.y >= Globals.SCREEN_HEIGHT:
                self.game_object_handler.remove_gameobject(tank)

        alive = 0
        for tank in self.playerTanks:
            alive += (tank.tLp > 0 and tank.y < Globals.SCREEN_HEIGHT)
        return alive >= 2
            

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
                self.projectile = None
                self.nextPlayer()

            if not self.check_if_live():
                self.runGameLoop = False

            self.window.fill(Colors.skyblue)
            self.game_object_handler.update()
            Game.clock.tick(Globals.FPS.FPS)

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
            if tank.y < Globals.SCREEN_HEIGHT:
                if tank.y < Globals.SCREEN_HEIGHT-(self.terrain.height[tank.x] + tank.theight -5):
                    tank.y += tank.ySpeed
                    tank.ySpeed += int(Globals.GRAVITY * Globals.FPS.dt)
                else:
                    tank.y = Globals.SCREEN_HEIGHT-(self.terrain.height[tank.x] + tank.theight - 5)
                    #Tank.tLp -= Tank.ySpeed
                    tank.ySpeed = 0
            else:
                tank.tLp = 0

class MenuBar:
    def __init__(self):
        self.menuBarColor = (230,238,240)
        self.width = Globals.SCREEN_WIDTH
        self.height = int(Globals.SCREEN_HEIGHT*1.5/10)

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
