from random import randrange
import pygame as pg
from pygame.sprite import Sprite
from vector import Vector
from settings import *
from random import randrange
from node import Nodes

class Candy(Sprite):
    def __init__(self, row, column):
        self.color = [randrange(256) for _ in range(3)] # will generate a random color for pellets
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
        self.image = pg.image.load('images/chocolate_bars-0.png')
        self.points = 100
        self.flashing_timer = 0.2
        self.timer = 0
        self.position = Vector(column * BLOCK_WIDTH -30, row * BLOCK_HEIGHT - 30)

    def update(self, time):
        self.timer += time
        if self.timer >= self.flashing_timer:
            self.visible = not self.visible
            self.timer = 0

    def draw(self, screen):
        if self.visible:
            pos = self.position.asInt()
            screen.blit(self.image, pos)

class CandyGroup(object):
    def __init__(self):
        self.data = Nodes('maze.txt').mazeData
        self.candyList = []
        self.candyBars = []
        self.createCandyList()
        self.amount_eaten = 0

    def update(self, amount):
        for candy in self.candyBars:
            candy.update(amount)
    
    def createCandyList(self):
        for row in range(len(self.data)):
            for col in range(len(self.data[row])):
                if self.data[row][col] in ['.', '+']:
                    self.candyList.append(Candy(row, col))
                elif self.data[row][col] in ['p']:
                    candy_bar = Candy_Bar(row, col)
                    self.candyList.append(candy_bar)
                    self.candyBars.append(candy_bar)

    def Empty(self):
        return len(self.candyList) == 0

    def draw(self, screen):
        for candy in self.candyList:
            candy.draw(screen)