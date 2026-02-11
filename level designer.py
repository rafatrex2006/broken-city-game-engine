import pygame
import csv
import math

pygame.init()
Width = 800
Height = 600
screen = pygame.display.set_mode((Width, Height))
clock = pygame.time.Clock()
level = 1

colls = 12
tile_s = 800/16
tile_copy = 800/16

#colors
black = (0,0,0)
white = (255,255,255)
color = (255,255,255)
red = (255,0,0)
green = (0,255,0)
brown = (101,67,33)

#scr
scr = 0
scr_y = 0
scl = False
scrr = False
scu = False
scd = False
scr_s = 1

#zoom
zoom = 1
zow = False
zup = False

#special tiles(enemies etc...)
enter = False
enemies= []
Specials = [False,False,False,False]

spec_tiles = [0,0]
St_surf = [pygame.Surface((100,100)),pygame.Surface((50,50))]
St_surf[0].fill(green)
St_surf[1].fill(green)
Stiles = []
Stiles_c = []

#tiles load
l_dic = ["","t","l","r","b","tl","tr","tb","lr","lb","rb","tlr","tlb","trb","lrb","tlrb"]
t_dic = {}
for i in range(16):
    imag = pygame.image.load(f"assets/tiles/forest/{i}.png").convert_alpha()
    t_dic[l_dic[i]] = pygame.transform.scale(imag,(50,50))
#tiles
def S_ad(string = ""):
    return pygame.transform.scale(t_dic[string],(int(tile_s*zoom)+2,int(tile_s*zoom)+2))

