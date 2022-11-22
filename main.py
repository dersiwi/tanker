import pygame
import math
import random
from tankClass import Tank
from terrainClass import Terrain
pygame.init()


#screen variables
w_width = int(900)
w_height= int(600)
window = (w_width, w_height)


#colors
ingame_menubar_backgroundcolor = (179,179,179)
wind_background = (255,255,255)
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
grey = (110,110,110)
forest_green = (34,139,34)
skyblue = (176,226,255)

#Terrain initialisation
Terrain = Terrain(w_width, w_height)
#Terrain.generate(0)
'''
Tank = Tank(100,100, black, w_width)
'''
#window 
win = pygame.display.set_mode(window)
pygame.display.set_caption("Tanker")



#menu-variables
menuRun = True              #needs to be a global variable
gotoGame = False            #this is only used to close the while loop without quitting pygame
terrainSelected = False     #this is so the player can only play if he selected a terrain Type 
terrainTypeSelected = 404   #this is the default value if anything hasent been specified yet
#menu spcifications Terrain Block
terrainBlockX = 150         #X-Koordinaten Terrainblock
terrainBlockY = 250         #y-koordinaten der Terrainüberschrift
dTerrainBlock = 30
fontSizeTerrainTitle = 30   #überschrift für Terrains
fontSizeTerrains = 24       #Die Terraintypes selbst; %2=0 sollte gelten; font size 24 ~= 32 px
bulletpointRadius = 6       #sollte mit 1.5 mulipliziert eine ganze Zahl seinn
colorSelected = red         #das ist die font farbe für das ausgewählte terrain

terrainBlock = [["Terraintype", black, fontSizeTerrainTitle, (terrainBlockX, int(terrainBlockY))],
                ["Woods", black, fontSizeTerrains, (terrainBlockX, int(terrainBlockY + dTerrainBlock * 2))],
                ["Dessert", black, fontSizeTerrains, (terrainBlockX, int(terrainBlockY + dTerrainBlock*3))],
                ["Random", black, fontSizeTerrains, (terrainBlockX, int(terrainBlockY + dTerrainBlock*4))]]

#["Woods", black, fontSizeTerrains, (x, y), (x-center-circle, y-center-circle)

playButtonCoordinates = (int(w_width * 8/10), int(w_height * 6/10))        #font-size: 40


#---------------------INGAME VARIABLES
playerAmount = 2            #the number of players
playerObjects = []          #stores every Player object 
playerTurn = 0              #Stores the index of the current player objects turn (if its player 1s turn its 0)


#--------------------Drawing Variables (GameLoop)

menuBarHeight = int(w_height*1.5/10)
menuBarColor = (230,238,240)
projectileGoing = False
SpeedRoundX = 0
SpeedRoundY = 10
bulletPosition = [0,0]
gravity = 5

#-------------------Variables for menu after gameLoop
gotoMenu = False            #this prevents the game from quitting pygame and so just ends the functin 
runGameLoop = True          #this is the boolean responsible for running the gameLoop
menuRoundRun = True         #this is the boolean responsible for running the menu Loop

shopBlock = ["Small Atom Bomb", 10000, 1, 20, black, (40,40)]
#shopBlock = ["Name", cost, amountPerBuy, fontSize, fonColor, (x-position, y-position)]

#----------------------FUNCTIONAL FUNCTIONS------------------------------------

