class TankerStartMenu:

    pygame = None


    shopBlock = ["Small Atom Bomb", 10000, 1, 20, black, (40,40)]

    playButtonCoordinates = (int(w_width * 8/10), int(w_height * 6/10))

    def __init__(self, py):
        self.pygame = py
        
    '''
    Start menup

    '''
    def startMenu():
        global menuRun
        while menuRun:
            self.pygame.time.delay(100)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menuRun = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #print(pygame.mouse.get_pos())
                    checkMouseClickMenu(pygame.mouse.get_pos())


            win.fill(white)
            
            redrawMenu()
        if gotoGame == False:
            pygame.quit()


    def redrawMenu(self):
        #MENU DRAWING
        message_to_screen("TANKER", red, 50, (int(w_width/2-80),int(w_height/5)))
        message_to_screen("PLAY", green, 40, playButtonCoordinates)
        #Terrain Block
        for x in range(len(terrainBlock)):
            message_to_screen(terrainBlock[x][0],terrainBlock[x][1],terrainBlock[x][2],terrainBlock[x][3])
        #circle(surface, color, center, radius)
        #for x in range(2,5):
        #    pygame.draw.circle(win, black, (int(terrainBlockX-fontSizeTerrains/2), terrainBlockY +dTerrainBlock * x + int(bulletpointRadius*1.5)) ,bulletpointRadius)
        pygame.display.update()


    def message_to_screen(msg, color, fontSize, fontKoordinaten):
        font = pygame.font.SysFont(None, fontSize)
        screen_text = font.render(msg, True, color)
        win.blit(screen_text, fontKoordinaten)
        

