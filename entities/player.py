import pygame
import math
import random
from engine import state

class Player:
    def __init__(self,x,y,s,img_list):
        self.ani_list = []
        self.ani_type = [0,0,0]
        self.ani_cooldown = [0,15]
        self.ground = False
        self.y_vel = 0
        self.speed = [7.5,0,2]
        self.flip = False
        self.health = [50,50,0,20]
        self.x = x
        self.y = y

        for i in img_list:
            self.new_list = []
            for b in i:
                self.new_list.append(pygame.transform.scale(b,(b.get_width()*s,b.get_height()*s)))
            self.ani_list.append(self.new_list)
        
        self.health_bar = health_bar(self.ani_list[0][0].get_width(),self.health[0])
        self.rect = self.ani_list[0][0].get_rect()
        self.rect.topleft = (x,y)
    def blitt(self,gun,boss):
        if self.health[1] > 0:
            if gun.active and gun.activate:
                if self.ani_type[2] == 1:
                    self.ani_type[2] = 2
                else:
                    self.ani_type[2] = 3
            elif not gun.active and gun.activate:
                if self.ani_type[2] == 1:
                    self.ani_type[2] = 4
                else:
                    self.ani_type[2] = 5
        else:
            self.ani_type[2] = 6
            state.scr_allow = True

        self.new_ani()
        if self.ani_cooldown[0] == self.ani_cooldown[1]:
            self.ani_cooldown[0] = 0
            self.ani_type[1] += 1
            if self.ani_type[2] == 6 and self.ani_type[1] == len(self.ani_list[self.ani_type[0]]):
                state.map_T = True
                boss.stage = -2
            if self.ani_type[1] == len(self.ani_list[self.ani_type[0]]):
                self.ani_type[1] = 0
        
        else:
            self.ani_cooldown[0] += 1
        self.rect.w = self.ani_list[self.ani_type[0]][self.ani_type[1]].get_width()
        #self.rect.h = self.ani_list[self.ani_type[0]][self.ani_type[1]].get_height()

        state.screen.blit(pygame.transform.flip(self.ani_list[self.ani_type[0]][self.ani_type[1]],self.flip,False),self.rect)
        if self.health[1] != self.health[0]:
            self.health[2] += 1
            if self.health[2] > self.health[3]:
                self.health[1] += 1
                self.health[2] = 0
                if self.health[1] > self.health[0]:
                    self.health[1] = self.health[0]
            self.health_bar.draw((self.rect.topleft[0],self.rect.topleft[1]-30),self.health[1])
        if self.y_vel > 150:
            self.health[1] = -20
            self.y_vel = 0

        #pygame.draw.rect(state.screen,state.black,self.rect)
    def move(self,inp,t):
        if self.health[1] > 0:
            self.ani_type[2] = 0
            self.movement = [0,False]
            if inp[0]:
                self.ani_type[2] = 1
                self.flip = False
                self.movement[0] += self.speed[0]
            if inp[1]: 
                self.ani_type[2] = 1
                self.flip = True
                self.movement[0] -= self.speed[0]
            if not self.ground:
                self.y_vel += state.G
            
            if inp[2] and self.ground:
                self.ground = False
                state.Sound_effects[2].play()
                self.y_vel = -13

            self.ground = False
            tcol = []
            for i in t:
                if (i[0].right > self.x and i[0].left < self.x + self.rect.width and i[0].bottom > self.y + self.y_vel and i[0].top < self.y+self.rect.height+self.y_vel):
                    tcol.append(i[0])

            #if len(tcol) == 0:
            #    self.ground = False
            #elif self.y_vel < 0:
            #    self.ground = False

            for y in tcol:
                self.movement[1] = True
                if self.y_vel > 0:
                    self.rect.bottom = y.top
                    self.y = self.rect.y
                    self.ground = True
                    self.y_vel = 0
                elif self.y_vel < 0:
                    self.rect.top = y.bottom
                    self.y = self.rect.y
            
            if not self.movement[1]:
                self.y += self.y_vel
                if ((self.y > 400 and self.y_vel > 0) or (self.y < 200 and self.y_vel < 0)) and state.scr_allow:
                    self.y -= self.y_vel
                    state.scr_y += self.y_vel
                self.rect.y = self.y
            
            self.movement[1] = False
            xrect = pygame.Rect(self.x+self.movement[0],self.y,self.rect.w,self.rect.h)
            tcol = []
            for i in t:
                if i[0].colliderect(xrect):
                    tcol.append(i[0])
            for x in tcol:
                self.movement[1] = True
                if self.movement[0] > 0:
                    self.rect.right = x.left
                    self.x = self.rect.x
                elif self.movement[0] < 0:
                    self.rect.left = x.right
                    self.x = self.rect.x

            if not self.movement[1]:
                if ((self.x > 600 and self.movement[0] > 0) or (self.x < 200 and self.movement[0] < 0)) and state.scr_allow:
                    state.scr += self.movement[0]
                else:
                    self.x += self.movement[0]
                    self.rect.x = self.x


    def new_ani(self):
        if self.ani_type[2] != self.ani_type[0]:
            self.ani_type[0] = self.ani_type[2]
            self.ani_type[1] = 0

class health_bar:
    def __init__(self,width,total_health,height = 6):
        self.health = total_health
        self.width = width
        self.h = height
    def draw(self,cords,health,color2 = state.green,color1 = state.red):
        pygame.draw.rect(state.screen,color1,(cords[0],cords[1],self.width,self.width/self.h))
        pygame.draw.rect(state.screen,color2,(cords[0],cords[1],self.width*(health/self.health),self.width/self.h))