def checkMouseClickMenu(pos):
    global terrainTypeSelected
    global terrainSelected
    global menuRun
    global gotoGame
    #this function checks if the mouse clicked any buttons and executes the corresponding action
    x = pos[0]
    y = pos[1]

    selection = 404
    if x > terrainBlockX and x < terrainBlockX + 90:
        if y > terrainBlockY + dTerrainBlock * 2 and y < terrainBlockY + dTerrainBlock * 4 + 20:
            if y > terrainBlockY + dTerrainBlock * 2 and y < terrainBlockY + dTerrainBlock * 2 + 20:
                selection = 0
            if y > terrainBlockY + dTerrainBlock * 3 and y < terrainBlockY + dTerrainBlock * 3 + 20:
                selection = 1
            if y > terrainBlockY + dTerrainBlock * 4 and y < terrainBlockY + dTerrainBlock * 4 + 20:
                selection = 2
        
            if selection == 0 or selection == 1 or selection == 2:
                terrainSelected = True
                for x in range(1,len(terrainBlock)):
                    terrainBlock[x][1] = black
                if selection == 0:
                    terrainBlock[1][1] = colorSelected
                    terrainTypeSelected = 0
                elif selection == 1:
                    terrainBlock[2][1] = colorSelected
                    terrainTypeSelected = 1
                elif selection == 2:
                    terrainBlock[3][1] = colorSelected
                    terrainTypeSelected = 2

    if x > playButtonCoordinates[0] and playButtonCoordinates[0] + 144:
        if y > playButtonCoordinates[1] and  y < playButtonCoordinates[0] + 30:
            if terrainSelected == True:
                gotoGame = True
                menuRun = False
                
    #int(w_width * 8/10), int(w_height * 6/10)

def checkMouseClickGame(pos):
    x = pos[0]
    y = pos[1]

    #"Change Weapon", black, 20, (410, 25)
    if x >= 410 and x < 410 + 120:
        if y >= 25 and y <= 25+25:
            playerObjects[playerTurn].changeWeapon()
            
    #message_to_screen("More", black, 20,(600, 10))
    #message_to_screen("Less", black, 20,(600, 40))
    if x > 600 and x < 600+50:
        if y > 10 and y < 10 + 25:
            playerObjects[playerTurn].changeV(1)
        if y > 40 and y < 40 + 25:
            playerObjects[playerTurn].changeV(-1)

    #message_to_screen("FIRE", red, 25, (750, 25))
    if x > 750 and x < 750 + 50:
        if y > 25 and y < 25 + 30:
            if not projectileGoing:
                fire()

def checkMouseClickShopMenu(pos):
    x = pos[0]
    y = pos[1]
    pass

def nextPlayer():
    global playerTurn, gotoMenu, runGameLoop
    amountLiving = 0
    for Tank in playerObjects:
        if Tank.tLp > 0:
            amountLiving += 1
    if amountLiving <= 1:
        gotoMenu = True
        runGameLoop = False
        return

    
    len(playerObjects)
    if playerTurn == len(playerObjects) - 1:
        playerTurn = 0 
    else:
        playerTurn += 1

    #this ensures that no dead player can have turns
    if playerObjects[playerTurn].tLp <= 0:
        nextPlayer()

def fire():
    global projectileGoing, bulletPosition, SpeedRoundX, SpeedRoundY
    playerObjects[playerTurn].fire()
    projectileGoing = True
    pos = playerObjects[playerTurn].calculateTurretEndPos()
    
    
    bulletPosition[0] = pos[0]
    bulletPosition[1] = pos[1]

    angle = playerObjects[playerTurn].turretAngle
    SpeedRoundY = playerObjects[playerTurn].v0
    SpeedRoundX = int(round(playerObjects[playerTurn].v0 * math.cos(angle*180/math.pi)))
    
def calculateProjectilePosition():
    #errechnet die FLugbahn eines Projektils
    global gravity, SpeedRoundY, SpeedRoundX, gravity
    bulletPosition[0] += SpeedRoundX
    bulletPosition[1] -= SpeedRoundY
    SpeedRoundY -= gravity
    checkForBulletCollision()
    return (bulletPosition[0],bulletPosition[1])

