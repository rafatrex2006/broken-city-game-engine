import pygame
import math
import random
from engine import state

class particle:
    def __init__(self,pos):
        self.cords = pos
        self.ani = []
        self.cooldown = [0,50]
        self.ani_i = [0,4]
        for i in range(5):
            im = pygame.image.load(f"assets/masks and others/Fine/{i}.png").convert_alpha()
            im = pygame.transform.scale(im,(int(im.get_width()*1.5),int(im.get_height()*1.5)))
            self.ani.append(im)
    def draw(self):
        self.cords[0] += 0.1
        self.cords[1] -= 0.3
        self.cooldown[0] += 1
        if self.cooldown[0] >= self.cooldown[1]:
            self.cooldown[0] = 0
            if self.cooldown[1] == 50:
                self.cooldown[1] = 10
            self.ani_i[0] += 1
            if self.ani_i[0] >= self.ani_i[1]:
                self.ani_i[0]
                return True
        
        state.screen.blit(self.ani[self.ani_i[0]],self.cords)
        return False