from src.menu import game
import pygame

pygame.init()

pygame.display.set_caption('Shiba-Inu')
icon = pygame.image.load('src/images/Pasted Graphic 3.tiff')
pygame.display.set_icon(icon)

try:
    game()
except Exception:
    pass
