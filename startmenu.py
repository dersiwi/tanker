import pygame
from utilities import message_to_screen, TextButton,Colors

class StartMenu:
    


    def __init__(self, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.playButtonCoordinates = (int(screenWidth * 8/10), int(screenHeight * 6/10))        


        self.terrainBlockX = 150
        self.terrainBlockY = 250
        self.dterrainBlock = 30
        self.fontSizeterrains = 24
        self.fontSizeterrainTitle = 30
        self.colorSelected = Colors.red 
        self.terrainBlock = [["terraintype", Colors.black, self.fontSizeterrainTitle, (self.terrainBlockX, int(self.terrainBlockY))],
                ["Woods", Colors.black, self.fontSizeterrains, (self.terrainBlockX, int(self.terrainBlockY + self.dterrainBlock * 2))],
                ["Dessert", Colors.black, self.fontSizeterrains, (self.terrainBlockX, int(self.terrainBlockY + self.dterrainBlock*3))],
                ["Random", Colors.black, self.fontSizeterrains, (self.terrainBlockX, int(self.terrainBlockY + self.dterrainBlock*4))]]

        self.terrainTypeSelected = None
        
        self.runMenuBool = True
        self.gotoGame = True

        self.playButton = TextButton(
            x = int(screenWidth * 8/10),
            y = int(screenHeight * 6/10),
            text = "PLAY",
            width = 144,
            height = 30,
            fontSize = 40,
            color=Colors.green
            )

    def checkMouseClick(self, pos):
        #this function checks if the mouse clicked any buttons and executes the corresponding action
        x = pos[0]
        y = pos[1]

        selection = 404
        if x > self.terrainBlockX and x < self.terrainBlockX + 90:
            if y > self.terrainBlockY + self.dterrainBlock * 2 and y < self.terrainBlockY + self.dterrainBlock * 4 + 20:
                if y > self.terrainBlockY + self.dterrainBlock * 2 and y < self.terrainBlockY + self.dterrainBlock * 2 + 20:
                    selection = 0
                if y > self.terrainBlockY + self.dterrainBlock * 3 and y < self.terrainBlockY + self.dterrainBlock * 3 + 20:
                    selection = 1
                if y > self.terrainBlockY + self.dterrainBlock * 4 and y < self.terrainBlockY + self.dterrainBlock * 4 + 20:
                    selection = 2
            
                if selection == 0 or selection == 1 or selection == 2:
                    for x in range(1,len(self.terrainBlock)):
                        self.terrainBlock[x][1] = Colors.black
                    if selection == 0:
                        self.terrainBlock[1][1] = self.colorSelected
                        self.terrainTypeSelected = 0
                    elif selection == 1:
                        self.terrainBlock[2][1] = self.colorSelected
                        self.terrainTypeSelected = 1
                    elif selection == 2:
                        self.terrainBlock[3][1] = self.colorSelected
                        self.terrainTypeSelected = 2

        if self.playButton.isClicked(pos):
            self.runMenuBool = False

    def drawMenu(self, win):
            #MENU DRAWING
        message_to_screen(win, "TANKER", Colors.red, 50, (int(self.screenWidth/2-80),int(self.screenHeight/5)))
        self.playButton.draw(win)
        #message_to_screen(win, "PLAY", Colors.green, 40, (int(self.screenWidth * 8/10),int(self.screenHeight * 6/10)))
        
        #terrain Block
        for x in range(len(self.terrainBlock)):
            message_to_screen(win, self.terrainBlock[x][0], self.terrainBlock[x][1], self.terrainBlock[x][2], self.terrainBlock[x][3])
        pygame.display.update()

    def runMenu(self, win):
        while self.runMenuBool:
            pygame.time.delay(100)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runMenuBool = False
                    self.gotoGame = False
                    continue
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #print(pygame.mouse.get_pos())
                    self.checkMouseClick(pygame.mouse.get_pos())


            win.fill(Colors.white)
            
            self.drawMenu(win)
        if not self.gotoGame:
            pygame.quit()

    