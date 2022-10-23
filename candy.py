from random import randrange
import pygame as pg
from pygame.sprite import Sprite
from vector import Vector
from settings import *
import numpy as np

class Candy(Sprite):
    def __init__(self, row, column):
        self.color = list(np.random.choice(range(256), size=3)) #(randrange(216,243),randrange(216,243),randrange(216,243)) # will generate a random color for pellets
        self.name = SMALL_CANDY
        self.position = Vector(column * BLOCK_WIDTH, row * BLOCK_HEIGHT)
        self.radius = int(4 * BLOCK_WIDTH / 16)
        self.collide_radius = int(4* BLOCK_WIDTH / 16)
        self.visible = True
        self.points = 5

    def draw(self, screen):
        if self.visible:
            pos = self.position.asInt()
            pg.draw.circle(screen, self.color, pos, self.radius)

class Candy_Bar(Candy):
    def __init__(self, row, column):
        Candy.__init__(self, row, column)
        self.name = CANDY_BAR
        self.radius = int(8 * BLOCK_WIDTH / 16)
        self.points = 100
        self.flashing_timer = 0.2
        self.timer = 0

    def update(self, time):
        self.timer += time
        if self.timer >= self.flashing_timer:
            self.visible = not self.visible
            self.timer = 0

class CandyGroup(object):
    def __init__(self, candyfile):
        self.candyList = []
        self.candyBars = []
        self.createCandyList(candyfile)
        self.amount_eaten = 0

    def update(self, amount):
        for candy in self.candyBars:
            candy.update(amount)

    def createCandyList(self, candyfile):
        data = self.readFile(candyfile)
        for row in range(data.shape[0]):
            for column in range(data.shape[1]):
                if data[row][column] in ['.', '+']:
                    self.candyList.append(Candy(row, column))
                elif data[row][column] in ['p']:
                    candy_bar = Candy_Bar(row, column)
                    self.candyList.append(candy_bar)
                    self.candyBars.append(candy_bar)

    def readFile(self, textfile):
        return np.loadtxt(textfile, dtype= '<U1')

    def Empty(self):
        if len(self.candyList) == 0:
            return True
        else:
            return False

    def draw(self, screen):
        for candy in self.candyList:
            candy.draw(screen)