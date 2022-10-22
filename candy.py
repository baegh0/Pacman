from random import randrange
import pygame as pg
from pygame.sprite import Sprite
from vector import Vector
from settings import *
import numpy as np

class Candy(object):
    def __init__(self, row, column):
        self.color = (randrange(216,243),randrange(216,243),randrange(216,243))
        self.name = SMALL_CANDY
        self.position = Vector(column * BLOCK_WIDTH, row * BLOCK_HEIGHT)
        self.radius = int(4 * BLOCK_WIDTH / 16)
        self.collide_radius = int(4* BLOCK_WIDTH / 16)
        self.visible = True
        self.points = 5

    def draw(self, screen):
        if self.visible:
            pos = self.position.asInt()
            pg.draw.circle(screen, self.collide_radius, pos, self.radius)