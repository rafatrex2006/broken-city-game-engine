import pygame
import math
import random
from engine import state
from entities.player import health_bar

class enemy:
    def __init__(self,plat_rect,dm,ani,rad,ranged_list,health):
        self.plat = plat_rect
        self.dm = dm
        self.ani = [0,ani[-1],0,0,1,0]
        #ani = [type,index,whichani_index]
        self.anim = ani[0]
        #ranged = [Is it ranged or not, projectile animation list]
        self.ranged = ranged_list
        self.proj = [0,10]
        self.health = [health,health,0,20]
        self.health_bar = health_bar(ani[0][0][0].get_width(),health)
        self.active = False
        self.flip = [False,ranged_list[2]]
        self.move = random.randint(self.plat[0],self.plat[0]+self.plat[2])
        self.rect = pygame.Rect(self.move,self.plat[1]-ani[0][0][0].get_height(),ani[0][0][0].get_width(),ani[0][0][0].get_height())
        self.hitbox = pygame.Rect(self.rect.center[0],self.rect.center[1],rad*2,rad*2)
    
    def spawn(self):
        self.hitbox.center = (self.rect.center[0]-state.scr,self.rect.center[1]-state.scr_y)
        if self.hitbox.colliderect(pygame.Rect(state.hero.rect.center[0]-300-state.Width/2,state.hero.rect.center[1]-300-state.Height/2,state.Width+600,state.Height+600)):
            self.AI(state.hero.rect)
            if self.ani[4] != self.ani[5]:
                self.ani[5] = self.ani[4]
                self.ani[0] = 0
                self.ani[2] = 0
            try:
                self.ani[3] = len(self.anim[self.ani[4]])
            except:
                print(self.ani)
            self.ani[0] += 1
            if self.ani[0] >= self.ani[1]:
                self.ani[0] = 0
                self.ani[2] += 1
                if self.ani[2] >= self.ani[3]:
                    self.ani[2] = 0

            #pygame.draw.rect(state.screen,(0,123,234),self.hitbox)
            state.screen.blit(pygame.transform.flip(self.anim[self.ani[4]][self.ani[2]],self.flip[0],False),(self.rect[0]-state.scr,self.rect[1]-state.scr_y))
            if not self.health[1] >= self.health[0]:
                self.health[2] += 1
                if self.health[2] > self.health[3]:
                    self.health[1] += 1
                    self.health[2] = 0
                self.health_bar.draw((self.rect.topleft[0]-state.scr,self.rect.topleft[1]-30-state.scr_y),self.health[1])

    def AI(self,player):
        if self.hitbox.colliderect(player):
            self.active = True
        else:
            self.active = False
        if pygame.Rect(self.rect.x-state.scr,self.rect.y-state.scr_y,self.rect.w,self.rect.h).colliderect(player):
            state.hero.health[1] -= 0.5
        
        if not self.active:
            if self.rect.x+self.ranged[2] > self.plat.x+self.plat.w or self.rect.x-self.ranged[2] < self.plat.x:
                self.flip[1] *= -1
                if self.flip[1] > 0:
                    self.flip[0] = True
                else:
                    self.flip[0] = False
            self.rect.x += self.flip[1]
            self.ani[4] = 0
        else:
            if self.ranged[0]:
                self.ani[4] = 1
                self.proj[-2] += 1
                if self.proj[-2] >= self.proj[-1]:
                    self.proj[-2] = 0
                    state.projectiles.insert(0,bulet(self.rect.center[0]-state.scr,self.rect.center[1]-state.scr_y,player.center[0],player.center[1],self.ranged[1]))
                    state.Sound_effects[1].play()
            else:
                if player.x > self.rect.x-state.scr:
                    if self.rect.x + self.ranged[1] < self.plat.x+self.plat.w-self.rect.w:
                        self.flip[0] = False
                        self.rect.x += self.ranged[1]
                elif player.x < self.rect.x-state.scr:
                    if self.rect.x - self.ranged[1] > self.plat.x:
                        self.rect.x -= self.ranged[1]
                        self.flip[0] = True

    def death(self,gun):
        if gun.active:
            angect = pygame.Rect(self.rect.center[0]-state.scr,self.rect.center[1]-state.scr_y,self.rect.w,self.rect.h)
            if math.sqrt((angect.x-gun.x)**2 + (angect.y-gun.y)**2) < gun.w:
                B = -math.atan2(angect.y-gun.y,angect.x-gun.x)
                #print(B,gun.ang_gun)           
                if math.tan(B) > math.tan(math.radians(gun.an - gun.ang_gun)) and math.tan(B) < math.tan(math.radians(gun.an + gun.ang_gun)):
                    self.health[1] -= 0.1
                    if self.health[1] < 0:
                        return True
        return False

class bulet:
    def __init__(self,x,y,x1,y1,r):
        self.r = math.atan2(y-y1,x1-x)
        self.x = x
        self.y = y
        #self.mov = [math.cos(self.r)*20,math.sin(self.r-math.pi)*20]
        self.movement = [math.sin(self.r-math.pi)*15,math.cos(self.r)*15]
        self.ani = [0,5,0,len(r)]
        self.rad = r
        self.rect = pygame.Rect(x,y,r[0].get_width()*1.5,r[0].get_height()*1.5)
        self.scr = [0,0,state.scr,state.scr_y]
    def blulet(self,gun):
        self.scr = [self.scr[2]-state.scr,self.scr[3]-state.scr_y,state.scr,state.scr_y]
        self.rect = pygame.Rect(self.rect.x+self.scr[0],self.rect.y+self.scr[1],self.rect.w,self.rect.h)
        if gun.active:
            if math.sqrt((self.rect.x-gun.x)**2 + (self.rect.y-gun.y)**2) < gun.w:
                B = -math.atan2(self.rect.y-gun.y,self.rect.x-gun.x)
                if math.tan(B) > math.tan(math.radians(gun.an - gun.ang_gun)) and math.tan(B) < math.tan(math.radians(gun.an + gun.ang_gun)):
                    return True
        if self.rect.colliderect(state.hero.rect):
            state.hero.health[1] -= 2
            #print(-math.degrees(math.atan2(self.rect.y-gun.y,self.rect.x-gun.x)),gun.an)
            return True
        self.movement[0] += 0.01
        self.movement[1] *= 0.999

        if self.ani[0] == self.ani[1]:
            self.ani[0] = 0
            self.ani[2] += 1
            if self.ani[2] == self.ani[3]:
                self.ani[2] = 0
        else:
            self.ani[0] += 1
        if not self.rect.colliderect(pygame.Rect(-100,-100,state.Width+200,state.Height+200)):
            return True

        self.rect.y += self.movement[0]
        self.rect.x += self.movement[1]

        state.screen.blit(self.rad[self.ani[2]],(self.rect.center[0],self.rect.center[1]))