import pygame as pg
from pygame.locals import *
from vector import Vector
from settings import *

class Player(object):
    def __init__(self):
        # self.name = PLAYER
        self.pos = Vector(200,400)
        self.direction = STOP
        self.directions = {STOP:Vector(), UP:Vector(0, -1), DOWN:Vector(0,1),
                            LEFT:Vector(-1,0), RIGHT:Vector(1,0)}
        self.speed = 80
        self.radius = 10
        self.color = YELLOW

    def update(self, input):
        self.pos += self.directions[self.direction]*self.speed*input
        self.direction = self.getKey()

    def getKey(self):
        pressed = pg.key.get_pressed()
        if pressed[K_UP]:
            return UP
        if pressed[K_DOWN]:
            return DOWN
        if pressed[K_LEFT]:
            return LEFT
        if pressed[K_RIGHT]:
            return RIGHT
        return STOP
        
    def draw(self, screen):
        pos = self.pos.asInt()
        pg.draw.circle(screen, self.color, pos, self.radius) # once we get the game working, replace this with jack o lanturn art
