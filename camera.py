import config

class Camera:
    def __init__(self):
        self.pos = [0, 0]
        self.zoom = 1

    def setPos(self, pos):
        self.pos = list(pos)

    def adjustPos(self, x, y):
        self.pos[0] += x
        self.pos[1] += y

    def adjustZoom(self, amt):
        self.zoom = max(self.zoom + amt, 0)

    def wts(self, pos):
        # wts = world to screen
        return (pos[0] + self.pos[0], pos[1] + self.pos[1])

    def wtsRect(self, rect):
        return [rect[0] + self.pos[0], rect[1] + self.pos[1], rect[2], rect[3]]

    def stw(self, pos):
        # stw = screen to world
        return (pos[0] - self.pos[0], pos[1] - self.pos[1])

    def stwRect(self, rect):
        return [rect[0] - self.pos[0], rect[1] - self.pos[1], rect[2], rect[3]]

GAMECAM = Camera()