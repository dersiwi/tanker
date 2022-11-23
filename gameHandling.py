from playerObjects import Terrain, Sun
from projectile import Projectile
from utilities import message_to_screen, Colors, TextButton
from fpsConstants import FPS

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


    def __init__(self, window, w_width, w_height, terrainType):

        self.window = window
        self.w_width = w_width
        self.w_height = w_height

        self.runGameLoop = True

        #-------------gameplay variables
        self.currentPlayer = None
        self.playerTanks = []
        self.gameObjects = []

        self.playerTurn = 0

        #-------------------------------initialize static game objects Sun, Terrain, MenuBar
        self.sun = Sun(w_width, w_height)
        self.terrain = Terrain(w_width, w_height)
        self.terrain.generate(terrainType)

        self.gameObjects.append(self.sun)
        self.gameObjects.append(self.terrain)

        self.menuBar = MenuBar(screenWidth=w_width, screenHeight=w_height)

        self.projectile = None

        #--------------constants

        self.gravity = 1.5 * FPS.FPS

        

    #create copy of player tanks so the modification of self.playerTanks does not effect global player-array
    def setPlayerTanks(self, playerTanks):
        for tank in playerTanks:
            self.playerTanks.append(tank)
        self.currentPlayer = self.playerTanks[self.playerTurn]

    
    """
        Return the next player in playerObjects. A player can only be chosen, if he has > 0 LP
        This method also removes all 'dead' players from playerObjects

        If <= 1 player are alive this method sets self.runGameLoop to false
    """
    def nextPlayer(self):
        amountLiving = 0
        for Tank in self.playerTanks:
            if Tank.tLp > 0:
                amountLiving += 1
        if amountLiving <= 1:
            self.runGameLoop = False
            return

        
        if self.playerTurn == len(self.playerTanks) - 1:
            self.playerTurn = 0 
        else:
            self.playerTurn += 1
        self.currentPlayer = self.playerTanks[self.playerTurn]

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
        self.currentPlayer.fire()
        pos = self.currentPlayer.calculateTurretEndPos()
        

        angle = self.currentPlayer.turretAngle
        SpeedRoundY = self.currentPlayer.v0
        SpeedRoundX = int(round(self.currentPlayer.v0 * math.cos(angle*180/math.pi)))
        self.projectile = Projectile(pos[0], pos[1], SpeedRoundX, SpeedRoundY, self.terrain, self.gravity, self.currentPlayer.getCurrentWeapon(), self.playerTanks)
        self.gameObjects.append(self.projectile)

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
            self.currentPlayer.move(-1, self.terrain.yWerte)
                
        if keys[pygame.K_RIGHT]:
            self.currentPlayer.move(1, self.terrain.yWerte)
            
        if keys[pygame.K_UP]:
            self.currentPlayer.turretAngle += 1
            
        if keys[pygame.K_DOWN]:
            self.currentPlayer.turretAngle -= 1
            #change player)

    def redrawGame(self):
        #GAME LOOP DRAWING
        #--------------------terrain drawing
        for gameObject in self.gameObjects:
            gameObject.draw(self.window)


        self.menuBar.draw(self.window, self.currentPlayer)
        

        for tank in self.playerTanks:
            if tank.tLp > 0:
                tank.draw(self.window)        
        pygame.display.update()
        


    def gameLoop(self):
        self.runGameLoop = True
        while self.runGameLoop:
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runGameLoop = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.checkMouseClickGame(pygame.mouse.get_pos())


            self.handleKeyPressed(keys = pygame.key.get_pressed())

            if not self.projectile == None and self.projectile.collisionDetection():
                self.gameObjects.remove(self.projectile)
                self.projectile = None
                self.nextPlayer()

            self.window.fill(Colors.skyblue)
            for tank in self.playerTanks:
                if tank.ty < self.w_height:
                    if tank.ty < self.w_height-(self.terrain.yWerte[tank.tx] + tank.theight -5):
                        tank.ty += tank.ySpeed
                        tank.ySpeed += int(self.gravity * FPS.dt)
                    else:
                        tank.ty = self.w_height-(self.terrain.yWerte[tank.tx] + tank.theight - 5)
                        #Tank.tLp -= Tank.ySpeed
                        tank.ySpeed = 0
                        
                else:
                    tank.tLp = 0
            
            Game.clock.tick(FPS.FPS)

            #das ist nur eine Provisorische Abfrage um bugs uz vermeiden
            if self.currentPlayer.tLp == 0:
                self.nextPlayer()
            self.redrawGame()

        pygame.quit()
    


class MenuBar:
    def __init__(self, screenWidth, screenHeight):
        self.menuBarColor = (230,238,240)
        self.width = screenWidth
        self.height = int(screenHeight*1.5/10)

        #(x, y, width, height, text=None, fontSize=12, color=Colors.black
        self.changeWeaponButton = TextButton(x=410, y=25, width=120, height=25, text="Change Weapon", fontSize=20, color=Colors.grey)
        self.moreForceButton = TextButton(x=600, y=10, width=50, height=25, text="More", fontSize=20)
        self.lessForceButton = TextButton(x=600, y=40, width=50, height=25, text="Less", fontSize=20)
        self.fireButton = TextButton(x=750, y=25, width=50, height=30, text="FIRE", fontSize=25, color=Colors.red)

        self.buttons = [self.changeWeaponButton, self.moreForceButton, self.lessForceButton, self.fireButton]

    


    def draw(self, win, currentPlayer):
        #-------------------Controlbar and contents of controlbar
        pygame.draw.rect(win, self.menuBarColor, (0,0, self.width, self.height))
        pygame.draw.line(win, (240,248,255), (0,self.height+1), (self.width, self.height+1), 0)

        #--drawing the current player
        pygame.draw.ellipse(win, currentPlayer.tcolor, (0, currentPlayer.turretheight, currentPlayer.twidth, currentPlayer.theight), 0)
        pygame.draw.ellipse(win, currentPlayer.tcolor, (int((currentPlayer.twidth-currentPlayer.turretwidth)/2), 5,currentPlayer.turretwidth,currentPlayer.turretheight),0)

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
