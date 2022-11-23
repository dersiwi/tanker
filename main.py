import pygame
import math
import random
#from tankClass import Tank
#from terrainClass import terrain
from playerObjects import Terrain, Sun, Tank, Projectile
from menubar import MenuBar
from startmenu import StartMenu
from utilities import Colors
pygame.init()


#screen variables
w_width = int(900)
w_height= int(600)
window = (w_width, w_height)





#terrain.generate(0)
'''
Tank = Tank(100,100, black, w_width)
'''
#window 
win = pygame.display.set_mode(window)
pygame.display.set_caption("Tanker")


#---------------------INGAME VARIABLES
playerAmount = 2            #the number of players
playerObjects = []          #stores every Player object 
playerTurn = 0              #Stores the index of the current player objects turn (if its player 1s turn its 0)

gameObjects = []
currentPlayer = None
terrain = None
def initializeTerrain(terrainType):
    global terrain
    terrain = Terrain(w_width, w_height)
    terrain.generate(terrainType)
    gameObjects.append(terrain)


sun = Sun(w_width, w_height)

bullet = None

gameObjects.append(sun)

menuBar = MenuBar(w_width, w_height)

#--------------------Drawing Variables (GameLoop)

projectileGoing = False
SpeedRoundX = 0
SpeedRoundY = 10
bulletPosition = [0,0]
gravity = 5

#-------------------Variables for menu after gameLoop
gotoMenu = False            #this prevents the game from quitting pygame and so just ends the functin 
runGameLoop = True          #this is the boolean responsible for running the gameLoop
menuRoundRun = True         #this is the boolean responsible for running the menu Loop

shopBlock = ["Small Atom Bomb", 10000, 1, 20, Colors.black, (40,40)]
#shopBlock = ["Name", cost, amountPerBuy, fontSize, fonColor, (x-position, y-position)]

#----------------------FUNCTIONAL FUNCTIONS------------------------------------

def checkMouseClickGame(pos):
    x = pos[0]
    y = pos[1]

    if x >= 410 and x < 410 + 120:
        if y >= 25 and y <= 25+25:
            currentPlayer.changeWeapon()
            
    if x > 600 and x < 600+50:
        if y > 10 and y < 10 + 25:
            currentPlayer.changeV(1)
        if y > 40 and y < 40 + 25:
            currentPlayer.changeV(-1)

    if x > 750 and x < 750 + 50:
        if y > 25 and y < 25 + 30:
            fire()

            

def nextPlayer():
    global playerTurn, gotoMenu, runGameLoop, currentPlayer
    amountLiving = 0
    for Tank in playerObjects:
        if Tank.tLp > 0:
            amountLiving += 1
    if amountLiving <= 1:
        runGameLoop = False
        return

    
    len(playerObjects)
    if playerTurn == len(playerObjects) - 1:
        playerTurn = 0 
    else:
        playerTurn += 1
    currentPlayer = playerObjects[playerTurn]

    #this ensures that no dead player can have turns
    if currentPlayer.tLp <= 0:
        playerObjects.pop(currentPlayer)
        nextPlayer()

def fire():
    global bullet
    currentPlayer.fire()
    pos = currentPlayer.calculateTurretEndPos()
    
    
    bulletPosition[0] = pos[0]
    bulletPosition[1] = pos[1]

    angle = currentPlayer.turretAngle
    SpeedRoundY = currentPlayer.v0
    SpeedRoundX = int(round(currentPlayer.v0 * math.cos(angle*180/math.pi)))
    bullet = Projectile(pos[0], pos[1], SpeedRoundX, SpeedRoundY, terrain, gravity, currentPlayer.getCurrentWeapon(), playerObjects)
    gameObjects.append(bullet)


def bulletHit():
    global bullet
    gameObjects.remove(bullet)
    bullet = None
    nextPlayer()

    
#----------------------GRAPHICAL FUNCTIONS--------------------------------------

    
    

def redrawGame():
    #GAME LOOP DRAWING
    #--------------------terrain drawing
    for gameObject in gameObjects:
        gameObject.draw(win)
    if not bullet == None and bullet.collisionDetection():
        bulletHit()

    menuBar.draw(win, currentPlayer)
    

    for tank in playerObjects:
        if tank.tLp > 0:
            tank.draw(win)

    
    pygame.display.update()
    



#---------------------------------MAIN GAME LOOP--------------------------------  
def gameLoop():
    global Tank
    global terrain
    runGameLoop = True
    while runGameLoop:
        pygame.time.delay(100)      #100 ms = 10 FPS
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runGameLoop = False
            #checkMouseClickGame(pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                checkMouseClickGame(pygame.mouse.get_pos())


        #checks for keys being pressed
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            fire()

        if keys[pygame.K_0]:
            nextPlayer()
            
        if keys[pygame.K_LEFT]:
            currentPlayer.move(-1, terrain.yWerte)
                
        if keys[pygame.K_RIGHT]:
            currentPlayer.move(1, terrain.yWerte)
            
        if keys[pygame.K_UP]:
            currentPlayer.turretAngle += 1
            
        if keys[pygame.K_DOWN]:
            currentPlayer.turretAngle -= 1
            #change player)

        win.fill(Colors.skyblue)
        for tank in playerObjects:
            if tank.ty < w_height:
                if tank.ty < w_height-(terrain.yWerte[tank.tx] + tank.theight -5):
                    tank.ty += tank.ySpeed
                    tank.ySpeed += gravity
                else:
                    tank.ty = w_height-(terrain.yWerte[tank.tx] + tank.theight - 5)
                    #Tank.tLp -= Tank.ySpeed
                    tank.ySpeed = 0
                    
            else:
                tank.tLp = 0

        #das ist nur eine Provisorische Abfrage um bugs uz vermeiden
        if currentPlayer.tLp == 0:
            nextPlayer()
        redrawGame()

    pygame.quit()
    

#---------------------------------MAIN FUNCTION------------------------------------
def main():
    global currentPlayer

    startingMenu = StartMenu(screenWidth=w_width, screenHeight=w_height)
    startingMenu.runMenu(win)
    initializeTerrain(startingMenu.terrainTypeSelected)

    #gameInitialisation

    
    for x in range(playerAmount):
        randomX = random.randint(0, 740)
        T = Tank(randomX,100, Colors.black, w_width, x+1)
        playerObjects.append(T)
    currentPlayer = playerObjects[0]

    game = True
    while game:
        gameLoop()
    
main()


