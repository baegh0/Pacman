import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from timer import Timer

class Pacman(Entity):
    pumpkin_images = [pygame.image.load(f'images/pumpkinman0.png'), pygame.image.load(f'images/pumpkinman1.png')]
    flip_pumpkin_images = [pygame.transform.flip(pygame.image.load(f'images/pumpkinman{n}.png'), True, False) for n in range(2)]

    def __init__(self, node):
        Entity.__init__(self, node )
        self.name = PACMAN    
        self.color = YELLOW
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.lives = 3
        self.alive = True
        self.image = pygame.image.load('images/pumpkinman0.png')
        self.timer = Timer(image_list = self.pumpkin_images, delay=200)
        self.timer_flip = Timer(image_list=self.flip_pumpkin_images, delay=200)

    def draw(self, screen):
        image = self.timer_flip.image() if self.direction == RIGHT else self.timer.image()
        adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
        p = self.position - adjust
        screen.blit(image, p.asTuple())

    def reset(self):
        Entity.reset(self)
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True

    def die(self):
        self.alive = False
        self.direction = STOP

    def update(self, dt, screen):	
        self.position += self.directions[self.direction]*self.speed*dt
        direction = self.getValidKey()
        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else: 
            if self.oppositeDirection(direction):
                self.reverseDirection()
        self.draw(screen)

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP  

    def eatPellets(self, pelletList):
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None    
    
    def collideGhost(self, ghost):
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius)**2
        return dSquared <= rSquared