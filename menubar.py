import pygame
from fpsConstants import Globals
from utilities import TextButton, message_to_screen, Colors
from core_objects import Tank, TankGlobals

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

        message_to_screen(win, str(0), Colors.black, 20, (TankGlobals.WIDTH+5,0))

        #--the fuel and the left and right buttons
        message_to_screen(win, str("Fuel: " + str(currentPlayer.fuel)), Colors.black, 20, (TankGlobals.WIDTH+5, 15))
        #left button is missing
        #right button is missing

        #--Livepoints
        message_to_screen(win, str("LP: " + str(currentPlayer.tLp)), Colors.black, 20, (TankGlobals.WIDTH+5, 30))

        #--Weapons and Amount
        stringWeapons = str(currentPlayer.getCurrentWeapon().amount) + " : "
        stringWeapons += str(currentPlayer.getCurrentWeapon().name)
        message_to_screen(win, stringWeapons, Colors.black, 20, (400,5))

        #change v0-Projectile Buttons
        message_to_screen(win, str("Force: " + str(currentPlayer.v0)), Colors.black, 20,(600, 25))

        for button in self.buttons:
            button.draw(win)
