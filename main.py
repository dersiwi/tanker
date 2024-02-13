import pygame
import random
#from tankClass import Tank
#from terrainClass import terrain
from core_objects import Tank
from gameHandling import Game
from startmenu import StartMenu, PlayerSelector
from shop import GameShop
from utilities import Colors
from player import Player, HumanPlayer, RandomPlayer
from fpsConstants import Globals
from weapons import WeaponsManager
from gameobject import GameObjectHandler
pygame.init()
pygame.font.init()

#screen variables
w_width = Globals.SCREEN_WIDTH
w_height= Globals.SCREEN_HEIGHT
window = (w_width, w_height)
win = pygame.display.set_mode(window)
pygame.display.set_caption("Tanker")




def create_players(player_types):
    player = []

    for x, ptype in enumerate(player_types):

        if ptype == PlayerSelector.PlayerType.HUMAN:
            p = HumanPlayer(name=x, 
                            color=Colors.playerColors[x % len(Colors.playerColors)], 
                            weapons =  WeaponsManager.get_instance().get_initial_weapons())
        elif ptype == PlayerSelector.PlayerType.RANDOM:
            p = RandomPlayer(name=x, 
                             color=Colors.playerColors[x % len(Colors.playerColors)], 
                             weapons =  WeaponsManager.get_instance().get_initial_weapons())
            
        elif ptype == PlayerSelector.PlayerType.AI:
            raise NotImplementedError("Ai not implemented yet")
        
        p.create_tank(x = random.randint(0, Globals.SCREEN_WIDTH), y = 200)
        player.append(p)

    return player

def main():
    startingMenu = StartMenu(screenWidth=w_width, screenHeight=w_height)
    startingMenu.runMenu(win)

    #gameInitialisation
    players : list[Player] = create_players(startingMenu.player_selector.get_player_types())
    
    
    #gameplay
    while True:
        GameObjectHandler.destroy_instance()
        game = Game(window=win, players=players, terrain_id=startingMenu.terrain_selector.terrainTypeSelected)
        game.gameLoop()
        
        gameshop = GameShop(players)
        gameshop.runGameShop(win)
        for player in players:
            player.create_tank(x = random.randint(0, Globals.SCREEN_WIDTH), y = 200)
        
        

main()
