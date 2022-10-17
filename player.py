import pygame as pg
from pygame.locals import *
from vector import Vector
from settings import *

class Player(object):
    def __init__(self, node):
        self.name = 'PLAYER'
        # self.pos = Vector(200,400) #was used to spawn test player
        self.direction = STOP
        self.directions = {STOP:Vector(), UP:Vector(0, -1), DOWN:Vector(0,1),
                            LEFT:Vector(-1,0), RIGHT:Vector(1,0)}
        self.speed = 80
        self.radius = 10
        self.color = YELLOW
        self.node = node
        self.setStart()
        self.target = node

    def setStart(self):
        self.pos = self.node.position.copy()

    def update(self, input):
        self.pos += self.directions[self.direction]*self.speed*input
        direction = self.getKey()
        # self.direction = direction
        # self.node = self.nextNode(direction)
        # self.setStart()
        if self.overshootStop():
            self.node = self.target
            self.target = self.nextNode(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.direction = STOP
            self.setStart()

    def checkDirection(self, direction):
        if direction is not STOP:
            if self.node.neighbor[direction] is not None:
                return True
        return False

    def nextNode(self, direction):
        if self.checkDirection(direction):
            return self.node.neighbor[direction]
        return self.node


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

    def overshootStop(self):
        if self.target is not None:
            vector1 = self.target.position - self.node.position
            vector2 = self.pos - self.node.position
            node2Target = vector1.magnitudeSquared()
            node2Self = vector2.magnitudeSquared()
            return node2Self >= node2Target
        else:
            return False