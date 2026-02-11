import pygame
import math
import random
from engine import state
from engine import assets
from entities.player import health_bar
from entities.particles import particle

class load:
    def __init__(self,width,ammount,height = 6):
        self.ammount = [0,ammount]
        self.bar = health_bar(width,ammount,height)
    def draw(self,cords,key):
        if key:
            self.bar.draw(cords,self.ammount[0],state.red,state.black)
            self.ammount[0] += 1
            if self.ammount[0] >= self.ammount[1]:
                self.ammount[0] = 0
                return True
        else:
            self.ammount[0] = 0
        return False

class bill:
    def __init__(self,start,plus):
        self.start = start
        self.p = plus
    def draw(self):
        self.start += self.p
        return self.start

class boss_bulet:
    def __init__(self,cords,damage,ani,health,gun):
        self.damage = damage
        self.health = [health,health]
        self.bar = health_bar(20,health)
        self.ani = ani
        self.ani_i = [0,10,0,len(ani)]
        self.rect = pygame.Rect(cords[0],cords[1],self.ani[0].get_width(),self.ani[0].get_height())
        self.w = self.ani[0].get_width()
        self.h = self.ani[0].get_height()
        self.momentum = [0,0]
        self.gun = gun
    def draw(self):
        self.ani_i[0] += 1
        if self.ani_i[0] >= self.ani_i[1]:
            self.ani_i[2] += 1
            self.ani_i[0] = 0
            if self.ani_i[2] >= self.ani_i[3]:
                self.ani_i[2] = 0
        a = pygame.transform.flip(self.ani[self.ani_i[2]],True,False)
        an = math.degrees(-math.atan2(state.hero.rect.center[1]-self.rect[1],state.hero.rect.center[0]-self.rect[0]))
        try:
            self.momentum[0] += (state.hero.rect.center[0]-self.rect[0])/1000
            self.momentum[1] += (state.hero.rect.center[1]-self.rect[1])/1000
            self.rect.x += self.momentum[0]
            self.rect.y += self.momentum[1]
        except:
            self.rect.x += self.momentum[0]
            self.rect.y += self.momentum[1]
        
        if self.gun.active:
            angect = pygame.Rect(self.rect.center[0],self.rect.center[1],self.rect.w,self.rect.h)
            if math.sqrt((angect.x-self.gun.x)**2 + (angect.y-self.gun.y)**2) < self.gun.w:
                B = -math.atan2(angect.y-self.gun.y,angect.x-self.gun.x)
                #print(B,gun.ang_gun)           
                if math.tan(B) > math.tan(math.radians(self.gun.an - self.gun.ang_gun)) and math.tan(B) < math.tan(math.radians(self.gun.an + self.gun.ang_gun)):
                    self.health[0] -= 0.5
                    if self.health[0] <= 0:
                        return True
        if self.health[0] != self.health[1]:
            self.bar.draw(self.rect.center,self.health[0])

        #print(self.momentum)
        #an = math.degrees(-math.atan2(self.momentum[0],self.momentum[1]))

        box = [pygame.math.Vector2(p) for p in [(0, self.h/2), (self.w, self.h/2), (self.w, -self.h/2), (0, -self.h/2)]]
        box_rotate = [p.rotate(an) for p in box]
        min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
        self.origin = (self.rect.x + min_box[0], self.rect.y - max_box[1])
        aa = pygame.transform.rotate(a,an)
        state.screen.blit(aa,self.origin)

class boss_hand:
    def __init__(self,damage,rect):
        self.damage = damage
        self.bound = rect
        self.y_vel = 0
        self.im = pygame.transform.scale(pygame.image.load("assets/Boss/hand.png").convert_alpha(),(int(75*1.5),int(96*1.5)))
        self.rect = pygame.Rect(rect.x,rect.y,self.im.get_width(),self.im.get_height())
        self.countdown = 0
    def draw(self):
        if self.countdown >= 20:
            if self.rect.colliderect(state.hero.rect):
                state.hero.health[1] -= self.damage
            self.y_vel += 1
            self.rect.y += self.y_vel
            if self.rect.y > 800:
                self.countdown = 0
                self.rect.y = self.bound.y
                self.y_vel = 0
        else:
            if self.rect.right + (state.hero.rect.center[0] - self.rect.center[0])/5 < self.bound.right and self.rect.x + (state.hero.rect.center[0] - self.rect.center[0])/5 > self.bound.left:
                self.rect.x += (state.hero.rect.center[0] - self.rect.center[0])/5
            self.countdown += 1
        state.screen.blit(self.im,self.rect)

class boss_eyes:
    def __init__(self,bound_rect,eye_rect):
        self.bound = bound_rect
        self.rect = eye_rect
    def draw(self):
        movement = [(state.hero.rect.center[0]-self.rect.center[0])/10,(state.hero.rect.center[1]-self.rect.center[1])/10]

        #print(state.hero.rect.center[1],self.rect.center[1])

        if self.rect.right + movement[0] > self.bound.right:
            self.rect.right = self.bound.right
        elif self.rect.left + movement[0] < self.bound.left:
            self.rect.left = self.bound.left

        else:
            self.rect.x += movement[0]

        if self.rect.top + movement[1] < self.bound.top:
            self.rect.top = self.bound.top
        elif self.rect.bottom + movement[1] > self.bound.bottom:
            self.rect.bottom = self.bound.bottom
        else:
            self.rect.y += movement[1]
        
        #print(movement)

        pygame.draw.rect(state.screen,state.white,self.bound)
        pygame.draw.rect(state.screen,state.black,self.rect)

