
from utilities import Colors, TextButton
from weapons import Weapon
from fpsConstants import FPS
import pygame

class GameShop:

    clock = pygame.time.Clock()
    def __init__(self, screenWidth, screenHeight):

        self.runningGameShop = True
        self.gotoGame = True

        self.shopButtonMargins = 5

        self.startXForButtons = int(screenWidth * 1 / 8)
        self.startYForButtons = int(screenHeight * 1 / 4)
        self.anticipatedYDistance = 50
        self.itemFontSize = 24

        self.buttonWidth = 200
        #x, y, text=None, fontSize=12, color=Colors.black
        self.smallMissileButton = TextButton(self.startXForButtons, 0, Weapon.getSmallMissile().name ,self.itemFontSize)
        self.vulcanoBombButton = TextButton(self.startXForButtons, 0, Weapon.getVulcanoBomb().name, self.itemFontSize)
        self.ballButton = TextButton(self.startXForButtons, 0, Weapon.getBall().name, self.itemFontSize)
        self.bigBallButton = TextButton(self.startXForButtons, 0, Weapon.getBigBall().name, self.itemFontSize)

        self.shopButtons = [self.smallMissileButton, self.vulcanoBombButton, self.ballButton, self.bigBallButton]

        #set the distance for all buttons
        for x in range(len(self.shopButtons)):
            self.shopButtons[x].y = self.startYForButtons + x * self.anticipatedYDistance

        for b in self.shopButtons:
            b.addBackground()
            b.setMargin(self.shopButtonMargins)
            b.addBorder()
            b.setWidth(self.buttonWidth)

        #return to playing button
        self.resumePlayingWidth = 200
        self.resumePlayingFontSize = 30
        self.resumePlaying = TextButton(int((screenWidth - self.resumePlayingWidth) / 2), int(screenHeight * 3/4), "Resume playing", self.resumePlayingFontSize, Colors.green)
        self.resumePlaying.setMargin(self.shopButtonMargins)
        self.resumePlaying.addBorder()
        self.resumePlaying.setWidth(self.resumePlayingWidth)

        self.shopButtons.append(self.resumePlaying)
        pass

    def checkMouseClick(self, pos):
        if self.resumePlaying.isClicked(pos):
            self.runningGameShop = False
        pass

    def runGameShop(self, win):
        while self.runningGameShop:
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runningGameShop = False
                    self.gotoGame = False
                    continue
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #print(pygame.mouse.get_pos())
                    self.checkMouseClick(pygame.mouse.get_pos())
            win.fill(Colors.white)
            self.draw(win)
            GameShop.clock.tick(FPS.FPS)

            pygame.display.update()
            
        if not self.gotoGame:
            pygame.quit()

    def draw(self, win):
        for b in self.shopButtons:
            b.draw(win)
        
        