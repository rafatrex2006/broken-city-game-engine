import pygame
import math
import random
from engine import state

class gun:
    def __init__(self,cord):
        self.x = cord[0]
        self.y = cord[1]
        self.activate = False
        self.active = False
        self.ani_list = []
        self.item_ani = []
        for i in range(4):
            image = pygame.image.load(f"assets/animations/gun/{i}.png").convert_alpha()
            image = pygame.transform.scale(image,(int(image.get_width()*0.19),int(image.get_height()*0.15)))
            self.ani_list.append(image)
        
        #item
        for i in range(10):
            image = pygame.image.load(f"assets/animations/gun i/{i}.png").convert_alpha()
            image = pygame.transform.scale(image,(int(image.get_width()*0.4),int(image.get_height()*0.4)))
            self.item_ani.append(image)

        self.i_rect = pygame.Rect(self.x,self.y,self.item_ani[2].get_width(),self.item_ani[2].get_height())
        self.col = [0,3,0]
        self.col_i = [0,9,0]
        #set angle, etc...
        self.w,self.h = self.ani_list[0].get_width(), self.ani_list[0].get_height()
        self.ang_gun = math.degrees(math.atan2(self.h/2,self.w))
        self.an = self.ang_gun

    def draw(self,prec):
        if self.activate:    
            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[1]:
                self.active = True
                #Animations
                self.col[0] += 1
                if self.col[0] == self.col[1]:
                    self.col[0] = 0
                    self.col[2] += 1
                    if self.col[2] == len(self.ani_list):
                        self.col[2] = 0
                a = pygame.transform.flip(self.ani_list[self.col[2]],False,prec.flip)

                #calculating angles and angling images

                if prec.flip:
                    self.x,self.y = prec.rect.x +41, prec.rect.y + 58
                else:
                    self.x,self.y = prec.rect.x +15, prec.rect.y + 58
                mx,my = pygame.mouse.get_pos()
                self.an = -math.degrees(math.atan2(my-self.y,mx-self.x))
                box = [pygame.math.Vector2(p) for p in [(0, self.h/2), (self.w, self.h/2), (self.w, -self.h/2), (0, -self.h/2)]]
                box_rotate = [p.rotate(self.an) for p in box]
                min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
                max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
                self.origin = (self.x + min_box[0], self.y - max_box[1])
                aa = pygame.transform.rotate(a,self.an)

                #rendering
                if pygame.mouse.get_pressed()[0]:
                    state.screen.blit(aa,self.origin)
                if -self.an > 40 and -self.an < 150 and pygame.mouse.get_pressed()[1]:
                    state.screen.blit(aa,self.origin)
                    if prec.y_vel == 0:
                        prec.y_vel = -20
                        state.Sound_effects[2].play()
                else:
                    aa = pygame.Surface((0,0))
            else:
                self.active = False

        else:
            if prec.rect.colliderect(self.i_rect):
                self.activate = True
                state.Sound_effects[3].play()
            else:
                self.col_i[0] += 1
                if self.col_i[0] == self.col_i[1]:
                    self.col_i[0] = 0
                    self.col_i[2] += 1
                    if self.col_i[2] == self.col_i[1]:
                        self.col_i[2] = 0
                self.i_rect = pygame.Rect(self.x-state.scr,self.y-state.scr_y,self.item_ani[2].get_width(),self.item_ani[2].get_height())
                self.aa = self.item_ani[self.col_i[2]]
                state.screen.blit(self.aa,self.i_rect)