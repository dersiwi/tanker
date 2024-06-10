from core_objects import Tank
from menubar import MenuBar
from fpsConstants import Globals
from weapons import Weapon
from utilities import ConsolePrinter

import random
import pygame, math, time
class Player:
    def __init__(self, name, color, weapons) -> None:
        self.fired = False
        self.name = name
        self.color = color
        self.weapons : list[Weapon] = weapons
        self.tank : Tank = None

    def begin_turn(self):
        """
        This method is called at the beginning of every players turn.
        """
        self.fired = False

    def create_tank(self, x, y) -> Tank:
        self.tank = Tank(x, y, self.color, self.weapons)
        return self.tank 


    def gameloop_iteration(self, keys_pressed, mouse_position) -> bool:
        """
        Handles the input of one game-loop iteration for this player instance.

        @param keys_pressed keys that are pressed in that iteration
        @param mouse_position tuple of (x, y) coordinates if the moues was pressed. (-1, -1) if the mouse
        was not clicked this iteration
        
        @return True, if the playe fired in this iteraiton or not.
        """
        raise NotImplementedError("The Player class is not to be used directly. Initialize subclass instead.")


    def gameshop_iteration(self):
        raise NotImplementedError("The Player class is not to be used directly. Initialize subclass instead.")



    

class HumanPlayer(Player):

    def __init__(self, name, color, weapons) -> None:
        super().__init__(name, color, weapons)
        self.menuBar = MenuBar()



    def gameloop_iteration(self, keys_pressed, mouse_position) -> bool:

        self.check_mouse_pressed(mouse_position)
        self.handleKeyPressed(keys_pressed)
        return self.fired


    def check_mouse_pressed(self, pos):
        if self.menuBar.changeWeaponButton.isClicked(pos):
            self.tank.changeWeapon()

        elif self.menuBar.moreForceButton.isClicked(pos):
            self.tank.changeV(1)

        elif self.menuBar.lessForceButton.isClicked(pos):
            self.tank.changeV(-1)

        elif self.menuBar.fireButton.isClicked(pos):
            self.fired = True


    def handleKeyPressed(self, keys):
        #checks for keys being pressed

        if keys[pygame.K_SPACE]:
            self.fired = True

        if keys[pygame.K_LEFT]:
            self.tank.move(-1)
                
        if keys[pygame.K_RIGHT]:
            self.tank.move(1)
            
        if keys[pygame.K_UP]:
            self.tank.adjust_turret_angle(5)
            
        if keys[pygame.K_DOWN]:
            self.tank.adjust_turret_angle(-5)

        if keys[pygame.K_s]:
            self.tank.deploy_shield()
        if keys[pygame.K_m]:
            self.tank.deploy_mine()

