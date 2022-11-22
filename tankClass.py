import math
class Tank:
    def __init__(self, tx, ty, color, screenwidth, playerNumber):
        self.tx = tx
        self.ty = ty                        #tx and ty are the x and y position of the tank
        self.playerNumber = playerNumber    #the player placement wothin the round (when his turn is)
        self.twidth = 20                    #used for drawing the tank: width of the bottom ellipse
        self.theight = 8                    #used for drawing the tank: height of the bottom ellipse
        self.tcolor = color                 #the tanks color
        self.ySpeed = 0                     #the tanks vertical speed, only used for gravity
        self.tSpeed = 5                     #the tanks speedS
        self.tLp = 100                      #the tanks livepoints
        self.fuel = 500                     #the fuel for each round
        self.scorePoints = 0                #you can buy stuff with those, also they represent your score
        self.fuelPerMove = 5
        self.weapons = [["Small Missile", 20, 1000, 10], ["Vulcano Bomb", 50, 100, 50], ["Ball", 100, 100, 200], ["BigBall", 300, 10, 1000]]
        self.currentWeapon = 0
        #self.weapons = ("Name", explosionRadius, amount, damage)
        #self.currentWeapon: index of current seleycted weapon
        
        self.turretwidth = 10
        self.turretheight = 8
        self.turretAngle = 90   #math.sin() returns radians, NOT degrees
        #self.turretStartingPosition = (self.tx+int(self.twidth/2), self.ty)    da die x und y posiition ständig verändert wird ist diese variable irrelevant
        self.turretLength = 15
        self.turretThickness = 2
        self.v0 = 50
        self.v0ChangePerClick = 5
        self.v0Max = 70

        self.maximumSlopeCrossable = 5

        self.screen_width = screenwidth

        
    def movementPossible(self, yWerte):
        #this function calculates if the slope is too high for a tank to move to
        if self.tx + self.tSpeed > len(yWerte)-1 or self.tx + self.tSpeed < 0:
            return False
        else:
            if yWerte[self.tx] - yWerte[self.tx+self.tSpeed] <= self.maximumSlopeCrossable:
                return True
            else:
                return False
    
    def move(self, leftRight, yWerteTerrain):
        #leftRight is either 1 or -1 to multiply the movement
        if self.movementPossible(yWerteTerrain) and self.tx + self.tSpeed <= self.screen_width-self.twidth and self.fuel >= self.fuelPerMove:
                self.tx +=  int(self.tSpeed * leftRight)
                self.fuel -= self.fuelPerMove
    
    def fire(self):
        self.weapons[self.currentWeapon][2] -= 1
        
        if self.weapons[self.currentWeapon][2] == 0:
            self.weapons.pop(self.currentWeapon)

            
    def changeWeapon(self):
        if self.currentWeapon == len(self.weapons)-1:
            self.currentWeapon = 0
        else:
            self.currentWeapon += 1

    def calculateTurretEndPos(self):
        endPosX = int(round(self.tx + self.twidth/2 + self.turretLength * math.cos(self.turretAngle*180/math.pi)))
        endPosY = int(round(self.ty + self.turretLength * math.sin(self.turretAngle*180/math.pi)))
        return (endPosX, endPosY)
                
        
    def resetValues(self):
        #this function is used if a new round begins, all basic values need to be resetted.
        self.tLp = 100
        self.fuel = 200
        self.turretAngle = 45

    def changeV(self, n):
        if self.v0 + self.v0ChangePerClick * n < 0 or self.v0 + self.v0ChangePerClick * n > self.v0Max:
            return
        else:
            self.v0 += n * self.v0ChangePerClick
        
        
