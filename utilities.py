import pygame

def message_to_screen(win, msg, color, fontSize, fontKoordinaten):
    font = pygame.font.SysFont(None, fontSize)
    screen_text = font.render(msg, True, color)
    win.blit(screen_text, fontKoordinaten)