class RandomPlayer(Player):

    NO_ACTION = -1
    DRIVE_LEFT = 0
    DRIVE_RIGHT = 1
    ADJUST_TURRET_LEFT = 2
    ADJUST_TURRET_RIGHT = 3
    INCREASE_V0 = 4
    DECREASE_V0 = 5
    CHANGE_WEAPON = 6

    FIRE_CHANGE = 0.2

    MIN_ACTION_DURATION = 2
    MAX_ACTION_DURATION = 20

    ACTIONS = [DRIVE_LEFT, DRIVE_RIGHT, ADJUST_TURRET_LEFT, ADJUST_TURRET_RIGHT, INCREASE_V0, DECREASE_V0, CHANGE_WEAPON]
    MIN_ACTION_DURATION = [5, 5, 5, 5, 1, 1, 1]
    MAX_ACTION_DURATION = [25, 25, 15, 15, 5, 5, 10]

    def __init__(self, name, color, weapons) -> None:
        super().__init__(name, color, weapons)

        self.current_action = RandomPlayer.NO_ACTION
        self.action_duration = 10

    def gameloop_iteration(self, keys_pressed, mouse_position) -> bool:

        #if the randomplayer has an action selected, it does the selecd action until its duration is over.
        if not self.current_action == RandomPlayer.NO_ACTION:
            self.__do_action()
            return False


        if random.random() < RandomPlayer.FIRE_CHANGE:
            return True

        self.__choose_random_action()
        self.__do_action()

    def __do_action(self):
        """
        Executes the currently selected action and decrements the duration of that action.
        If the duration is zero, it sets the current_action to NO_ACTOIN.
        """
        if self.current_action == RandomPlayer.DRIVE_LEFT:
            self.tank.move(-1)
                
        elif self.current_action == RandomPlayer.DRIVE_RIGHT:
            self.tank.move(1)
            
        elif self.current_action == RandomPlayer.ADJUST_TURRET_RIGHT:
            self.tank.adjust_turret_angle(5)
            
        elif self.current_action == RandomPlayer.ADJUST_TURRET_LEFT:
            self.tank.adjust_turret_angle(-5)
        
        elif self.current_action == RandomPlayer.CHANGE_WEAPON:
            self.tank.changeWeapon()
        elif self.current_action == RandomPlayer.INCREASE_V0:
            self.tank.changeV(1)
        elif self.current_action == RandomPlayer.DECREASE_V0:
            self.tank.changeV(-1)
        
        self.action_duration -= 1

        if self.action_duration <= 0:
            self.current_action = RandomPlayer.NO_ACTION

    def get_pos_for_projectile(self):
        x = random.randint(50, Globals.SCREEN_WIDTH - 50)
        y = random.randint(50, Globals.SCREEN_HEIGHT - 50)
        return (x,y)

    def __choose_random_action(self):
        """
        Chooses a random aciton and a duration.
        """
        self.current_action = random.randint(min(RandomPlayer.ACTIONS), max(RandomPlayer.ACTIONS))
        self.action_duration = random.randint(RandomPlayer.MIN_ACTION_DURATION[self.current_action],
                                              RandomPlayer.MAX_ACTION_DURATION[self.current_action])
        

class SmartComputerPlayer(Player):

    def __init__(self, name, color, weapons) -> None:
        super().__init__(name, color, weapons)
        self.other_players : list[Player] = None
        self.target_player : Player = None
        self.alpha : float = 0
        self.v0 : float = 0

    def set_other_player(self, other_players : list[Player]) -> None:
        self.other_players = other_players


    def begin_turn(self):
        """
        In this method the smart-computer player chooses a target
        """
        self.fired = False
        self.target_player = random.choice(self.other_players)
        if self.target_player.tank.tLp <= 0:
            self.target_player = self.__get_first_living()
        ConsolePrinter.print("Player %s aquired target %s"%(self.name, self.target_player.name), print_level=ConsolePrinter.VERBOSE)

        alpha, v0 = self.__calculate_turret_angle_and_force()

        self.tank.turretAngle = alpha
        self.tank.v0 = v0
    
    def __calculate_turret_angle_and_force(self) -> tuple[float, float]:
        """
        Calculates angle alpha and force v0
        """
        #max height of the projectile.
        distance = abs(self.tank.x - self.target_player.tank.x)
        h_max = distance / 2 + self.tank.x

        GRAVITY = Globals.GRAVITY / Globals.FPS.FPS

        vY = (h_max -  self.tank.x) * 2 * GRAVITY
        vX = distance / (math.sqrt((2*distance) / GRAVITY) + vY / GRAVITY)
        v0 = math.sqrt(vX**2 + vY ** 2)
        alpha_in_degrees = math.asin(vY/v0) * 180 / math.pi

        ConsolePrinter.print("SmartComputer Target Calculation: x-Distance to target %i, h_max = %.2f, vY = %.2f, vX = %.2f, v0=%.2f, alpha = %.2f"%(distance, h_max, vY, vX, v0, alpha_in_degrees), 
                             print_level=ConsolePrinter.VERBOSE)
        
        return alpha_in_degrees, v0

    
    def gameloop_iteration(self, keys_pressed, mouse_position) -> bool:      
        #somehow shoot the target

        return True

    def get_pos_for_projectile(self):
        x = random.randint(50, Globals.SCREEN_WIDTH - 50)
        y = random.randint(50, Globals.SCREEN_HEIGHT - 50)
        return (x,y)

    
    def __get_first_living(self):
        for player in self.other_players:
            if player.tank.tLp > 0:
                return player
        

    def gameshop_iteration(self):
        raise NotImplementedError("The Player class is not to be used directly. Initialize subclass instead.")