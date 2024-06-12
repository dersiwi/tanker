from core_objects import Terrain, Sun
from utilities import Colors, message_to_screen
from fpsConstants import Globals
from gameobject import GameObjectHandler
from player import Player, HumanPlayer
from weapons import Weapon_Executor
from menubar import MenuBar

import pygame



"""
    This class is supposed to run the game-loop
    Meaning it generates the terrain for one round, handles drawing and game objects for this round

    However, it does not know about the start-menu or the shop. Player (Tanks) are created somewhere else and only given to 
    the Game-class.

    The game-class has a run method which actually runs the game-loop, draws all objcets
"""
class Game:

    clock = pygame.time.Clock()

    STAGE_ONE = 1
    STAGE_TWO = 2

    ITERATIONS_TIL_START = 30
    """
    Amount of gameloop-iterations until the players can actually do something.
    in this time the players fall to the ground form the sky.
    """


    def __init__(self, window, players : list[Player], terrain_id : int):

        self.window = window
        self.runGameLoop = True

        #-------------gameplay variables
        self.game_object_handler : GameObjectHandler = GameObjectHandler.get_instance()
            
        for player in players:
            self.game_object_handler.add_gameobject(player.tank)

        self.playerTurn  : int = 0
        self.player : list[Player] = players
        self.current_player : Player = self.player[self.playerTurn]


        #-------------------------------initialize static game objects Sun, Terrain, MenuBar
        self.terrain = Terrain(terrain_id)

        self.game_object_handler.add_gameobject(Sun())
        self.game_object_handler.add_gameobject(self.terrain)

        self.menuBar = MenuBar()
        self.projectile : Weapon_Executor = None

        self.show_help_menu : bool = False

    
    """
        Return the next player in playerObjects. A player can only be chosen, if he has > 0 LP
        This method also removes all 'dead' players from playerObjects

        If <= 1 player are alive this method sets self.runGameLoop to false
    """
    def nextPlayer(self):
        self.stage = Game.STAGE_ONE

        for i in range(1, len(self.player)):
            self.playerTurn = (self.playerTurn + i) % len(self.player)
            self.current_player = self.player[self.playerTurn]

            if self.current_player.tank.tLp > 0:
                self.current_player.begin_turn()
                return
            
        self.runGameLoop = False



    def fire(self):
        if self.stage == Game.STAGE_ONE:
            self.stage = Game.STAGE_TWO

            currentPlayerTank = self.current_player.tank
            
            self.projectile = currentPlayerTank.get_weapon_executor()
            self.game_object_handler.add_gameobject(self.projectile)
            currentPlayerTank.fire()

    """
        Handle all key-pressed events that are happening
    """


    def redrawGame(self):
        """
        Calls for gameobject handler and menu bar to draw themeslves
        """
        #GAME LOOP DRAWING
        #--------------------terrain drawing
        self.game_object_handler.draw_gameobjects(self.window)
        self.menuBar.draw(self.window, self.current_player.tank) 
        pygame.display.update()
    


    def __stage_one_iteration(self) -> bool:
        mouse_pos = (-1, -1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.runGameLoop = False
                self.quitGame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        self.show_help_menu = keys[pygame.K_h]
        if self.current_player.gameloop_iteration(keys_pressed= keys, mouse_position=mouse_pos):
            self.fire()

    def __stage_two_iteration(self):
        pos = (-1, -1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.runGameLoop = False
                self.quitGame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
           
        self.show_help_menu = pygame.key.get_pressed()[pygame.K_h]

        if not type(self.current_player) == HumanPlayer:
            pos = self.current_player.get_pos_for_projectile()

        self.projectile.projectile_iteration(pos)
        

    def check_if_live(self) -> bool:
        """this method checks if still more than two players are alive   @return true, if tanks are still alive"""
        alive = 0
        for player in self.player:
            if player.tank.tLp <= 0 or player.tank.y >= Globals.SCREEN_HEIGHT:
                if not player.tank.removed_from_objecthandler:
                    self.game_object_handler.remove_gameobject(player.tank)
                    player.tank.removed_from_objecthandler = True
            else:
                alive += 1
        return alive >= 2
    

    def display_help_menu(self):
        helpstrings = ["Move left      : <", "Move right     : >", "Turret right   : up", "Turret down    : down",  "fire           : space", "deploy mine  : m",]
        for i, helpstring in enumerate(helpstrings):
            message_to_screen(self.window, msg=helpstring, color=Colors.black, fontSize=25, fontKoordinaten=(300, 200 + i * 25))

            

    def gameLoop(self):
        """
        Runs the game-loop. This method works in two stages for ecah player
            Stage 1 - Adjusting Stage:
                The player can drive around, change weapons, adjust force etc.
                As soon as the player fires, this switches to stage two
            Stage 2 - Projectile Stage:
                The player has fired and the "projcetile is in the air". During this phase "the projectile" has the opportunity 
                to accept player input if wanted - e.g. airstrike.
                The phase (and thereby the player turn) ends when projectile.hasCollided == True.
        """
        self.runGameLoop = True
        self.quitGame = False
        self.stage = Game.STAGE_ONE
        self.current_player.begin_turn()
        iteration = 0
        while self.runGameLoop:

            if iteration > Game.ITERATIONS_TIL_START:
            
                if self.stage == Game.STAGE_ONE:
                    self.__stage_one_iteration()
                elif self.stage == Game.STAGE_TWO:
                    self.__stage_two_iteration()
                else:
                    raise ValueError("Unknown stage %i."%self.stage)

            if not self.projectile == None and self.projectile.hasCollided:
                self.projectile = None
                self.nextPlayer()

            if not self.check_if_live():
                self.runGameLoop = False

            self.window.fill(Colors.skyblue)
            if self.show_help_menu:
                self.display_help_menu()
            self.game_object_handler.update()
            Game.clock.tick(Globals.FPS.FPS)

            #das ist nur eine Provisorische Abfrage um bugs uz vermeiden
            if self.current_player.tank.tLp == 0:
                self.nextPlayer()
            self.redrawGame()
            iteration += 1
        if self.quitGame:
            pygame.quit()


