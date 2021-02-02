import libs.game as game
import math
import libs.effects as effects
import random
import pygame

class Ship:
    """
    dimenziok: w=180,y=150
    """
    def __init__(self, img, wnd,wx,wy):

        self.x,self.y = wx,wy
        self.maxx=wx
        self.maxy=wy
        self.x/=2
        self.y-=75
        self.image=img
        self.window=wnd
        self.spdh=0
        self.spdv=0
        self.max_spd=2
        self.accel=0.002
        self.prev_dir=['','']
        self.health=5
        self.trail=[]
        self.safemode=False
        self.t_safemode=0
        self.refl=0
        wh=img.get_size()
        self.xi=wh[0]//2
        self.yi=wh[1]//2

        game.enginesnd.play(loops=-1)
        game.enginesnd.set_volume(0)
        game.trustsnd.play(-1)
        game.trustsnd.set_volume(0.5)
        self.pre_trail=effects.onsetup_trail(wnd=self.window,img=game.trailimg)



    def input_move(self,dir):
        #--------------------------------------------
        if dir[0] in ('R','L'):
            if dir[0]=='R' and self.x <= self.maxx-90:
                if self.prev_dir[0] !='R':
                    self.spdh+=0.2
                elif self.spdh <=self.max_spd:
                    self.spdh+= game.delta_t * self.accel
                self.prev_dir[0]='R'
            elif dir[0]=='L' and self.x >= 90:
                if self.prev_dir[0] != 'L':
                    self.spdh+= -0.2
                elif self.spdh >= -self.max_spd:
                    self.spdh-= game.delta_t * self.accel
                self.prev_dir[0]='L'
        #--------------------------------------------
        if dir[1] in ('U','D'):
            if dir[1] == 'U' and self.y >= 90:
                if self.prev_dir[1] != 'U':
                    self.spdv+= -0.2
                elif self.spdv >= -self.max_spd:
                    self.spdv-= game.delta_t * self.accel
                self.prev_dir[1]='U'
            elif dir[1] == 'D' and self.y <= self.maxy - 90:
                if self.prev_dir[1] != 'D':
                    self.spdv += 0.2
                elif self.spdv <= self.max_spd:
                    self.spdv += game.delta_t * self.accel
                self.prev_dir[1]='D'
        #--------------------------------------------

        if not dir[0] in ('L','R') and self.x >= 90 and self.x <= self.maxx-90:
            if self.prev_dir[0] != 'L' and self.spdh > 0:
                self.spdh -= game.delta_t * self.accel * 0.5
            elif self.prev_dir[0] != 'R' and self.spdh < 0:
                self.spdh += game.delta_t * self.accel * 0.5
            self.prev_dir[0]=''

        if not dir[1] in ('U','D') and self.y >= 90 and self.y <= self.maxy-90:
            if self.prev_dir[1] != 'U' and self.spdv > 0:
                self.spdv -= game.delta_t * self.accel * 0.5
            elif self.prev_dir[1] != 'D' and self.spdv < 0:
                self.spdv += game.delta_t * self.accel * 0.5
            self.prev_dir[1]=''


        self.x += self.spdh * game.delta_t
        self.y += self.spdv * game.delta_t
        if self.x < 90:
            self.x=90
            self.spdh=0
        elif self.x > self.maxx-90:
            self.x=self.maxx-90
            self.spdh=0

        if self.y < 90:
            self.y=90
            self.spdv=0
        elif self.y > self.maxy-90:
            self.y=self.maxy-90
            self.spdv=0
        self.make_trail()
        self.engine_volume()


    def collision(self,x,y,xi,yi,mask):
        if ((abs(x - self.x) <=(self.xi+xi)) and (abs(y-self.y) <= (self.yi+yi))):
            offs = [int((x - xi)-(self.x - self.xi) ), int((y - yi)-(self.y - self.yi))]
            return game.ship_mask.overlap(mask, offs)
        else:
            return False

    def getxy(self):
        return self.x, self.y

    def getspd(self):
        return self.spdh, self.spdv

    def relative_speed(self):
        v=math.sqrt(self.spdh**2 + self.spdv**2)/math.sqrt(8)
        v*=v
        if v > 1:
            v=1
        return v

    def rajz(self,reflect,reflimg):
        self.window.blit(self.image,dest=(self.x-self.xi+game.offset[0],self.y-self.yi+game.offset[1]))
        if reflect:
            self.window.blit(reflimg, dest=(self.x - self.xi + game.offset[0], self.y - self.yi + game.offset[1]))
        if game.delta_t > 0:
            self.refl=random.randint(0,1)
        if self.refl==1:
            self.window.blit(game.trustimg, dest=(self.x - self.xi + game.offset[0], self.y - self.yi-9+22 + game.offset[1]))

        for tr in self.trail:
            tr.rajz()
        if self.safemode:
            self.t_safemode+=game.delta_t
            if self.t_safemode > 500:
                self.safemode=False
                self.t_safemode=0

    def health_val(self,val=0):
        if self.safemode and val < 0:
            val=0
        self.health+=val
        if self.health > 5:
            self.health = 5
        if val < 0:
            self.safemode = True
            game.hitsnd.play()
            game.shake=True
            game.musicgen.change_key()
            game.musicgen.change_chord(form='disson')
            game.musicgen.play_chord_block()
        return self.health

    #A meghivo(akivel utkozik a ship) x,y pozicioja:
    def knock_back(self,x,y,spdx,spdy):
        a=0.3
        if x>self.x:
            self.spdh=-abs(spdx*0.5)-a
        elif x < self.x:
            self.spdh=+abs(spdx*0.5)+a
        if y>self.y:
            self.spdv=-abs(spdy*0.5)-a
        elif y<self.y:
            self.spdv=+abs(spdy*0.5)+a



    def engine_volume(self):
        game.enginesnd.set_volume(self.relative_speed())

    def make_trail(self):
        if game.delta_t >5:
            self.trail.append(effects.Trail(wnd=self.window,xy=self.getxy(),spdxy=self.getspd(),pre_trail=self.pre_trail))
        if len(self.trail) > 30:
            self.trail.remove(self.trail[0])