class boss:
    def __init__(self,health):
        self.rest_health = health
        self.health = health
        self.anim = []
        self.y = 1100
        self.f = False
        for i in [[2,"idle/"],[3,"idle 2/"],[7,"Transition/"]]:
            self.anim.insert(len(self.anim),[])
            for o in range(i[0]):
                img = pygame.image.load("assets/Boss/"+i[1]+ str(o) +".png").convert_alpha()
                img = pygame.transform.scale(img,(img.get_width()*20,img.get_height()*20))
                self.anim[-1].append(img)

        self.ani_i = [0,20,0,len(self.anim[0]),0,0]
        self.projec = [boss_hand(5,pygame.Rect(0,0,400,1)), boss_hand(5,pygame.Rect(400,0,400,1)),boss_eyes(pygame.Rect(280,240,60,60),pygame.Rect(0,0,20,20)),boss_eyes(pygame.Rect(420,240,60,60),pygame.Rect(0,0,20,20))]
        self.cooldown = [0,0,False]
        self.w_ani = []
        self.w_ani.insert(len(self.w_ani),[])
        for i in range(3):
            im = pygame.image.load(f"assets/Boss/projectile/{i}.png").convert_alpha()
            im = pygame.transform.scale(im,(im.get_width()*10,im.get_height()*10))
            self.w_ani[-1].append(im)
        self.stage = -1
        self.bar = health_bar(self.anim[0][0].get_width()-40,health,20)
        self.attack_loader = load(state.hero.rect.w,60,6)
        self.bills = bill(30,15)
    def draw(self,gun):
        state.scr_allow = False
        state.scr,state.scr_y = 0,0

        if self.ani_i[4] != self.ani_i[5]:
            self.ani_i[2] = 0
            self.ani_i[3] = len(self.anim[self.ani_i[4]])
            self.ani_i[5] = self.ani_i[4]
        else:
            self.ani_i[0] += 1
            if self.ani_i[0] >= self.ani_i[1]:
                self.ani_i[0] = 0
                self.ani_i[2] += 1
                if self.ani_i[2] >= self.ani_i[3]:
                    self.ani_i[2] = 0
        
        state.screen.blit(self.anim[self.ani_i[4]][self.ani_i[2]],(0,self.y -self.anim[self.ani_i[4]][self.ani_i[2]].get_height()))
        self.bar.draw((20,20),self.health)
        if self.stage == -2:
            self.y = 1100
            self.health = self.rest_health
            self.projec = [boss_hand(5,pygame.Rect(0,0,400,1)), boss_hand(5,pygame.Rect(400,0,400,1)),boss_eyes(pygame.Rect(280,240,60,60),pygame.Rect(0,0,20,20)),boss_eyes(pygame.Rect(420,240,60,60),pygame.Rect(0,0,20,20))]
            self.ani_i[4] = 0
            self.stage += 1
        if self.stage == 0:
            for i in self.projec[2:]:
                i.draw()
        if self.stage <= 0:
            self.cooldown[1] = 100
            self.cooldown[0] += 1
            if self.cooldown[0] >= self.cooldown[1]:
                self.y -= 2
                if self.y <= 600:
                    self.y = 600
                    self.stage += 1
                    self.cooldown[0] = 0
        elif self.stage == 1:
            if self.health >= 400:
                self.cooldown[1] = 100
                self.cooldown[0] += 1
                if self.cooldown[0] >= self.cooldown[1]:
                    self.cooldown[0] = 0
                for i in self.projec:
                    i.draw()
            elif self.health >= 200:
                state.scr_y = -90
                if not self.cooldown[2]:
                    self.ani_i[4] = 2
                    if self.ani_i[2] == self.ani_i[3]-1:
                        self.cooldown[2] = True
                else:
                    self.ani_i[4] = 1
                    self.cooldown[1] = 200
                    self.cooldown[0] += 1
                    if self.cooldown[0] >= self.cooldown[1]:
                        self.cooldown[0] = 0
                        self.projec.insert(len(self.projec),boss_bulet((420,460),0.5,self.w_ani[0],1,gun))
                    for i in reversed(self.projec[2:]):
                        if i.draw():
                            self.projec.remove(i)
                    for i in self.projec[4:]:
                        if i.rect.colliderect(state.hero.rect):
                            state.hero.health[1] -= i.damage
            elif self.health > 0:
                self.projec[0].damage,self.projec[1].damage = 1,1
                state.scr_y = -90
                self.ani_i[4] = 1
                self.cooldown[1] = 200
                self.cooldown[0] += 1
                if self.cooldown[0] >= self.cooldown[1]:
                    self.cooldown[0] = 0
                    self.projec.insert(len(self.projec),boss_bulet((420,460),0.5,self.w_ani[0],1,gun))
                for i in reversed(self.projec):
                    if i.draw():
                        self.projec.remove(i)
                for i in self.projec[4:]:
                    if i.rect.colliderect(state.hero.rect):
                        state.hero.health[1] -= i.damage
            else:
                scr_allow = True
                state.cutscenes[1].active = True
                state.map_T = True
                return True

    def drawtop(self):
        if self.stage == 1:
            if state.hero.ani_type[2] == 0:
                if self.attack_loader.draw((state.hero.rect.x,state.hero.rect.bottom + 20),self.f):
                    self.health -= self.bills.draw()
                    state.particles.append(particle([state.hero.rect.x,state.hero.rect.top - 100]))
            else:
                self.attack_loader.draw((state.hero.rect.x,state.hero.rect.bottom + 20),False)