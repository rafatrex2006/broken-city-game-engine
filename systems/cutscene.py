import pygame
import math
import random
from engine import state

class cutscene:
    def __init__(self,path,ammount):
        #path = "assets/cutscenes/whatever folder/"
        self.list = []
        self.ammount = [0,ammount-1]
        self.cooldown = [0,10]
        self.active = False
        for i in range(ammount):
            image = pygame.image.load(path+str(i)+".png").convert_alpha()
            self.list.append(pygame.transform.scale(image,(state.Width,state.Height)))
    def draw(self):
        if self.active:
            self.cooldown[0] += 1
            if self.cooldown[0] >= self.cooldown[1]:
                self.cooldown[0] = 0
                self.ammount[0] += 1
                if self.ammount[0] >= self.ammount[1]:
                    self.ammount[0] = 0
                    self.active = False
            state.screen.blit(self.list[self.ammount[0]],(0,0))