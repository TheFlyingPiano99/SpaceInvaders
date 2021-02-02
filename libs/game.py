from base import *
from libs.blasts import Blast
from libs.invaders import Invader, Bomber
from libs.misc import Star
from libs.ship import Ship
import libs.effects as effects
import random
from libs.items import Health
from libs.music import Generate_music
import os.path
import datetime

delta_t = 0
t_bomb = 0
invaders = []
blasts = []
score = 0
gameover = False
ship=None
enginesnd=None
offset=[0,0]
shake=False
hitsnd=None
trailimg=None
trustsnd=None
items=[]
trustimg=None
musicsnd=None
musicgen=None
ship_mask=None
invader_mask=None
bomber_mask=None
hp_mask=None
blast_mask=None
bomb_mask=None


def getsortkey(x):
    return int(x[0])

class Game(Base):
    def __init__(self):
        global delta_t
        global invaders
        global blasts
        global score
        global gameover
        global ship
        global enginesnd
        global hitsnd
        global trailimg
        global offset
        global shake
        global trustsnd
        global items
        global trustimg
        global musicsnd
        global musicgen
        global ship_mask
        global invader_mask
        global hp_mask
        global blast_mask
        global bomb_mask
        global bomber_mask

        Base.__init__(self, config.SCREEN_TITLE, config.SCREEN_WIDTH, config.SCREEN_HEIGHT, config.FRAMERATE,
                      config.SCREEN_FULLSCREEN)
        self.loadFolders(images=True)
        self.loadFolders(sounds=True)
        print(self.images)
        print(self.sounds)
        self.delta = 0
        self.delta_prev=0
        self.t_shoot = 0
        self.t_inv = 0
        self.t_bomber=0
        self.t_item=0
        self.spd_item=0.4
        self.wx,self.wy = pygame.display.get_surface().get_size()
        self.starimages=[self.images['star01'],self.images['star02'],self.images['star03'],self.images['star04']]
        self.blastimg=self.images['blast']
        self.invaderimg=self.images['invader']
        self.bomberimg=self.images['bomber']
        self.startsnd=self.sounds['start']
        self.explosionsnd=self.sounds['explosion']
        self.lasersnd=self.sounds['laser']
        self.bombimg=self.images['bomb']
        self.hpimg=self.images['hp']
        self.reflection=self.images['ship_reflection']
        self.shipimg=self.images['ship']

        ship_mask=pygame.mask.from_surface(self.shipimg)
        invader_mask=pygame.mask.from_surface(self.invaderimg)
        hp_mask=pygame.mask.from_surface(self.hpimg)
        blast_mask = pygame.mask.from_surface(self.blastimg)
        bomb_mask = pygame.mask.from_surface(self.bombimg)
        bomber_mask =pygame.mask.from_surface(self.bomberimg)

        trustimg = self.images['trust']
        trailimg = self.images['trail']
        enginesnd = self.sounds['spaceshipengine']
        hitsnd = self.sounds['takenhit']
        trustsnd = self.sounds['truster']
        musicsnd = [self.sounds['01'],self.sounds['02'],self.sounds['03'],self.sounds['04'],self.sounds['05'],self.sounds['06'],self.sounds['07'],self.sounds['08'],self.sounds['09'],self.sounds['10'],self.sounds['11'],self.sounds['12'],self.sounds['13'],self.sounds['14'],self.sounds['15'],self.sounds['16'],self.sounds['17'],self.sounds['18'],self.sounds['19'],self.sounds['20'],self.sounds['21'],self.sounds['22'],self.sounds['23'],self.sounds['24'],self.sounds['25']]
        musicgen = Generate_music()
        self.score_fn = 'scores.txt'
        self.stars = []
        self.reflect = False
        self.speed = 1
        self.pause = False
        for i in range(100):
            self.star(setup = True)
        ship = Ship(img = self.images['ship'], wnd=self.window,wx=self.wx,wy=self.wy)
        self.startsnd.play()

    def score_read(self):
        global score
        lines=[]
        if os.path.isfile(self.score_fn):
            with open(self.score_fn) as f:
                for t in f.read().split('\n'):
                    if t != '':
                        lines.append(t)
        return lines

    def score_write(self):
        global score
        if score < 1:
            return
        lines=self.score_read()
        t=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines.append(str(score)+'|'+t)
        for i in range(len(lines)):
            lines[i] = lines[i].split('|')

        lines = sorted(lines, key = getsortkey, reverse = True)
        with open(self.score_fn,mode = 'w') as f:
            i = 0
            for t in lines:
                f.write(str(t[0])+'|'+str(t[1])+'\n')
                i += 1
                if i >= 10:
                    break


    def display_scores(self):
        textwidth=None
        lines=self.score_read()
        i = 1
        txt = 'Rank'
        textwidth = font.size(txt)
        self.window.blit(font.render(txt, True, (255, 255, 255)),
                         ((self.wx // 2) - textwidth[0] - 50, self.wy // 2 + i * 40))
        txt = 'Score'
        textwidth = font.size(txt)
        self.window.blit(font.render(txt, True, (255, 255, 255)),
                         ((self.wx // 2) - textwidth[0] + 50, self.wy // 2 + i * 40))
        txt = 'Date and Time'
        self.window.blit(font.render(txt, True, (255, 255, 255)), ((self.wx // 2) + 100, self.wy // 2 + i * 40))

        for l in lines:
            l=l.split('|')
            txt = '%d.' % i
            textwidth = font.size(txt)
            self.window.blit(font.render(txt, True, (255, 255, 255)), ((self.wx // 2) -textwidth[0]-50, self.wy //2 + i*40+50))
            txt = l[0]
            textwidth = font.size(txt)
            self.window.blit(font.render(txt, True, (255, 255, 255)), ((self.wx // 2) -textwidth[0]+50, self.wy //2 + i*40+50))
            txt = l[1]
            self.window.blit(font.render(txt, True, (255, 255, 255)), ((self.wx // 2) +100, self.wy //2 + i*40+50))
            i+=1
            if i > 10:
                break

    def logic(self, keys, newkeys, buttons, newbuttons, mousepos, lastmousepos, delta):
        global score
        global gameover
        global delta_t
        global ship
        global enginesnd
        dir=['','']
        if K_ESCAPE in keys:
            print('Score = ',score)
            self.score_write()
            pygame.event.post(pygame.event.Event(QUIT))

        if K_a in keys or K_LEFT in keys:
            dir[0]='L'
        elif K_d in keys or K_RIGHT in keys:
            dir[0]='R'

        if K_w in keys or K_UP in keys:
            dir[1]='U'
        elif K_s in keys or K_DOWN in keys:
            dir[1]='D'

        if K_SPACE in keys:
            self.shoot(ship.getxy())

        if K_KP_PLUS in keys:
            self.speed+=0.05
        if K_KP_MINUS in keys:
            self.speed-=0.05
        if K_KP0 in keys:
            self.speed=1
        ship.input_move(dir=dir)
        if self.speed > 1.5:
            self.speed=1.5
        elif self.speed < 0.5:
            self.speed=0.5

        if self.pause and K_r in keys:
            if gameover:
                print('Score = ', score)
                self.score_write()
                score=0
                blasts.clear()
                invaders.clear()
                items.clear()
                ship = Ship(img=self.shipimg, wnd=self.window, wx=self.wx, wy=self.wy)
                self.startsnd.play()
                gameover=False
            self.pause=False
            pygame.mixer.unpause()



        #-----------------------------------------------------------
        if ship.health_val()<=0:
            gameover=True

        if gameover or K_p in keys:
            self.pause=True
            pygame.mixer.pause()
            if gameover:
                pygame.mixer.stop()

        #------------time---------------------------------------
        delta_t = (self.delta - self.delta_prev)*self.speed
        self.delta_prev=self.delta
        if self.pause:
            delta_t=0
        #-------------events-------------------------------------

        self.invade()
        self.make_item()
        if self.t_shoot > 50:
            self.reflect = False


        #-------------------timers------------------------------
        self.t_shoot += delta_t
        self.t_inv += delta_t
        self.t_bomber += delta_t
        self.t_item+= delta_t

    def kiir(self,txt=''):
        textwidth = font.size(txt)
        self.window.blit(font.render(txt, True, (255, 255, 255)),
                         ((self.wx // 2) - (textwidth[0] // 2), self.wy // 2 - (textwidth[1] // 2)))

    def shoot(self, xy):
        if self.t_shoot > 200:
            self.t_shoot = 0
            self.reflect=True
            self.lasersnd.play()
            blasts.append(Blast(img=self.blastimg, wnd=self.window, snd=self.explosionsnd,
                                wy=self.wy, x=xy[0], y=xy[1]-75-25, spdxy=ship.getspd()))
    def invade(self):
        global invaders
        if self.t_inv >1000:
            self.t_inv=0
            invaders.append(Invader(img=self.invaderimg, wnd=self.window, wx=self.wx, wy=self.wy))

        if self.t_bomber > random.randint(5000,8000):
            self.t_bomber=0
            invaders.append(Bomber(img=self.bomberimg, bombimg=self.bombimg, wnd=self.window, wx=self.wx, wy=self.wy))
    def make_item(self):
        global items

        if self.t_item > 5000:
            self.t_item=0
            items.append(Health(wnd=self.window,img=self.hpimg,snd=self.startsnd,wx=self.wx,wy=self.wy,spd=self.spd_item))

    def star(self,setup=False):
        self.stars.append(Star(wnd=self.window,img=self.starimages[random.randint(0,len(self.starimages)-1)],wx=self.wx,wy=self.wy,setup=setup))



    def paint(self, surface):
        global shake
        global offset
        self.surface=surface
        surface.fill((10,10,10))
        self.delta += self.clock.get_time()
        if shake:
            offset,shake=effects.shake_screen()
        self.rajz()

    def rajz(self):
        global ship
        global score
        global items
        for obj in self.stars:
            if obj.alive():
                obj.rajz()
            else:
                self.stars.remove(obj)
                self.star()

        for obj in items:
            if obj.alive():
                obj.rajz()
            else:
                items.remove(obj)
        for obj in blasts:
            if obj.alive():
                obj.rajz()
            else:
                blasts.remove(obj)
        ship.rajz(reflect=self.reflect,reflimg=self.reflection)
        for obj in invaders:
            if obj.health_val() < 1:
                score += obj.getvalue()
                musicgen.play_single()
            if obj.alive():
                obj.rajz()

            else:
                invaders.remove(obj)

        if self.pause:
            effects.dimm(wnd=self.window,wx=self.wx,wy=self.wy)
            self.display_scores()
        if gameover :
            self.kiir('Gameover! Score earned: %i Press r, to replay!' % score)
        elif self.pause:
            self.kiir('Paused Press r, to resume!')


        self.window.blit(font.render("Score: %i" % score, True, (255, 255, 255)), (self.wx-200, 0))
        self.window.blit(font.render("Health: %i" % ship.health_val(), True, (255, 255, 255)), (self.wx-200, 50))
        self.health_bar()

    def health_bar(self):
        global ship
        for i in range(ship.health_val()):
            pygame.draw.rect(self.window, (255,255,255),(self.wx-200+i*35,80,30,30), 0)