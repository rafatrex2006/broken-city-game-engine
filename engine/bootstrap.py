import pygame
from engine import state

def init():
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 512)
    Width = 800
    Height = 600

    screen = pygame.display.set_mode((Width, Height))
    clock = pygame.time.Clock()
    level = 2

    pygame.display.set_caption("Broken city")
    icon = pygame.image.load("assets/map/0.png")
    pygame.display.set_icon(icon)

    #global variables setup
    state.Width = Width
    state.Height = Height
    state.screen = screen
    state.level = level
    state.clock = clock
    state.tile_size = 50