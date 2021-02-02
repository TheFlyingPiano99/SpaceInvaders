import libs.game as game
import pygame
import random

class Star:
    def __init__(self,wnd,img,wx,wy,setup=False):
        self.wx=wx
        self.wy=wy
        self.window=wnd
        self.image=img
        wh=img.get_size()
        self.xi=wh[0]//2
        self.yi=wh[1]//2
        self.alpha_surface = pygame.Surface((wh[0], wh[1])).convert()
        self.opacity = random.randint(25,200)
        self.x = random.randrange(10, self.wx - 10)
        if setup:
            self.y= random.randrange(10, self.wy - 10)
        else:
            self.y = -10
        self.spd=0.02

    def blit_alpha(self):
        self.alpha_surface.blit(self.window, (-self.x+game.offset[0]*0.5, -self.y+game.offset[1]*0.5))
        self.alpha_surface.blit(self.image, (0, 0))
        self.alpha_surface.set_alpha(self.opacity)
        self.window.blit(self.alpha_surface, dest=(self.x - self.xi+game.offset[0]*0.5, self.y-self.yi+game.offset[1]*0.5))

    def rajz(self):

        self.blit_alpha()
        self.y+=self.spd*game.delta_t

    def alive(self):
        return self.y < self.wy+10
