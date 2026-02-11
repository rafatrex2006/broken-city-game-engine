import pygame
import math
import random
from engine import state
from engine.bootstrap import init
from engine.assets import load
from entities.player import Player
from entities.boss import boss
from entities.gun import gun
from systems.ui import Map2
from levels.level_loader import Map, new_map

class Game:
    def __init__(self):
        #system initialization(bootstrap & Assets)
        init()
        load()

        #colors
        #background = (52,218,201)
        state.background = pygame.image.load("assets/backgrounds/2.png").convert_alpha()

        #scr
        state.scr = 0
        state.scr_y = 0
        state.scr_allow = True
        state.G = 0.3

        #particles
        state.particles =[]

        #inputs
        state.E_input = False

        #map congig
        state.map_T = True

        #projectiles for enemies
        state.projectiles = []

        #Map Variables
        state.enemies = []
        state.Stiles = []

        #Object Initiation
        self.trygun = gun((300,300))

        self.hero = Player(200,100,1,state.ani_list)
        self.hero_inputs = [False,False,False,False]
        state.hero = self.hero

        self.Boss = boss(500)
        state.boss_death = False

        self.surfs = [pygame.transform.scale(pygame.image.load("assets\masks and others\level1.png").convert_alpha(),(100,100)),pygame.transform.scale(pygame.image.load("assets\masks and others\level2.png").convert_alpha(),(100,100)),pygame.transform.scale(pygame.image.load("assets\masks and others\level3.png").convert_alpha(),(50,50)),pygame.transform.scale(pygame.image.load("assets\masks and others\level4.png").convert_alpha(),(100,100))]
        self.surf2 = []
        for i in range(31):
            im = pygame.image.load(f"assets/map/{i}.png").convert_alpha()
            im = pygame.transform.scale(im,(im.get_width()*2,im.get_height()*2))
            self.surf2.append(im)
        self.map = Map(self.surf2,[[[200,400],self.surfs[0],True,1, 0],[[1150,325],self.surfs[1],False,2, 0],[[725,500],self.surfs[2],False,3, 1],[[675,300],self.surfs[3],False,4, 1]])
        obs = [pygame.Rect(180,210,410,10),pygame.Rect(10,590,780,10),pygame.Rect(0,290,10,310),pygame.Rect(790,300,10,300),pygame.Rect(780,290,20,10),pygame.Rect(770,280,30,10),pygame.Rect(750,270,50,10),pygame.Rect(730,260,70,10),pygame.Rect(660,210,10,10),pygame.Rect(670,210,20,20),pygame.Rect(690,210,20,30),pygame.Rect(710,210,90,50),pygame.Rect(30,260,20,10),pygame.Rect(20,260,10,20),pygame.Rect(0,260,20,30),pygame.Rect(110,210,10,10),pygame.Rect(90,210,20,20),pygame.Rect(70,210,20,30),pygame.Rect(0,0,800,210),pygame.Rect(0,210,70,50),pygame.Rect(160,300,240,140),pygame.Rect(150,300,10,130),pygame.Rect(140,300,10,100),pygame.Rect(130,300,10,20),pygame.Rect(400,310,230,140),pygame.Rect(630,320,10,130),pygame.Rect(640,330,10,120),pygame.Rect(650,380,10,70)]
        state.map2 = [Map2(pygame.image.load("assets/map/map 2.png").convert_alpha(),obs,[[(400,200),1]]),True]
        state.tiles = new_map(state.level,state.l_dic[0],self.map)
        state.tiles_copy = new_map(state.level,state.l_dic[1],self.map,True)


    def run(self):
        run = True
        while run:
            state.screen.blit(state.background,(0,0))
            state.clock.tick(60)

            if not state.map2[-1]and not state.map_T and not state.boss_death and state.level == 4:
                if self.Boss.draw(self.trygun):
                    state.boss_death = True
            for i in state.projectiles:
                if i.blulet(self.trygun):
                    state.projectiles.remove(i)

            for o,i in enumerate(state.tiles):
                #remove if laggy
                for z in state.projectiles:
                    if z.rect.colliderect(i[0]):
                        state.projectiles.remove(z)
                #___________________________
                i[0].x = state.tiles_copy[o][0].x - state.scr
                i[0].y = state.tiles_copy[o][0].y - state.scr_y
                state.screen.blit(i[1],i[0])
            for i in state.Stiles:
                i.draw()
            for i in state.particles:
                if i.draw():
                    state.particles.remove(i)
            self.hero.blitt(self.trygun,self.Boss)
            if state.map2[-1]:
                state.map2[0].start(self.hero_inputs)
            elif state.map_T:
                self.map.m_draw(self.hero_inputs,state.l_dic,self.map)
            else:
                self.hero.move(self.hero_inputs,state.tiles)
                self.trygun.draw(self.hero)
                for i in reversed(state.enemies):
                    i.spawn()
                    if i.death(self.trygun):
                        state.enemies.remove(i)

            for i in state.cutscenes:
                i.draw()
            if not state.boss_death and state.level == 4:
                self.Boss.drawtop()

            #Inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.hero_inputs[0] = True
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.hero_inputs[1] = True
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.hero_inputs[2] = True
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.hero_inputs[3] = True
                    if event.key == pygame.K_e:
                        state.E_input = True
                    if event.key == pygame.K_f:
                        self.Boss.f = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.hero_inputs[0] = False
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.hero_inputs[1] = False
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.hero_inputs[2] = False
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.hero_inputs[3] = False
                    if event.key == pygame.K_e:
                        state.E_input = False
                    if event.key == pygame.K_f:
                        self.Boss.f = False
            
            pygame.display.update()