import pygame
import random
#from tankClass import Tank
#from terrainClass import terrain
from tank import Tank
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


playerAmount = 4       #the number of players



def main():
    #startingMenu = StartMenu(screenWidth=w_width, screenHeight=w_height)
    #startingMenu.runMenu(win)

    #gameInitialisation

    playerObjects = []
    colors = Colors.playerColors
    colorCounter = 0
    for x in range(playerAmount):
        randomX = random.randint(0, 740)
        T = Tank(randomX,100, colors[colorCounter], w_width, x+1)
        colorCounter+=1
        if colorCounter ==len(colors):
            colorCounter = 0
        playerObjects.append(T)

    #gameplay
    
    #game = Game(window=win, w_width=w_width, w_height=w_height, terrainType=startingMenu.terrainTypeSelected)
    game = Game(window=win, w_width=w_width, w_height=w_height, terrainType=1)
    game.setPlayerTanks(playerObjects)
    game.gameLoop()

main()


