import libs.game as game
import random


class Health:
    #dimenziok:
    #   w,h = 40, 40
    def __init__(self,wnd,img,snd,wx,wy,spd):
        self.x=random.randint(0+50,wx-50)
        self.wy=wy
        self.y=-20
        self.spd=spd
        self.window=wnd
        self.image=img
        self.sound=snd
        wh=img.get_size()
        self.xi=wh[0]//2
        self.yi=wh[1]//2

    def move(self):
        self.y+=self.spd*game.delta_t
        self.hit()

    def rajz(self):
        self.window.blit(self.image,dest=(self.x-self.xi+game.offset[0],self.y-self.yi+game.offset[1]))
        self.move()

    def alive(self):
        return self.y < self.wy

    def hit(self):
        if game.ship.collision(self.x, self.y, self.xi, self.yi,mask=game.hp_mask):
            if self.sound:
                self.sound.play()
            game.items.remove(self)
            game.ship.health_val(+1)
            game.musicgen.change_chord(form='triad')
            game.musicgen.play_chord_block()