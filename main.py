import pygame
import random
#from tankClass import Tank
#from terrainClass import terrain
from tank import Tank, TankInitValues
from gameHandling import Game
from startmenu import StartMenu
from shop import GameShop
from utilities import Colors
from player import Player
from fpsConstants import Globals
from weapons import WeaponsManager
pygame.init()
pygame.font.init()

#screen variables
w_width = Globals.SCREEN_WIDTH
w_height= Globals.SCREEN_HEIGHT
window = (w_width, w_height)
win = pygame.display.set_mode(window)
pygame.display.set_caption("Tanker")




def create_tanks(player_amount):
    player = []
    playerTanks = []
    colors = Colors.playerColors
    colorCounter = 0
    for x in range(player_amount):
        p = Player(x, colors[colorCounter])

        randomX = random.randint(0, 740)
        T = Tank(randomX,100, colors[colorCounter], x + 1, initial_weapons=WeaponsManager.get_instance().get_initial_weapons())
        p.tank = T

        player.append(p)
        playerTanks.append(T)

        colorCounter+=1
        if colorCounter ==len(colors):
            colorCounter = 0
    return player, playerTanks

def main():
    startingMenu = StartMenu(screenWidth=w_width, screenHeight=w_height)
    startingMenu.runMenu(win)

    #gameInitialisation
        
    
    #gameplay
    while True:
        #game = Game(window=win, w_width=w_width, w_height=w_height, terrainType=startingMenu.terrainTypeSelected)
        player, playerTanks = create_tanks(startingMenu.player_selector.get_n_players())
        game = Game(window=win, tanks=playerTanks, terrainType=startingMenu.terrain_selector.terrainTypeSelected)
        game.gameLoop()

        #gameShop = GameShop(w_width, w_height)
        #gameShop.runGameShop(win)

        #for tank in playerTanks:
        #    tank.tLp = TankInitValues.LP

main()
