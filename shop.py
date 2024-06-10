
from utilities import Colors, TextButton, message_to_screen, ConsolePrinter
from weapons import Weapon, WeaponsManager
from fpsConstants import Globals
import pygame
from player import Player
from core_objects import Tank

class GameShop:

    START_X = int(Globals.SCREEN_WIDTH * 1 / 8)
    START_Y = int(Globals.SCREEN_WIDTH * 1 / 4)
    FONTSIZE = 24
    BUTTON_MARGIN = 5



    clock = pygame.time.Clock()
    def __init__(self, players):

        self.players : list[Player] = players
        self.current_player = 0

        self.runningGameShop = True

        self.curr_weapon_type = Weapon.TYPE_0

        self.weapons_buttons : dict[int, list[TextButton]] = {}
        self.__create_weapons_buttons()
        self.resumePlaying : TextButton = self.__generate_shopbutton(int((Globals.SCREEN_WIDTH - 200) / 2), int(Globals.SCREEN_HEIGHT * 3/4), 
                                           "Next Player", Colors.green)
        
        self.switchWeaponType : TextButton = self.__generate_shopbutton(GameShop.START_X, int(Globals.SCREEN_HEIGHT * 1/4),
                                                                        "switch weapon type",  Colors.grey)


    def __generate_shopbutton(self, x, y, text, color):
        return TextButton(x, y, text, GameShop.FONTSIZE, color, border=True, margin=GameShop.BUTTON_MARGIN)

    def __create_weapons_buttons(self):
        wm = WeaponsManager.get_instance()
        for weapon_type in Weapon.TYPES:
            self.weapons_buttons[weapon_type] = []
            for i, weapon in enumerate(wm.weapons[weapon_type]):
                self.weapons_buttons[weapon_type].append(
                    self.__generate_shopbutton(GameShop.START_X, GameShop.START_Y + i * 2 * GameShop.FONTSIZE, weapon.name, Colors.black))
                
    def checkMouseClick(self, pos):
        if self.resumePlaying.isClicked(pos):
            if self.current_player < len(self.players) - 2:
                self.current_player += 1
            elif self.current_player == len(self.players) - 2:
                self.current_player += 1
                self.resumePlaying.setText("Resume Game")
            elif self.current_player >= len(self.players) - 1:
                #last players turn is now finished
                self.runningGameShop = False

        if self.switchWeaponType.isClicked(pos):
            self.curr_weapon_type = (self.curr_weapon_type + 1) % len(Weapon.TYPES)
        for idx, weapon_button in enumerate(self.weapons_buttons[self.curr_weapon_type]):
            if weapon_button.isClicked(pos):
                ConsolePrinter.print("Player %s bought %s - pricing not implemeneted yet"%(self.players[self.current_player].name, weapon_button.text), 
                                     print_level=ConsolePrinter.VERBOSE)
                self.__add_weapon_to_player(WeaponsManager.get_instance().weapons[self.curr_weapon_type][idx].get_copy())

    def __add_weapon_to_player(self, weapon : Weapon):
        for we in self.players[self.current_player].weapons:
            if we.name == weapon.name:
                we.amount += weapon.amount
                return
        self.players[self.current_player].weapons.append(weapon)
        

    def runGameShop(self, win):
        gotoGame = True
        while self.runningGameShop:
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runningGameShop = False
                    gotoGame = False
                    continue
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.checkMouseClick(pygame.mouse.get_pos())
            win.fill(Colors.white)
            self.draw(win)
            GameShop.clock.tick(Globals.FPS.FPS)

            pygame.display.update()
        if not gotoGame:
            pygame.quit()

    def draw(self, win):
        message_to_screen(win, "Player : %s"%self.players[self.current_player].name, color = Colors.black, fontSize=GameShop.FONTSIZE, 
                          fontKoordinaten=(int(Globals.SCREEN_WIDTH / 2), 100))
        curPtank = self.players[self.current_player].tank
        curPtank.tank_graphics.draw(win, int(Globals.SCREEN_WIDTH / 2) + 125, 100, 
                                                                  Tank.calculateTurretEndPos(int(Globals.SCREEN_WIDTH / 2) + 125, 100, 
                                                                                             curPtank.turretAngle))

        self.resumePlaying.draw(win)
        self.switchWeaponType.draw(win)
        for button in self.weapons_buttons[self.curr_weapon_type]:
            button.draw(win)

        
        