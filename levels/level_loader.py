import pygame
import math
import random
import csv
from engine import state
from entities.enemy import enemy
from entities.player import health_bar
from systems.ui import buttons

def new_map(lv,til,MAP,pl = False):
    state.level = lv
    tiles = []
    state.boss_death = False
    state.hero.health[1] = 50
    state.hero.rect.topleft = (100,200)
    #icons = []
    button = []
    state.scr = 0
    state.scr_y = 0
    #caracter.rect[1] = 100w
    #caracter.energy_wasted = 0
    with open(f"Assets\level {lv}_data.csv", newline="") as f:
        reader = csv.reader(f)
        platform_list = list(reader)
        #print(reader)
    for x,i in enumerate(platform_list):
        for y,p in enumerate(i):
            platform_list[x][y] = int(p)
    for b in platform_list[:-2]:
        c = 0
        for i in reversed(range(1,17)):
            for v in range(b[-i-1]):
                #print(c)
                tiles.append([pygame.Rect(b[c],b[-1],state.tile_size,state.tile_size),til[15-i]])
                c += 1
    if pl:
        for k in range(len(platform_list[-1])//9):
            if platform_list[-1][8+9*k] and platform_list[-1][4+9*k]:
                state.enemies.append(enemy(pygame.Rect(platform_list[-1][0+9*k],platform_list[-1][1+9*k],platform_list[-1][2+9*k],platform_list[-1][3+9*k]),platform_list[-1][7+9*k],[state.Monster_ani[0],10],platform_list[-1][5+9*k],[platform_list[-1][4+9*k],[pygame.Surface((10,10)),pygame.Surface((5,5))],10],platform_list[-1][6+9*k]))
            elif platform_list[-1][8+9*k] and not platform_list[-1][4+9*k]:
                state.enemies.append(enemy(pygame.Rect(platform_list[-1][0+9*k],platform_list[-1][1+9*k],platform_list[-1][2+9*k],platform_list[-1][3+9*k]),platform_list[-1][7+9*k],[state.Monster_ani[1],20],400,[platform_list[-1][4+9*k],10,5],platform_list[-1][6+9*k]))
        for l in range(len(platform_list[-2])//3):
            if platform_list[-2][2+3*l] == 3:
                button.append([[platform_list[-2][0+3*l],platform_list[-2][1+3*l]]])
            if len(button) > 1:
                state.Stiles.append(buttons(button,MAP))
    return tiles

class Map:
    def __init__(self,back,l_list):
        self.levels = l_list
        self.background = back
        self.b_col = [0,20,0,len(back)]
        self.scr = [0,0]
        self.scr_limit = [self.background[0].get_width() - state.Width - 5,self.background[0].get_height() - state.Height - 5]
    def m_draw(self,inputs,l_dic,MAP):
        self.b_col[0] += 1
        if self.b_col[0] > self.b_col[1]:
            self.b_col[2] += 1
            self.b_col[0] = 0
            if self.b_col[2] >= self.b_col[3]:
                self.b_col[2] = 0
        if pygame.mouse.get_pressed()[0]:
            m_pos = pygame.mouse.get_pos()
            for i in self.levels:
                if pygame.Rect((i[0][0]+self.scr[0],i[0][1]+self.scr[1]),(i[1].get_width(),i[1].get_height())).collidepoint(m_pos) and i[2]:
                    state.enemies = []
                    if i[4] == 0:
                        state.background = pygame.transform.scale(pygame.image.load("assets/backgrounds/2.png").convert_alpha(),(state.Width,state.Height))
                    else:
                        state.background = pygame.transform.scale(pygame.image.load("assets/backgrounds/4.png").convert_alpha(),(state.Width,state.Height))
                    state.Stiles = []
                    state.tiles = new_map(i[3],l_dic[i[4]],MAP)
                    state.tiles_copy = new_map(i[3],l_dic[i[4]],MAP,True)
                    state.map_T = False
        
        if inputs[0]:
            if not self.scr[0] < -self.scr_limit[0]:
                self.scr[0] -= 5
        if inputs[1]:
            if self.scr[0] < -5:
                self.scr[0] += 5
        if inputs[2]:
            if not self.scr[1] > -5:
                self.scr[1] += 5
        if inputs[3]:
            if self.scr[1] > -self.scr_limit[1]:
                self.scr[1] -= 5
        
        state.screen.blit(self.background[self.b_col[2]],self.scr)
        for i in self.levels:
            state.screen.blit(i[1],(i[0][0] + self.scr[0],i[0][1] + self.scr[1]))