import pygame
import math
import random
from engine import state
from engine import assets


class buttons:
    def __init__(self,cord_list,MAP):
        self.cords = cord_list
        self.images = [pygame.image.load("assets/tiles/button off.png").convert_alpha(),pygame.image.load("assets/tiles/button on.png").convert_alpha()]
        self.images = [pygame.transform.scale(self.images[0],(state.tile_size,state.tile_size)),pygame.transform.scale(self.images[1],(state.tile_size,state.tile_size))]
        for i in self.cords:
            i.insert(1,self.images[0])
            i.insert(2,False)
        self.map = MAP
    def draw(self):
        ret = True
        for i in self.cords:
            #print(i[0][0]-state.scr,state.hero.rect.x)
            if math.sqrt((i[0][0]-state.scr-25-state.hero.rect.x)**2+(i[0][1]-state.scr_y+25-state.hero.rect.y)**2) < 130:
                if state.E_input:
                    i[1] = self.images[1]
                    i[2] = True
            if not i[2]:
                ret = False
            state.screen.blit(i[1],(i[0][0]-state.scr,i[0][1]-state.scr_y))
        if ret:
            if state.level == 2:
                state.cutscenes[0].active = True
            for i in self.cords:
                i[2] = False
                i[1] = self.images[0]
            self.map.levels[state.level][2] = True
            state.enemies = []
            state.map_T = True
            state.Stiles = []

class Map2:
    def __init__(self,background,obstacles,points):
        self.background = pygame.transform.scale(background,(state.Width,state.Height))
        self.obstacles = obstacles
        self.points = points
        self.rect = pygame.Rect(730,530,50,50)
    def start(self,hero):
        state.screen.blit(self.background,(0,0))
        for i in self.points:
            if math.sqrt((self.rect.x-i[0][0])**2+(self.rect.y-i[0][1])**2) < 90 and state.E_input:
                if i[1] == 1:
                    state.map2[-1] = False
                else:
                    print(i[1])
                    

        movement = [0,0]
        if hero[0] and self.rect.topright[0] < 800:
            movement[0] += 5
        if hero[1] and self.rect.topleft[0] > 0:
            movement[0] -= 5
        if hero[2] and self.rect.topright[1] > 0:
            movement[1] -= 5
        if hero[3] and self.rect.bottomright[1] < 600:
            movement[1] += 5

        self.rect.x += movement[0]
        for i in self.obstacles:
            if i.colliderect(self.rect):
                if movement[0] > 0:
                    self.rect.right = i.left
                elif movement[0] < 0:
                    self.rect.left = i.right
        self.rect.y += movement[1]
        for i in self.obstacles:
            #pygame.draw.rect(state.screen,state.green,i,2)
            if i.colliderect(self.rect):
                if movement[1] > 0:
                    self.rect.bottom = i.top
                elif movement[1] < 0:
                    self.rect.top = i.bottom
        
        state.screen.blit(pygame.Surface((50,50)),self.rect)