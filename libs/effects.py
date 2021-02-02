import libs.game as game
import pygame
import random

i_shake=0
def shake_screen():
    global i_shake
    b=True
    ofs=[[-20,-20],[-15,-15],[-10,-10],[-5,-5],[0,0],[5,5],[10,10],[15,15],[20,20],[15,15],[10,10]]
    i_shake += 1
    if i_shake > 9:
        b=False
        i_shake=0
    return ofs[i_shake-1], b

def dimm(wnd,wx,wy):
    s = pygame.Surface((wx, wy))
    s.set_alpha(128)
    s.fill((0, 0, 0))
    wnd.blit(s, (0, 0))


class Trail:
    def __init__(self,wnd,xy,spdxy,pre_trail):
        self.window=wnd
        self.x=xy[0]+random.randint(-15,15)
        self.y=xy[1]+80+random.randint(0,15)
        self.spdxy=[spdxy[0],spdxy[1]+2]
        self.ship_spd_y=spdxy[1]
        self.pre_trail=pre_trail
        self.i_trail=0
        wh=pre_trail[0].get_size()
        self.xi=wh[0]//2
        self.yi=wh[1]//2



    def move(self):
        self.x+=self.spdxy[0]*game.delta_t
        self.y+=self.spdxy[1]*game.delta_t
        if self.spdxy[1]> self.ship_spd_y+1:
            self.spdxy[1]-=0.01*game.delta_t
            self.spdxy[0]*= 0.01*game.delta_t
        self.i_trail+=1


    def rajz(self):
        if self.i_trail < len(self.pre_trail):
            self.window.blit(self.pre_trail[self.i_trail], dest=(self.x - self.xi+game.offset[0]*0.5, self.y-self.yi+game.offset[1]*0.5))
        if game.delta_t > 0:
            self.move()

def onsetup_trail(wnd,img):
    opacity=255
    trail=[]

    for i in range(30):
        bmp=pygame.Surface((img.get_width(), img.get_height())).convert()
        bmp.blit(wnd, (0, 0))
        bmp.blit(img, (0, 0))
        bmp.set_alpha(opacity)
        opacity-=10
        trail.append(bmp)
    return trail
