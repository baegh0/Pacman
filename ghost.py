from random import randint
import pygame as pg
from pygame.sprite import Sprite, Group
from settings import *
from vector import Vector
from timer import Timer

# manages each individual ghost
class Ghost(Sprite):
    # Chase/Regular modes:
    angel_ghost = [pg.image.load(f'images/angel ghost-{n}.png') for n in range(2)]
    butterfly_ghost = [pg.image.load(f'images/butterfly ghost-{n}.png') for n in range(2)]
    devil_ghost = [pg.image.load(f'images/devil ghost-{n}.png') for n in range(2)]
    witch_ghost = [pg.image.load(f'images/witch ghost-{n}.png') for n in range(2)]
    # Scatter Modes:

    # Run Modes: 

    # Dictionaries that determine which mode and which frames to play
    chase_dict = {0: angel_ghost, 1: butterfly_ghost, 2: devil_ghost, 3: witch_ghost}
    scatter_dict = {}
    run_dict = {}

    def __init__(self, node):
        self.name = None
        self.directions = {STOP:Vector(), UP:Vector(0, -1), DOWN:Vector(0,1),
                            LEFT:Vector(-1,0), RIGHT:Vector(1,0)}
        self.direction = STOP
        self.setSpeed(100)
        self.radius = 10
        self.collideRadius = 5
        self.color = WHITE
        self.node = node
        self.setPos()
        self.target = node
        self.visible = True
        self.disablePortal = False

    def setPos(self):
        self.position = self.node.position.copy()

    def checkDirection(self, direction):
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        else:
            return False

    def nextNode(self, direction):
        if self.checkDirection(direction):
            return self.node.neighbor[direction]
        return self.node

    def overshootStop(self):
        if self.target is not None:
            vector1 = self.target.position - self.node.position
            vector2 = self.pos - self.node.position
            node2Target = vector1.magnitudeSquared()
            node2Self = vector2.magnitudeSquared()
            return node2Self >= node2Target
        else:
            return False

    def reverse(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    def opposite(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        else:
            return False

    def setSpeed(self, speed):
        self.speed = speed * BLOCK_WIDTH / 10
    
    def draw(self, screen):
        if self.visible:
            ghost_pos = self.position.asInt()
            pg.draw.circle(screen, self.color, ghost_pos, self.radius)

    def availableDirections(self):
        directions = []
        for button in [UP, DOWN, LEFT, RIGHT]:
            if self.checkDirection(button):
                if button != self.direction * -1:
                    directions.append(button)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

    def Random(self, directions):
        return directions[randint(0, len(directions)-1)]
        
    def update(self, x):
        self.position += self.directions[self.direction]*self.speed*x
        if self.overshootStop():
            self.node = self.target
            directions = self.checkDirection()
            direction = self.Random(directions)
            if not self.disablePortal:
                if self.node.neighbor[PORTAL] is not None:
                    self.node = self.node.neighbor[PORTAL]
            self.target = self.nextNode(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.nextNode(self.direction)
            self.setPos()