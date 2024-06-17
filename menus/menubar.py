import pygame
from utils.fpsConstants import Globals
from utils.utilities import TextButton, message_to_screen, Colors
from gameobjects.core_objects import Tank, TankGlobals
import json


class MenuBarLoader:
    """This class is responsible for loading menubar contents like color, width etc."""
    PATH ="data\menus.json"

    def __init__(self) -> None:
        with open(MenuBarLoader.PATH, "r") as file:
            menudict = json.load(file)
        self.info = menudict["menubar"]

class MenuBar:
    """
    Menubar is displayed at the top of the screen when playing the game. The menu bar contains visuals and 
    buttons for the player to see for example the force, left ammo and lifepoints.
    """
    def __init__(self):
        mbLoader = MenuBarLoader()
        self.menuBarColor = mbLoader.info["color"]
        self.width = int(mbLoader.info["width"]*Globals.SCREEN_WIDTH)
        self.height = int(mbLoader.info["height"]*Globals.SCREEN_HEIGHT)

        #(x, y, width, height, text=None, fontSize=12, color=Colors.black
        self.changeWeaponButton = TextButton.from_json_dict(mbLoader.info["change_weapon_button"])
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


