import random
import sys
import argparse
import pygame


from gameHandling import Game
from menus.startmenu import StartMenu, PlayerSelector, TerrainType
from menus.shop import GameShop
from utils.utilities import Colors, ConsolePrinter
from player import Player, HumanPlayer, RandomPlayer, SmartComputerPlayer
from utils.fpsConstants import Globals
from weapons.weapons import WeaponsManager
from gameobjects.gameobject import GameObjectHandler


#define args and argparser
parser = argparse.ArgumentParser(
    prog="tanker",
    description="2d tank game"
)
parser.add_argument("-c", "--console_level", type=int, default=ConsolePrinter.NOTHING,
                    help="Defines console messages to be displayed. 0 (debug), 1(regular), 2(verbose), 3(all)")
parser.add_argument("-s", "--shop", action="store_true", default=False, help="If typed, the program jumpts to the store without starting the game.")
parser.add_argument("-t", "--throw", action="store_true", help="If called with this flag, an exception in the main method is thrown.")
args = parser.parse_args()


throw_exception_in_main = args.throw
ConsolePrinter.PRINT_LEVEL = args.console_level



pygame.init()
pygame.font.init()

#screen variables
w_width = Globals.SCREEN_WIDTH
w_height= Globals.SCREEN_HEIGHT
window = (w_width, w_height)
win = pygame.display.set_mode(window)
pygame.display.set_caption("Tanker")



def test_random_players(n_players : int = 4):
    #create players
    players : list[Player] = []
    for i in range(n_players):
        players.append(
            RandomPlayer(name=i, 
                        color=Colors.playerColors[i % len(Colors.playerColors)], 
                        weapons =  WeaponsManager.get_instance().get_initial_weapons())
        )

    #gameplay
    while True:
        GameObjectHandler.destroy_instance()
        game = Game(window=win, players=players, terrain_id=TerrainType.RANDOM)
        game.gameLoop()
    
        gameshop = GameShop(players)
        gameshop.runGameShop(win)
        for player in players:
            player.create_tank(x = random.randint(0, Globals.SCREEN_WIDTH), y = 200)

try:
    test_random_players()
except Exception as e:
    ConsolePrinter.print("Exception in main method", print_level=ConsolePrinter.DEBUG)
    ConsolePrinter.print(str(e.args), print_level=ConsolePrinter.DEBUG)
    if throw_exception_in_main:
        raise e
