import pygame

def message_to_screen(win, msg, color, fontSize, fontKoordinaten):
    font = pygame.font.SysFont(None, fontSize)
    screen_text = font.render(msg, True, color)
    win.blit(screen_text, fontKoordinaten)


class Colors:
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
                    |        text       |     height
                    |___________________|

        
    """
    def __init__(self, x, y, width, height, text=None, fontSize=12, color=Colors.black):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.fontSize = fontSize
        self.color = color
    

    """
        True if the position was inside the bounds of this button
    """
    def isClicked(self, pos):
        mouseX, mouseY= pos[0], pos[1]

        if mouseX > self.x and mouseX < self.x + self.width:
            if mouseY > self.y and  mouseY < self.y + self.height:
                return True

        return False 

    #win, msg, color, fontSize, fontKoordinaten
    def draw(self, win):
        message_to_screen(win, self.text, self.color, self.fontSize, (self.x, self.y))