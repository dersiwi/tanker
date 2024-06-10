import random
import sys
import argparse
import pygame


from gameHandling import Game
from startmenu import StartMenu, PlayerSelector
from shop import GameShop
from utilities import Colors, ConsolePrinter
from player import Player, HumanPlayer, RandomPlayer
from fpsConstants import Globals
from weapons import WeaponsManager
from gameobject import GameObjectHandler


#define args and argparser
parser = argparse.ArgumentParser(
    prog="tanker",
    description="2d tank game"
)
parser.add_argument("-c", "--console_level", type=int, default=ConsolePrinter.NOTHING,
                    help="Defines console messages to be displayed. 0 (debug), 1(regular), 2(verbose).")
parser.add_argument("-s", "--shop", action="store_true", default=False, help="If typed, the program jumpts to the store without starting the game.")
parser.add_argument("-t", "--throw", action="store_true", help="If called with this flag, an exception in the main method is thrown.")
args = parser.parse_args()


goto_shop = args.shop
throw_exception_in_main = args.throw
ConsolePrinter.PRINT_LEVEL = args.console_level
ConsolePrinter.print("Console printer level : %i, gotoshop : %s"%(ConsolePrinter.PRINT_LEVEL, goto_shop), 
                     print_level=ConsolePrinter.DEBUG)




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
        if not goto_shop:
            GameObjectHandler.destroy_instance()
            game = Game(window=win, players=players, terrain_id=startingMenu.terrain_selector.terrainTypeSelected)
            game.gameLoop()
        
        gameshop = GameShop(players)
        gameshop.runGameShop(win)
        for player in players:
            player.create_tank(x = random.randint(0, Globals.SCREEN_WIDTH), y = 200)

try:
    main()
except Exception as e:
    ConsolePrinter.print("Exception in main method", print_level=ConsolePrinter.DEBUG)
    ConsolePrinter.print(str(e.args), print_level=ConsolePrinter.DEBUG)
    if throw_exception_in_main:
        raise e