def checkForBulletCollision():
    #Kollisoinskontrolle für die Kanonenkugel mit dem Terrain und anderen Pnazern
    global projectileGoing
    if bulletPosition[0] > w_width or bulletPosition[0] < 0:
        projectileGoing = False
        nextPlayer()
        return

    #falls eine Kugel direkt auf den Panzer trifft
    for Tank in playerObjects:
        if bulletPosition[0] > Tank.tx and bulletPosition[0] < Tank.tx+Tank.twidth:
            if bulletPosition[1] > Tank.ty-5 and bulletPosition[1] < Tank.ty + 2* Tank.theight:
                Tank.tLp -= playerObjects[playerTurn].weapons[playerObjects[playerTurn].currentWeapon][3]
                Terrain.explosion(bulletPosition[0], playerObjects[playerTurn].weapons[playerObjects[playerTurn].currentWeapon][1])
                projectileGoing = False
                nextPlayer()

    #kollisionskontrolle mit dem Terrain
    if bulletPosition[1] >= w_height-Terrain.yWerte[bulletPosition[0]]:
        explosionRadius = playerObjects[playerTurn].weapons[playerObjects[playerTurn].currentWeapon][1]
        Terrain.explosion(bulletPosition[0], explosionRadius)
        projectileGoing = False
        #schadensverwaltung für panzer im umkreis der Explosion
        for Tank in playerObjects:
            if Tank.tx > bulletPosition[0] - explosionRadius and Tank.tx < bulletPosition[0] + explosionRadius:
                Tank.tLp -= int(playerObjects[playerTurn].weapons[playerObjects[playerTurn].currentWeapon][3]/2)
        nextPlayer()


    
#----------------------GRAPHICAL FUNCTIONS--------------------------------------
def message_to_screen(msg, color, fontSize, fontKoordinaten):
    font = pygame.font.SysFont(None, fontSize)
    screen_text = font.render(msg, True, color)
    win.blit(screen_text, fontKoordinaten)
    
    

def redrawGame():
    #GAME LOOP DRAWING

    #--------------------Terrain drawing
    for x in range(w_width):
        pygame.draw.line(win, Terrain.color, (x+1, w_height), (x+1, w_height-Terrain.yWerte[x]), 1)
    pygame.draw.circle(win, Terrain.sunColor, Terrain.sunCoordinates, Terrain.sunRadius)

    #-------------------Controlbar and contents of controlbar
    pygame.draw.rect(win, menuBarColor, (0,0, w_width, menuBarHeight))
    pygame.draw.line(win, (240,248,255), (0,menuBarHeight+1), (w_width, menuBarHeight+1), 0)

    #--drawing the current player
    pygame.draw.ellipse(win, playerObjects[playerTurn].tcolor, (0, playerObjects[playerTurn].turretheight, playerObjects[playerTurn].twidth, playerObjects[playerTurn].theight), 0)
    pygame.draw.ellipse(win, playerObjects[playerTurn].tcolor, (int((playerObjects[playerTurn].twidth-playerObjects[playerTurn].turretwidth)/2), 5,playerObjects[playerTurn].turretwidth,playerObjects[playerTurn].turretheight),0)
    message_to_screen(str(playerObjects[playerTurn].playerNumber), black, 20, (playerObjects[playerTurn].twidth+5,0))

    #--the fuel and the left and right buttons
    message_to_screen(str("Fuel: " + str(playerObjects[playerTurn].fuel)), black, 20, (playerObjects[playerTurn].twidth+5, 15))
    #left button is missing
    #right button is missing

    #--Livepoints
    message_to_screen(str("LP: " + str(playerObjects[playerTurn].tLp)), black, 20, (playerObjects[playerTurn].twidth+5, 30))

    #--Weapons and Amount
    stringWeapons = str(playerObjects[playerTurn].weapons[playerObjects[playerTurn].currentWeapon][2]) + " : "
    stringWeapons += str(playerObjects[playerTurn].weapons[playerObjects[playerTurn].currentWeapon][0])
    message_to_screen(stringWeapons, black, 20, (400,5))

    #--cahngeWeaponButton
    message_to_screen("Change Weapon", grey, 20, (410, 25))

    #change v0-Projectile Buttons
    message_to_screen(str("Force: " + str(playerObjects[playerTurn].v0)), black, 20,(600, 25))
    message_to_screen("More", black, 20,(600, 10))
    message_to_screen("Less", black, 20,(600, 40))

    #a fire Button
    message_to_screen("FIRE", red, 25, (750, 25))

    #--Draw a projectile
    if projectileGoing:
        pygame.draw.circle(win, black, calculateProjectilePosition(), 1)
    #--------------------tank and other drawings 
    for Tank in playerObjects:
        if Tank.tLp > 0:
            pygame.draw.ellipse(win, Tank.tcolor, (Tank.tx,Tank.ty,Tank.twidth,Tank.theight), 0)
            pygame.draw.ellipse(win, Tank.tcolor, (int(Tank.tx + (Tank.twidth-Tank.turretwidth)/2), Tank.ty-Tank.turretheight+5 ,Tank.turretwidth,Tank.turretheight),0)
            pygame.draw.line(win, Tank.tcolor, ((Tank.tx+int(Tank.twidth/2), Tank.ty)), Tank.calculateTurretEndPos(), Tank.turretThickness)
    
    pygame.display.update()
    