def new_map(lv,pl = False):
    global scr,scr_y,enemies,Stiles,Stiles_c
    tiles = []
    with open(f"Assets\level {lv}_data.csv", newline="") as f:
        reader = csv.reader(f)
        platform_list = list(reader)
    for x,i in enumerate(platform_list):
        for y,p in enumerate(i):
            platform_list[x][y] = int(p)
    for b in platform_list[:-2]:
        c = 0
        for i in reversed(range(1,17)):
            for v in range(b[-i-1]):
                if pl:
                    tiles.append([pygame.Rect(b[c],b[-1],50,50),t_dic[l_dic[16-i]],l_dic[16-i]])
                else:
                    tiles.append([pygame.Rect(b[c],b[-1],50,50),t_dic[l_dic[16-i]]])
                c += 1
    if pl:
        for k in range(len(platform_list[-1])//9):
            enemies.append([pygame.Rect(platform_list[-1][0+9*k],platform_list[-1][1+9*k],platform_list[-1][2+9*k],platform_list[-1][3+9*k]),[platform_list[-1][4+9*k],platform_list[-1][5+9*k]],platform_list[-1][6+9*k],platform_list[-1][7+9*k],platform_list[-1][8+9*k]])
        for l in range(len(platform_list[-2])//3):
            if platform_list[-2][2+3*l] == 2:
                Stiles.append([pygame.Rect(platform_list[-2][0+3*l],platform_list[-2][1+3*l],tile_s*2,tile_s*2),St_surf[0]])
                Stiles_c.append([pygame.Rect(platform_list[-2][0+3*l],platform_list[-2][1+3*l],tile_s*2,tile_s*2),St_surf[0]])
            elif platform_list[-2][2+3*l] == 1:
                Stiles.append([pygame.Rect(platform_list[-2][0+3*l],platform_list[-2][1+3*l],tile_s,tile_s),St_surf[1],platform_list[-2][2+3*l]])
                Stiles_c.append([pygame.Rect(platform_list[-2][0+3*l],platform_list[-2][1+3*l],tile_s,tile_s),St_surf[1],platform_list[-2][2+3*l]])
            elif platform_list[-2][2+3*l] == 3:
                print(platform_list[-2][0+3*l],platform_list[-2][1+3*l])
                Stiles.append([pygame.Rect(platform_list[-2][0+3*l],platform_list[-2][1+3*l],tile_s,tile_s),St_surf[1],platform_list[-2][2+3*l]])
                Stiles_c.append([pygame.Rect(platform_list[-2][0+3*l],platform_list[-2][1+3*l],tile_s,tile_s),St_surf[1],platform_list[-2][2+3*l]])
    return tiles

tiles = new_map(level)
tiles_c = new_map(level,True)

drawing = False
drawing1 = False
hit_list = []

def load_background(ti,st):
    for i in ti:
        screen.blit(i[1],i[0])
    for e in enemies:
        pygame.draw.rect(screen,white,((e[0].x-scr)*zoom,(e[0].y-scr_y)*zoom,(e[0].w)*zoom,(e[0].h)*zoom),2)
    for o in st:
        screen.blit(o[1],o[0])

def col_to_tile(tc):
    new_rect = pygame.Rect((mouse[0]+scr)//tile_s*tile_s,(mouse[1]+scr_y)//tile_s*tile_s,tile_s,tile_s)
    #pygame.draw.rect(screen,(255,0,0),new_rect,3)
    for i in tc:
        if i[0].collidepoint((new_rect[0],new_rect[1])):
            return False
    return True

def col_to_spec(tc,st,r):
    #pygame.draw.rect(screen,(255,0,0),new_rect,3)
    Scol = []
    for z in range(r[1]**2):
        Scol.append((mouse[0]*zoom+(tile_s+10*zoom)*((z/2-math.floor(z/2))*2),mouse[1]*zoom+(tile_s+10*zoom)*math.ceil((z-1)/2)))
        pygame.draw.rect(screen,red,(mouse[0]*zoom+(tile_s+10*zoom)*((z/2-math.floor(z/2))*2),mouse[1]*zoom+(tile_s+10*zoom)*math.ceil((z-1)/2),4,4))
    if not r[3]:
        for i in tc:
            for x in Scol:
                if i[0].collidepoint(x):
                    return False
    for o in st:
        for y in Scol:
            if o[0].collidepoint(y):
                return False
    return True

def rearenge(t,fu):
    for i in t[0]:
        img_ex = "tlrb"
        ind = fu.index(i)
        for b in t[1]:
            if b[0].collidepoint((i[0].x + 5,i[0].y - 5)):
                img_ex = img_ex.replace('t','')
            if b[0].collidepoint((i[0].x - 4,i[0].y + 4)):
                img_ex = img_ex.replace('l','')
            if b[0].collidepoint((i[0].x + tile_s + 3,i[0].y + 3)):
                img_ex = img_ex.replace('r','')
            if b[0].collidepoint((i[0].x + 5,i[0].y + tile_s + 5)):
                img_ex = img_ex.replace('b','')

        tiles[ind][1] = S_ad(img_ex)
        tiles_c[ind][2] = img_ex


def gib_screen(t,tc,rect):
    ret = []
    ret1 = []
    fora = pygame.Rect(rect.x-rect.w,rect.y-rect.h,rect.w*3,rect.h*3)
    fora1 = pygame.Rect(rect.x-rect.w*2,rect.y-rect.h*2,rect.w*5,rect.h*5)

    #pygame.draw.rect(screen,white,fora)
    #pygame.draw.rect(screen,white,fora1)
    for x,i in enumerate(t):
        if i[0].colliderect(fora):
            ret.append(tc[x])

        if i[0].colliderect(fora1):
            ret1.append(tc[x])

    return [ret,ret1]

def gib_around(tc,rect):
    ret = []
    ret1 = []
    fora = pygame.Rect(rect.x-rect.w,rect.y-rect.h,rect.w*3,rect.h*3)
    fora1 = pygame.Rect(rect.x-rect.w*2,rect.y-rect.h*2,rect.w*5,rect.h*5)

    #pygame.draw.rect(screen,white,fora)
    #pygame.draw.rect(screen,white,fora1)
    for i in tc:
        if i[0].colliderect(fora):
            ret.append(i)
        if i[0].colliderect(fora1):
            ret1.append(i)

    return [ret,ret1]


def zoomLoad(up,down):
    global zoom
    
    z = False
    if up:
        if zoom < 3:
            zoom += 0.01
            z = True
    if down:
        if zoom > 0.1:
            zoom -= 0.01
            z = True
    zoom = round(zoom,3)
    if z:
        for i in tiles:
            i[1] = pygame.transform.scale(t_dic[tiles_c[tiles.index(i)][2]],(int(tile_s*zoom)+2,int(tile_s*zoom)+2))
        for y,o in enumerate(Stiles):
            o[1] = pygame.transform.scale(Stiles_c[y][1],(int(Stiles_c[y][1].get_width()*zoom)+2,int(Stiles_c[y][1].get_height()*zoom)+2))



            
    return zoom

def c_zoom(ti,ti_co,stc,st,ts):
    for x,z in enumerate(ti_co):
        ti[x][0] = pygame.Rect((z[0][0]-scr)*zoom,(z[0][1]-scr_y)*zoom,ts*zoom,ts*zoom)
    for y,a in enumerate(stc):
        st[y][0] = pygame.Rect((a[0][0]-scr)*zoom,(a[0][1]-scr_y)*zoom,a[0][2]*zoom,a[0][3]*zoom)

run = True
while run:
    screen.fill(black)
    clock.tick(60)
    mouse = pygame.mouse.get_pos()
    mouse = [mouse[0]/zoom,mouse[1]/zoom]
    if scl:
        scr -= 5 * scr_s
    if scrr:
        scr += 5 * scr_s
    if scd:
        scr_y += 5 * scr_s
    if scu:
        scr_y -= 5 * scr_s
    zoomLoad(zup,zow)
    c_zoom(tiles,tiles_c,Stiles_c,Stiles,tile_s)
    load_background(tiles,Stiles)
    if Specials[0] == True or Specials[1]:
        if pygame.mouse.get_pressed()[1]:
            Specials[-2] = True
            enter = False
            ammount = [0,0]
            enemy = [pygame.Rect((mouse[0]+scr)//tile_s*tile_s,(mouse[1]+scr_y)//tile_s*tile_s,tile_s,tile_s),pygame.Rect((mouse[0]+scr)//tile_s*tile_s,(mouse[1]+scr_y)//tile_s*tile_s,tile_s,tile_s)]
            platf = [pygame.Rect((mouse[0]+scr)//tile_s*tile_s,(mouse[1]+scr_y)//tile_s*tile_s,tile_s,tile_s),pygame.Rect((mouse[0]+scr)//tile_s*tile_s,(mouse[1]+scr_y+tile_s)//tile_s*tile_s,tile_s,tile_s)]
        if Specials[-2]:
            enemy[0] = pygame.Rect((enemy[1][0]-scr)*zoom,(enemy[1][1]-scr_y)*zoom,enemy[1][2]*zoom,enemy[1][3]*zoom)
            platf[0] = pygame.Rect((platf[1][0]-scr)*zoom,(platf[1][1]-scr_y)*zoom,platf[1][2]*zoom,platf[1][3]*zoom)
            Distance = (mouse[0]+scr-enemy[1].midbottom[0])//tile_s
            if Distance-ammount[0] > 0:
                platf[0].w += ((Distance-ammount[0])*tile_s)*zoom
            elif Distance-ammount[1] < 0:
                platf[0].x += ((Distance-ammount[1])*tile_s)*zoom
                platf[0].w -= ((Distance-ammount[1])*tile_s)*zoom
            if pygame.mouse.get_pressed()[0]:
                if Distance > ammount[0]:
                        platf[1].w += (Distance-ammount[0])*tile_s
                        ammount[0] = Distance
                elif Distance < ammount[1]:
                        platf[1].x += (Distance-ammount[1])*tile_s
                        platf[1].w -= (Distance-ammount[1])*tile_s
                        ammount[1] = Distance

            
            pygame.draw.rect(screen,white,enemy[0],2)
            pygame.draw.rect(screen,red,platf[0],1)
            pygame.draw.rect(screen,green,(enemy[0].midbottom[0],enemy[0].midbottom[1],5,5))
        if enter:
            Specials[-2] = False
            #[platform,[ranged ot not(1,2),if 2 range], Health, Attack, type(type of monster)]
            if not Specials[-1]:
                Specials[-1] = True
                enemies.insert(0,[platf[1],[0,0],0,0,0])
                for x,i in enumerate(["health","attack","type"]):
                    while True:
                        try:
                            var = input("What is the "+i+" of the monster: ")
                            var = int(var)
                            enemies[0][x+2] = var
                            break
                        except:
                            print("A number plz.")
                            continue
            if Specials[1]:
                range_r = (mouse[0]+scr-enemy[1].center[0])*zoom
                enemy[0] = pygame.Rect((enemy[1][0]-scr)*zoom,(enemy[1][1]-scr_y)*zoom,enemy[1][2]*zoom,enemy[1][3]*zoom)
                range_rect = pygame.Rect(enemy[0].center[0]-range_r, enemy[0].center[1]-range_r, range_r*2, range_r*2)
                range_rect.center = enemy[0].center
                pygame.draw.rect(screen,(230,230,250),range_rect,4)
                if pygame.mouse.get_pressed()[0]:
                    enemies[0][1][0] = 1
                    enemies[0][1][1] = round(range_r/zoom,-1)
                    Specials = [False,False,False,False]
                    enter = False
                    print(enemies)
            else:
                enemies[0][1][0] = 0
                Specials = [False,False,False,False]
                enter = False
                print(enemies)
    elif (pygame.mouse.get_pressed()[2] or pygame.mouse.get_pressed()[1]) and not drawing and not drawing1:
        col_rect = pygame.Rect(mouse[0]*zoom,mouse[1]*zoom,0,0)
        x_col = mouse[0]*zoom
        y_col = mouse[1]*zoom
        copy = scr
        copy_y = scr_y
        if pygame.mouse.get_pressed()[1]:
            drawing1 = True
        if pygame.mouse.get_pressed()[2]:
            drawing = True
    elif drawing or drawing1:
        col_rect.w = mouse[0]*zoom- x_col
        col_rect.h = mouse[1]*zoom - y_col
        #col_rect.x = x_col - (scr - copy)
        #col_rect.y = y_col - (scr_y - copy_y)
        if drawing1:
            pygame.draw.rect(screen,green,col_rect,2)
        elif drawing:
            pygame.draw.rect(screen,red,col_rect,2)

        if not pygame.mouse.get_pressed()[2] and not pygame.mouse.get_pressed()[1]:
            #col_rect.x = col_rect.x - scr
            #col_rect.y = col_rect.y - scr_y
            drawing = False
            for i in reversed(tiles):
                if i[0].colliderect(col_rect):
                    tiles_c.remove(tiles_c[tiles.index(i)])
                    tiles.remove(i)
            for i in reversed(enemies):
                if pygame.Rect((i[0].x-scr)*zoom,(i[0].y-scr_y)*zoom,i[0].w*zoom,i[0].h*zoom).colliderect(col_rect):
                    enemies.remove(i)
            for i in reversed(Stiles):
                if i[0].colliderect(col_rect):
                    Stiles_c.remove(Stiles_c[Stiles.index(i)])
                    Stiles.remove(i)
            if drawing1:
                if col_rect[2] < 0 and col_rect[3] < 0:
                    col_rect = pygame.Rect(col_rect.bottomright[0] ,col_rect.bottomright[1] ,abs(col_rect[2]) ,abs(col_rect[3]))
                elif col_rect[2] < 0:
                    col_rect = pygame.Rect(col_rect.topright[0] ,col_rect.topright[1] ,col_rect[2] ,abs(col_rect[3]))
                elif col_rect[3] < 0:
                    col_rect = pygame.Rect(col_rect.bottomleft[0] ,col_rect.bottomleft[1] ,abs(col_rect[2]) ,col_rect[3] )

                tile_z = tile_s*zoom
                for i in range(abs(int(col_rect[2]//tile_z))+1):
                    for o in range(abs(int(col_rect[3]//tile_z))+1):
                        tiles.append([pygame.Rect(col_rect.topleft[0]//tile_z*tile_z+tile_z*i, col_rect.topleft[1]//tile_z*tile_z+tile_z*o, tile_z,tile_z),S_ad()])
                        #tiles_c.append([pygame.Rect((col_rect.topleft[0]//tile_z*tile_z)/zoom+scr+tile_s*i,(col_rect.topleft[1]//tile_z*tile_z)/zoom+scr_y+tile_s*o, tile_s,tile_s),S_ad(),""])
                        tiles_c.append([pygame.Rect(((col_rect.topleft[0]/zoom+scr)//tile_s*tile_s+tile_s*i),((col_rect.topleft[1]/zoom+scr_y)//tile_s*tile_s+tile_s*o), tile_s,tile_s),S_ad(),""])
                        #print(((col_rect.topleft[0]/zoom+scr)//tile_s*tile_s+tile_s*i))
            drawing1 = False
            rearenge(gib_screen(tiles,tiles_c,pygame.Rect(-100,-100,900,700)),tiles_c)
    elif pygame.mouse.get_pressed()[0]:
        if spec_tiles[0] != 0:
            #pygame.draw.rect(screen,red,pygame.Rect((mouse[0]//tile_s*tile_s)*zoom,(mouse[1]//tile_s*tile_s)*zoom,tile_s*zoom*spec_tiles[1],tile_s*zoom*spec_tiles[1]))
            if col_to_spec(tiles,Stiles,spec_tiles):
                Stiles.append([pygame.Rect((mouse[0]+scr)//tile_s*tile_s,(mouse[1]+scr_y)//tile_s*tile_s,tile_s*spec_tiles[1],tile_s*spec_tiles[1]),pygame.transform.scale(spec_tiles[2],(int(spec_tiles[2].get_width()*zoom)+2,int(spec_tiles[2].get_height()*zoom)+2)),spec_tiles[0]])
                Stiles_c.append([pygame.Rect((mouse[0]+scr)//tile_s*tile_s,(mouse[1]+scr_y)//tile_s*tile_s,tile_s*spec_tiles[1],tile_s*spec_tiles[1]),spec_tiles[2],spec_tiles[0]])

        else:
            if col_to_tile(tiles_c):
                add = pygame.Rect((mouse[0]+scr)//tile_s*tile_s,(mouse[1]+scr_y)//tile_s*tile_s,tile_s,tile_s)
                tiles.append([add,S_ad()])
                tiles_c.append([add,S_ad(),""])
                rearenge(gib_around(tiles_c,add),tiles_c)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                drawing = False
            #zoom
            if event.key == pygame.K_e:
                zow = True
            if event.key == pygame.K_q:
                zup = True
            #scrollds
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                scl = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                scrr = True
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                scu = True
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                scd = True
            if event.key == pygame.K_LSHIFT  or event.key == pygame.K_RSHIFT:
                scr_s = 5
            if event.key == pygame.K_1:
                Specials[0] = True
            if event.key == pygame.K_2:
                Specials[1] = True

            if event.key == pygame.K_3:
                spec_tiles = [1,1,St_surf[1],False]
            if event.key == pygame.K_4:
                spec_tiles = [2,2,St_surf[0],False]
            if event.key == pygame.K_5:
                spec_tiles = [3,1,St_surf[1],True]
            if event.key == pygame.K_0:
                spec_tiles = [0,0,0]

            if event.key == pygame.K_RETURN:
                enter = True
        if event.type == pygame.KEYUP:
            #zoom
            if event.key == pygame.K_e:
                zow = False
            if event.key == pygame.K_q:
                zup = False
            #scrool
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                scl = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                scrr = False
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                scu = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                scd = False
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                scr_s = 1


    pygame.display.update()

#print(tiles_c)
export = []
for z in tiles_c:
    new = True
    k = l_dic.index(z[2])-17
    for n in export:
        if z[0].y == n[-1]:
            kk = 0
            for i in range(-17,k):
                kk += n[i]
            new = False
            n[k] += 1
            n.insert(kk,(z[0].x))
    if new:
        export.insert(0,[z[0].x,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,z[0].y])
        export[0][k] += 1

export.insert(len(export),[1])
enemy_n = 0
for i in enemies:
    for x in range(4):
        export[len(export)-1].insert(enemy_n,i[0][x])
        enemy_n += 1
    for y in range(2):
        export[len(export)-1].insert(enemy_n,int(i[1][y]))
        enemy_n += 1
    for z in range(3):
        export[len(export)-1].insert(enemy_n,i[z+2])
        enemy_n += 1

export.insert(-1,[1])
#[Rect,image,type]
for i in Stiles_c:
    export[-2].insert(0,i[2])
    export[-2].insert(0,i[0][1])
    export[-2].insert(0,i[0][0])


print(export[-1])

with open(f"Assets/level {level}_data.csv" , "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter = ",")
            for r in export:
                writer.writerow(r)

pygame.quit()