import pygame as pg
from pygame.sprite import Sprite


class Candy(Sprite):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = self.game.surface

        self.rect.left = 259
        self.rect.top = 363
        self.x = float(self.rect.x)

        self.image = pg.image.load('images/chocolate_bars-0.png')
        self.rect = self.image.get_rect()


    def width(self): return self.rect.width

    def height(self): return self.rect.height

    def check_edges(self):
        r = self.rect
        s_r = self.screen.get_rect()
        return r.right >= s_r.right or r.left <= 0

    def draw(self): self.screen.blit(self.image, self.rect)

    def update(self):
        self.draw()
