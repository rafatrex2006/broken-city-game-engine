import pygame
import math
from engine import state
from systems.cutscene import cutscene

def load():
    #music
    pygame.mixer.music.load("assets\Main music.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    #Sound effects
    Sound_effects = []
    for i in range(4):
        SN = pygame.mixer.Sound(f"assets/Sounds/{i}.wav")
        SN.set_volume(0.1)
        Sound_effects.insert(len(Sound_effects),SN)
    state.Sound_effects = Sound_effects

    #Tiles
    l_dic = [[],[]]
    for i in range(16):
        imag = pygame.image.load(f"assets/tiles/forest/{i}.png").convert_alpha()
        l_dic[0].insert(-1,pygame.transform.scale(imag,(state.tile_size,state.tile_size)))
    for i in range(16):
        imag = pygame.image.load(f"assets/tiles/city/{i}.png").convert_alpha()
        l_dic[1].insert(-1,pygame.transform.scale(imag,(state.tile_size,state.tile_size)))
    state.l_dic = l_dic

    #Enemy sprites
    state.Monster_ani = []
    nm = []
    for i in [["run",4],["idle",5]]:
        nl = []
        for x in range(i[1]):
            nl.append(pygame.transform.scale((pygame.image.load(f"assets/enemies/1/{i[0]}/{x}.png").convert_alpha()),(70,70)))
        nm.append(nl)
    state.Monster_ani.append(nm)
    nm = []
    for i in [["rool",4]]:
        nl = []
        for x in range(i[1]):
            nl.append(pygame.transform.scale((pygame.image.load(f"assets/enemies/2/{i[0]}/{x}.png").convert_alpha()),(70,70)))
        nm.append(nl)
    state.Monster_ani.append(nm)

    #animations
    ani_list = []
    nani = []
    Load_dic = {"idle":[2,(50,100)],"run":[3,(55,100)],"gun_active":[3,(60,100)],"gun_i_active":[1,(55,100)],"gun_run":[3,(60,100)],"gun_idle":[1,(60,100)]}
    for key in Load_dic:
        nani = []
        for i in range(Load_dic[key][0]+1):
            n = pygame.image.load(f"assets/animations/Main person/{key}/{i}.png").convert_alpha()
            n = pygame.transform.scale(n,Load_dic[key][1])
            nani.append(n)
        ani_list.append(nani)
    nani = []
    for i in range(5):
        n = pygame.image.load(f"assets/animations/Main person/death/{i}.png").convert_alpha()
        n = pygame.transform.scale(n,(100,100))
        nani.append(n)
    ani_list.insert(len(ani_list),nani)
    state.ani_list = ani_list
    #cutscenes
    state.cutscenes = [cutscene("assets/cutscenes/1/",37),cutscene("assets/cutscenes/2/",32)]
