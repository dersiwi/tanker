from pygame.font import SysFont
from pygame.draw import rect, line
import math

def message_to_screen(win, msg, color, fontSize, fontKoordinaten):
    font = SysFont(None, fontSize)  #pygame function
    screen_text = font.render(msg, True, color)
    win.blit(screen_text, fontKoordinaten)

def message_to_screen_fontObject(win, fontObj, text, color, fontKoordinaten):
    screen_text = fontObj.render(text, True, color)
    win.blit(screen_text, fontKoordinaten)


class DegreeCnvt:
    CNVT = math.pi/180
    def degree_to_radians(angle_in_degree) -> float:
        return angle_in_degree * DegreeCnvt.CNVT
    
    def radians_to_degree(angle_in_radians) -> float:
        return angle_in_radians / DegreeCnvt.CNVT


class ExplosionData:
    def __init__(self,x, y, radius, damage) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.damage = damage

    def is_in_radius(self, x, y) -> bool:
        """
        check if the point
        @param x,y point to check 
        @return true if the point is inside the radius of this explosion
        """
        return x <= self.x + self.radius and x >= self.x - self.radius and \
                y <= self.y + self.radius and y >= self.y - self.radius
    
class ConsolePrinter:

    class bcolors:
        #https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    
    NOTHING = -1
    ALL = 3
    DEBUG = 0
    REGULAR = 1
    VERBOSE = 2
    LEVELS = [DEBUG, REGULAR, VERBOSE]
    LEVEL_PREMESSAGE = ["[DEBUG] : ", "[REGULAR] : ", "[VERBOSE] : "]
    LEVEL_COLORS = [bcolors.WARNING, bcolors.OKBLUE, bcolors.BOLD]
    PRINT_LEVEL = NOTHING

    @staticmethod
    def print(message : str, print_level : int = DEBUG) -> None:
        """
        Prints messages to the console. Depeding on the print_level with different colors and pre-messages
        @param message : str to print
        @param print_level, one of NOTHING, DEBUG, REGULAR, VERBOSE. Defaults to DEBUG
        """
        if print_level == ConsolePrinter.NOTHING:
            return
        elif print_level == ConsolePrinter.PRINT_LEVEL or ConsolePrinter.PRINT_LEVEL == ConsolePrinter.ALL:
            ConsolePrinter.print_color(ConsolePrinter.LEVEL_PREMESSAGE[print_level] + message, 
                                       color = ConsolePrinter.LEVEL_COLORS[print_level])
            return
        if not print_level in ConsolePrinter.LEVELS:
            ConsolePrinter.print_color("[UNKNOWN-PRINT-LEVEL] : " + message, color = ConsolePrinter.bcolors.FAIL)

    @staticmethod
    def print_color(message : str, color = bcolors.ENDC) -> None:
        print(color + message + ConsolePrinter.bcolors.ENDC)
            
    

class Colors:
    #colors
    ingame_menubar_backgroundcolor = (179,179,179)
    wind_background = (255,255,255)
    black = (0,0,0)
    white = (255,255,255)
    red = (255,0,0)
    blue = (0,0,255)
    green = (0,255,0)
    orange = (255, 165, 0)
    grey = (110,110,110)
    forest_green = (34,139,34)
    skyblue = (176,226,255)
    yellow = (255, 255, 0)

    playerPurple = (127, 0, 255)
    playerTourquise = (0, 153, 153)
    playerYellow = (255, 255, 51)
    playerRed = (255, 51, 51)

    playerColors = [playerPurple, playerTourquise, playerYellow, playerRed]





class TextButton:
    """
        (x, y) have to be the absolute position on the window this button is to be drawn.
        width and height are then relatively added to x and y.

                            width
            (x,y)-> .___________________
                    |                   |
                    |        text <-m-> |     height
                    |___________________|
            
            m : is the added margin 
    """
    def __init__(self, x, y, text=None, fontSize=12, color=Colors.black, border : bool = False, margin : int = 0):
        self.x = x
        self.y = y
        self.textX = x
        self.textY = y
        #self.width = width
        #self.height = height
        self.text = text
        self.fontSize = fontSize
        self.color = color

        self.fontObject = SysFont(None, fontSize)
        
        if not text == None:
            self.textwidth, self.textheight = self.fontObject.size(text)
            self.buttonWidth, self.buttonHeight = self.textwidth, self.textheight


        #----variables for border

        self.hasBorder = border
        self.borderColor = Colors.black

        #---variables for background color
        self.hasBackgroundFilling = False
        self.backgroundColor = Colors.white

        self.setMargin(margin)


    def setText(self, text):
        self.text = text
        self.textwidth, self.textheight = self.fontObject.size(text)
        self.buttonWidth, self.buttonHeight = self.textwidth, self.textheight
        self.setMargin(self.margin)

    """
        the border is drawn around the rectangle, described by the x and y coordinates and the width and height of the 
        button.
    """
    def addBorder(self, borderColor=Colors.black):
        self.hasBorder = True
        self.borderColor = borderColor

    def addBackground(self, backgroundColor=Colors.white):
        self.hasBackgroundFilling = True
        self.backgroundColor = backgroundColor

    def setBackgroundColor(self, backgroundColor):
        self.hasBackgroundFilling = True
        self.backgroundColor = backgroundColor

    """
        Margin is always applied to the text itself, see description of TextButton
    """
    def setMargin(self, margin):
        self.margin = int(margin)

        #shifting of the text to the left
        self.textX = self.x + self.margin
        self.textY = self.y + self.margin

        #expanding of button width and height
        self.buttonWidth = 2 * self.margin + self.textwidth
        self.buttonHeight = 2 * self.margin + self.textheight


    def setWidth(self, width):
        self.textX = self.x + int(((width - self.textwidth) / 2))
        self.buttonWidth = width
    
    def setHeight(self, height):
        self.textY = self.y + int(((height - self.textwidth) / 2))
        self.buttonHeight = height


    """
        True if the position was inside the bounds of this button
    """
    def isClicked(self, pos):
        mouseX, mouseY= pos[0], pos[1]

        if mouseX > self.x and mouseX < self.x + self.buttonWidth:
            if mouseY > self.y and  mouseY < self.y + self.buttonHeight:
                return True

        return False 

    def getButtonDimensions(self):
        return (self.buttonWidth, self.buttonHeight)

    #win, msg, color, fontSize, fontKoordinaten
    def draw(self, win):
        if self.hasBackgroundFilling:
            backgroundRect = (self.x, self.y, self.buttonWidth, self.buttonHeight)
            rect(win, self.backgroundColor, backgroundRect)

        if self.hasBorder:
            line(win, self.borderColor, (self.x, self.y), (self.x + self.buttonWidth, self.y))
            line(win, self.borderColor, (self.x, self.y), (self.x, self.y + self.buttonHeight))
            line(win, self.borderColor, (self.x, self.y + self.buttonHeight), (self.x + self.buttonWidth, self.y + self.buttonHeight))
            line(win, self.borderColor, (self.x + self.buttonWidth, self.y), (self.x + self.buttonWidth, self.y + self.buttonHeight))


        message_to_screen(win, self.text, self.color, self.fontSize, (self.textX, self.textY))

        
        


