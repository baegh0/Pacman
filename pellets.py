import pygame
from vector import Vector2
from random import randint
from constants import *
from nodes import NodeGroup

class Pellet(object):
    def __init__(self, row, column):
        self.name = PELLET
        self.position = Vector2(column*TILEWIDTH, row*TILEHEIGHT)
        self.color = list(randint(0, 255) for _ in range(3)) # will generate a random color for pellets
        self.radius = int(2 * TILEWIDTH / 16)
        self.collideRadius = int(2 * TILEWIDTH / 16)
        self.points = 10
        self.visible = True
        
    def render(self, screen):
        if self.visible:
            adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
            p = self.position + adjust
            pygame.draw.circle(screen, self.color, p.asInt(), self.radius)



class PowerPellet(Pellet):
    def __init__(self, row, column):
        Pellet.__init__(self, row, column)
        self.name = POWERPELLET
        self.image = pygame.image.load('images/chocolate_bars-0.png')
        self.points = 100
        self.flashTime = 0.2
        self.timer= 0
        self.collideRadius = int(13 * TILEWIDTH / 16)
        self.position = Vector2(column * TILEWIDTH - 15, row * TILEHEIGHT - 15)
        
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.flashTime:
            self.visible = not self.visible
            self.timer = 0
    
    def render(self, screen):
        if self.visible:
            pos = self.position.asInt()
            screen.blit(self.image, pos)

class PelletGroup(object):
    def __init__(self):
        self.pelletList = []
        self.powerpellets = []
        self.pelletFile = self.readPelletfile()
        self.createPelletList()
        self.numEaten = 0

    def update(self, dt):
        for powerpellet in self.powerpellets:
            powerpellet.update(dt)
                
    def createPelletList(self):     
        for row in range(len(self.pelletFile)):
            for col in range(len(self.pelletFile[row])):
                if self.pelletFile[row][col] in ['.', '+']:
                    self.pelletList.append(Pellet(row, col))
                elif self.pelletFile[row][col] in ['P', 'p']:
                    pp = PowerPellet(row, col)
                    self.pelletList.append(pp)
                    self.powerpellets.append(pp)
                    
    def readPelletfile(self):
        return NodeGroup().mazeData
    
    def isEmpty(self):
        if len(self.pelletList) == 0:
            return True
        return False
    
    def render(self, screen):
        for pellet in self.pelletList:
            pellet.render(screen)

