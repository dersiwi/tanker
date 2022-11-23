import pygame
import random
#from tankClass import Tank
#from terrainClass import terrain
from playerObjects import Tank
from gameHandling import Game
from startmenu import StartMenu
from utilities import Colors
pygame.init()


#screen variables
w_width = int(900)
w_height= int(600)
window = (w_width, w_height)
win = pygame.display.set_mode(window)
pygame.display.set_caption("Tanker")


playerAmount = 2            #the number of players

def main():
    startingMenu = StartMenu(screenWidth=w_width, screenHeight=w_height)
    startingMenu.runMenu(win)

    #gameInitialisation

    playerObjects = []
    for x in range(playerAmount):
        randomX = random.randint(0, 740)
        T = Tank(randomX,100, Colors.black, w_width, x+1)
        playerObjects.append(T)
    
    game = Game(window=win, w_width=w_width, w_height=w_height, terrainType=startingMenu.terrainTypeSelected)
    game.setPlayerTanks(playerObjects)
    game.gameLoop()

main()


