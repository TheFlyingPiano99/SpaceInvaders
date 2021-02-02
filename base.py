import pygame, sys
from pygame.locals import *
import os

import config

pygame.init()

font = pygame.font.Font(None, 42)

class Base:
    def __init__(self, title, width, height, framerate, fullscreen):
        if not fullscreen:
            self.window = pygame.display.set_mode((width, height))
        else:
            self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            config.SCREEN_WIDTH, config.SCREEN_HEIGHT = self.window.get_size()
            
        pygame.display.set_caption(title)

        self.clock = pygame.time.Clock()
        self.framerate = framerate

    def logic(self, keys, newkeys, buttons, newbuttons, mousepos, lastmousepos, delta):
        raise NotImplementedError()

    def paint(self, surface):
        raise NotImplementedError()

    def loadFolders(self, images=False, sounds=False, music=False):
        if images:
            self.images = {str(i)[:-4]:pygame.image.load("images/"+i).convert_alpha() for i in os.listdir("images") if os.path.isfile("images/"+i) if i[0] != "."}
        if sounds:
            self.sounds = {str(i)[:-4]:pygame.mixer.Sound("sounds/"+i) for i in os.listdir("sounds") if os.path.isfile("sounds/"+i)}
        if music:
            self.music = {str(i)[:-4]:"music/"+i for i in os.listdir("music") if os.path.isfile("music/"+i)}

    def main(self):
        keys = set()
        buttons = set()
        mousepos = (1, 1)

        while True:
            self.clock.tick(self.framerate)
            delta = float(self.clock.get_time()) / float(self.framerate)

            newkeys = set()
            newbuttons = set()
            lastmousepos = mousepos

            for event in pygame.event.get():

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    return

                if event.type == MOUSEBUTTONDOWN:
                    buttons.add(event.button)
                    newbuttons.add(event.button)
                    mousepos = event.pos
                if event.type == MOUSEBUTTONUP:
                    buttons.discard(event.button)
                    mousepos = event.pos

                if event.type == MOUSEMOTION:
                    mousepos = event.pos

                if event.type == KEYDOWN:
                    keys.add(event.key)
                    newkeys.add(event.key)

                if event.type == KEYUP:
                    keys.discard(event.key)

            self.logic(keys, newkeys, buttons, newbuttons, mousepos, lastmousepos, delta)
            self.paint(self.window)
            self.window.blit(font.render("FPS: %i" % self.clock.get_fps(), True, (255, 255, 255)), (0, 0))

            pygame.display.update()
