import random
import libs.game as game
from libs.blasts import Bomb
import pygame

"""
dimenziok: w=180,y=128
"""
class Invader:
    def __init__(self, img, wnd,wx,wy):
        self.img=img
        self.wy=wy
        self.wx=wx
        self.wnd=wnd
        self.y=-55
        self.value=1
        self.defspd=(0,0.2)
        self.spdxy=list(self.defspd)
        self.health=1
        self.accel=0.0005
        wh=img.get_size()
        self.xi=wh[0]//2
        self.yi=wh[1]//2
        self.mask=game.invader_mask
        self.safemode=False
        self.t_safemode=0

        gen=True
        while gen:
            self.x=random.randrange(self.xi,self.wx-self.xi)
            if len(game.invaders) > 1:
                if game.invaders[-2].collision(self.x,self.y,self.xi,self.yi,mask=self.mask):
                    gen=True
                else:
                    gen=False
            else:
                gen = False

    def getvalue(self):
        return self.value

    def move(self):
        if self.spdxy[0]>self.defspd[0]:
            self.spdxy[0]-=game.delta_t*self.accel
        elif self.spdxy[0]<self.defspd[0]:
            self.spdxy[0]+=game.delta_t*self.accel

        if self.spdxy[1]>self.defspd[1]:
            self.spdxy[1]-=game.delta_t*self.accel
        elif self.spdxy[1]<self.defspd[1]:
            self.spdxy[1]+=game.delta_t*self.accel

        self.x+= self.spdxy[0] * game.delta_t
        self.y+= self.spdxy[1] * game.delta_t
        self.testforcollision(selfmask=self.mask)


    def rajz(self):
        self.wnd.blit(self.img,dest=(self.x-self.xi+game.offset[0],self.y-self.yi+game.offset[1]))
        self.move()

        if self.safemode:
            self.t_safemode+=game.delta_t
            if self.t_safemode > 500:
                self.safemode=False
                self.t_safemode=0


    def alive(self):
        return self.y < self.wy+100 and self.health > 0

    def collision(self,x,y,xi,yi,mask):
        if ((abs(x - self.x) <=(self.xi+xi)) and (abs(y-self.y) <= (self.yi+yi))):
            offs = [int((x - xi)-(self.x - self.xi)), int((y - yi)-(self.y - self.yi))]
            return game.invader_mask.overlap(mask,offs)
        else:
            return False

    def health_val(self,val=0):
        if self.safemode and val < 0:
            val=0
        self.health+=val
        return self.health

    def knock_back(self,x,y,spdx,spdy):
        if x>self.x:
            self.spdxy[0]=-abs(spdx*0.5)
        elif x < self.x:
            self.spdxy[0]=+abs(spdx*0.5)
        if y>self.y:
            self.spdxy[1]=-abs(spdy*0.5)
        elif y<self.y:
            self.spdxy[1]=+abs(spdy*0.5)

    def testforcollision(self,selfmask):
        if game.ship.collision(self.x, self.y, self.xi, self.yi,mask=selfmask):
            spd=list(self.spdxy)
            self.knock_back(game.ship.getxy()[0],game.ship.getxy()[1],game.ship.getspd()[0],game.ship.getspd()[1])
            game.ship.knock_back(self.x,self.y,spd[0],spd[1])
            game.ship.health_val(-1)


class Bomber(Invader):
    def __init__(self, img, bombimg, wnd,wx,wy):
        Invader.__init__(self, img, wnd,wx,wy)
        self.bombimg=bombimg
        self.x=self.wx+100
        self.y=random.randint(50,self.wy//2)
        self.defspd=(-0.3, 0.1)
        self.spdxy=list(self.defspd)
        self.bomb_interval=1500
        self.t_bomb=random.randint(0,self.bomb_interval)
        self.health=2
        wh=img.get_size()
        self.xi=wh[0]//2
        self.yi=wh[1]//2
        self.mask=game.bomber_mask
        self.value=5

    def bomb(self):
        self.t_bomb+=game.delta_t
        if (self.t_bomb > self.bomb_interval):
            self.t_bomb = 0
            game.blasts.append(Bomb(img=self.bombimg, wnd=self.wnd, wy=self.wy, x=self.x, y=self.y, spdxy=self.spdxy))

    def alive(self):
        self.bomb()
        return self.x > -100 and self.health > 0