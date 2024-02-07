import pygame
import random
#from tankClass import Tank
#from terrainClass import terrain
from tank import Tank, TankInitValues
from gameHandling import Game
from startmenu import StartMenu, PlayerSelector
from shop import GameShop
from utilities import Colors
from player import Player, HumanPlayer, RandomPlayer
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




def create_tanks(player_types):
    player = []
    playerTanks = []
    colors = Colors.playerColors
    colorCounter = 0
    for x, ptype in enumerate(player_types):

        randomX = random.randint(0, 740)
        T = Tank(randomX,100, colors[colorCounter], x + 1, initial_weapons=WeaponsManager.get_instance().get_initial_weapons())

        if ptype == PlayerSelector.PlayerType.HUMAN:
            p = HumanPlayer(name=x, color=colors[colorCounter], tank=T)
        elif ptype == PlayerSelector.PlayerType.RANDOM:
            p = RandomPlayer(name=x, color=colors[colorCounter], tank=T)
        elif ptype == PlayerSelector.PlayerType.AI:
            raise NotImplementedError("Ai not implemented yet")


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
        player, playerTanks = create_tanks(startingMenu.player_selector.get_player_types())
        game = Game(window=win, players=player, terrainType=startingMenu.terrain_selector.terrainTypeSelected)
        game.gameLoop()

        #gameShop = GameShop(w_width, w_height)
        #gameShop.runGameShop(win)

        #for tank in playerTanks:
        #    tank.tLp = TankInitValues.LP

main()
