import pygame
from utilities import message_to_screen, Colors

class MenuBar:
    def __init__(self, screenWidth, screenHeight):
        self.menuBarColor = (230,238,240)
        self.width = screenWidth
        self.height = int(screenHeight*1.5/10)

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

        #--cahngeWeaponButton
        message_to_screen(win, "Change Weapon", Colors.grey, 20, (410, 25))

        #change v0-Projectile Buttons
        message_to_screen(win, str("Force: " + str(currentPlayer.v0)), Colors.black, 20,(600, 25))
        message_to_screen(win, "More", Colors.black, 20,(600, 10))
        message_to_screen(win, "Less", Colors.black, 20,(600, 40))

        #a fire Button
        message_to_screen(win, "FIRE", Colors.red, 25, (750, 25))