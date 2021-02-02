import libs.game as game

class Blast:
    """
    dimenziok: w=10, h=50
    """
    def __init__(self, img, wnd, snd, wy, x, y, spdxy):
        self.x=x
        self.y=y
        self.wy=wy
        self.image=img
        self.window=wnd
        self.sound=snd
        self.spd=[spdxy[0]*0.5, spdxy[1]*0.5-2]
        wh=img.get_size()
        self.xi=wh[0]//2
        self.yi=wh[1]//2


    def rajz(self):
        self.window.blit(self.image,dest=(self.x-self.xi+game.offset[0],self.y-self.yi+game.offset[1]))
        self.move()

    def move(self):
        self.x+=self.spd[0]*game.delta_t
        self.y+=self.spd[1]*game.delta_t
        self.hit()

    def alive(self):
        return self.y > -50

    def hit(self):
        for inv in game.invaders:
            if inv.collision(self.x,self.y,self.xi,self.yi,mask=game.blast_mask):
                if self.sound:
                    self.sound.play()
                    inv.health_val(-1)
                    game.blasts.remove(self)
                break


    """
    dimenziok: w=40, h=40
    """
class Bomb(Blast):
    def __init__(self, img, wnd, wy, x, y, spdxy):
        Blast.__init__(self,img,wnd,None,wy,x,y,spdxy)
        self.spd=[spdxy[0] * 0.8, spdxy[1]+0.2]
        wh=img.get_size()
        self.xi=wh[0]//2
        self.yi=wh[1]//2

    def alive(self):
        return self.y < self.wy

    def hit(self):
        if game.ship.collision(self.x, self.y, self.xi, self.yi,mask=game.bomb_mask):
            if self.sound:
                self.sound.play()
            game.blasts.remove(self)
            game.ship.health_val(-1)