def redrawMenu():
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

def redrawShopMenu():
    for message in shopBlock:
        message_to_screen(str(str(message[1]) + message[0]), message[4], message[3], message[5])

    pygame.display.update()



#---------------------------------MAIN GAME LOOP--------------------------------  
def gameLoop():
    global Tank
    global Terrain
    while runGameLoop:
        pygame.time.delay(100)      #100 ms = 10 FPS
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #checkMouseClickGame(pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                checkMouseClickGame(pygame.mouse.get_pos())


        #checks for keys being pressed
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            if not projectileGoing:
                fire()

        if keys[pygame.K_0]:
            nextPlayer()
            
        if keys[pygame.K_LEFT]:
            playerObjects[playerTurn].move(-1, Terrain.yWerte)
                
        if keys[pygame.K_RIGHT]:
            playerObjects[playerTurn].move(1, Terrain.yWerte)
            
        if keys[pygame.K_UP]:
            playerObjects[playerTurn].turretAngle += 1
            
        if keys[pygame.K_DOWN]:
            playerObjects[playerTurn].turretAngle -= 1
            #change player)

        win.fill(skyblue)
        for Tank in playerObjects:
            if Tank.ty < w_height:
                if Tank.ty < w_height-(Terrain.yWerte[Tank.tx] + Tank.theight -5):
                    Tank.ty += Tank.ySpeed
                    Tank.ySpeed += gravity
                else:
                    Tank.ty = w_height-(Terrain.yWerte[Tank.tx] + Tank.theight - 5)
                    #Tank.tLp -= Tank.ySpeed
                    Tank.ySpeed = 0
                    
            else:
                Tank.tLp = 0

        #das ist nur eine Provisorische Abfrage um bugs uz vermeiden
        if playerObjects[playerTurn].tLp == 0:
            nextPlayer()
        redrawGame()

    if gotoMenu == False:
        pygame.quit()


#-------------------------------------MENU LOOP------------------------------------ 
def startMenu():
    global menuRun
    while menuRun:
        pygame.time.delay(100)
            
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



#-------------------------------START MENU LOOP-----------------------------------
def menu():
    global menuRoundRun
    while menuRoundRun:
        pygame.time.delay(100)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuRoundRun = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                checkMouseClickShopMenu(pygame.mouse.get_pos())


        win.fill(white)
        
        redrawShopMenu()
    if gotoGame == False:
        pygame.quit()
    

#---------------------------------MAIN FUNCTION------------------------------------
def main():
    startMenu()

    
    #gameInitialisation
    Terrain.generate(terrainTypeSelected)
    
    for x in range(playerAmount):
        randomX = random.randint(0, 740)
        T = Tank(randomX,100, black, w_width, x+1)
        playerObjects.append(T)

    game = True
    while game:
        gameLoop()
        menu()
    
main()


