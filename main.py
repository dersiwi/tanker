import pygame
import random
#from tankClass import Tank
#from terrainClass import terrain
from tank import Tank
from gameHandling import Game
from startmenu import StartMenu
from utilities import Colors
from player import Player
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

    colors = Colors.playerColors
    colorCounter = 0

    player = []
    playerTanks = []

    for x in range(playerAmount):
        p = Player(x, colors[colorCounter])

        randomX = random.randint(0, 740)
        T = Tank(randomX,100, colors[colorCounter], w_width, x + 1)
        p.tank = T

        player.append(p)
        playerTanks.append(T)

        colorCounter+=1
        if colorCounter ==len(colors):
            colorCounter = 0

    
        
        

    #gameplay
    
    #game = Game(window=win, w_width=w_width, w_height=w_height, terrainType=startingMenu.terrainTypeSelected)
    game = Game(window=win, w_width=w_width, w_height=w_height, terrainType=1)
    game.setPlayerTanks(playerTanks)
    game.gameLoop()

main()


