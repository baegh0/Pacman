import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from modes import ModeController
from timer import Timer

class Ghost(Entity):
    def __init__(self, node, pacman=None, blinky=None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        self.image = None
        self.directionMethod = self.goalDirection
        self.pacman = pacman
        self.mode = ModeController(self)
        self.blinky = blinky
        self.homeNode = node

    def reset(self):
        Entity.reset(self)
        self.points = 200
        self.directionMethod = self.goalDirection

    def update(self, dt):
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def draw(self, screen):
        img_list = self.invert_image_list if self.mode.current == FREIGHT else self.image_list
        self.timer = Timer(image_list=img_list, delay=150)
        image = self.timer.image()
        adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
        p = self.position - adjust
        screen.blit(image, p.asTuple())

    def scatter(self):
        self.goal = Vector2()

    def chase(self):
        self.goal = self.pacman.position

    def spawn(self):
        self.goal = self.spawnNode.position

    def setSpawnNode(self, node):
        self.spawnNode = node

    def startSpawn(self):
        self.mode.setSpawnMode()
        if self.mode.current == SPAWN:
            self.setSpeed(150)
            self.directionMethod = self.goalDirection
            self.spawn()

    def startFreight(self):
        self.mode.setFreightMode()
        if self.mode.current == FREIGHT:
            self.setSpeed(50)
            self.directionMethod = self.randomDirection    

    def normalMode(self):
        self.setSpeed(100)
        self.directionMethod = self.goalDirection
        self.homeNode.denyAccess(DOWN, self)

class Blinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = BLINKY
        self.image = pygame.image.load(f'images/angelghost-0.png')
        self.image_list = [pygame.image.load(f'images/angelghost-0.png'), pygame.image.load(f'images/angelghost-1.png')]
        self.invert_image_list = [pygame.image.load(f'images/angelinverted-{n}.png') for n in range(2)]

class Pinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = PINKY
        self.image = pygame.image.load('images/butterflyghost-0.png')
        self.image_list = [pygame.image.load(f'images/butterflyghost-0.png'), pygame.image.load(f'images/butterflyghost-1.png')]
        self.invert_image_list = [pygame.image.load(f'images/butterflyinverted-{n}.png') for n in range(2)]

    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS, 0)

    def chase(self):
        self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4

class Inky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = INKY
        self.image = pygame.image.load('images/witchghost-0.png')
        self.image_list = [pygame.image.load(f'images/witchghost-0.png'), pygame.image.load(f'images/witchghost-1.png')]
        self.invert_image_list = [pygame.image.load(f'images/witchinverted-{n}.png') for n in range(2)]

    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS, TILEHEIGHT*NROWS)

    def chase(self):
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 2
        vec2 = (vec1 - self.blinky.position) * 2
        self.goal = self.blinky.position + vec2

class Clyde(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = CLYDE
        self.image = pygame.image.load('images/devilghost-0.png')
        self.image_list = [pygame.image.load(f'images/devilghost-0.png'), pygame.image.load(f'images/devilghost-1.png')]
        self.invert_image_list = [pygame.image.load(f'images/devilinverted-{n}.png') for n in range(2)]

    def scatter(self):
        self.goal = Vector2(0, TILEHEIGHT*NROWS)

    def chase(self):
        d = self.pacman.position - self.position
        ds = d.magnitudeSquared()
        if ds <= (TILEWIDTH * 8)**2:
            self.scatter()
        else:
            self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4

class GhostGroup(object):
    def __init__(self, node, pacman):
        self.blinky = Blinky(node, pacman)
        self.pinky = Pinky(node, pacman)
        self.inky = Inky(node, pacman, self.blinky)
        self.clyde = Clyde(node, pacman)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

    def __iter__(self):
        return iter(self.ghosts)

    def SpeedIncrease(self):
        self.speed += 25
        print(f'Speed is now {self.speed}') 

    def ResetSpeed(self):
        self.speed = 100
        print(f'Speed has been set back to {self.speed}') 

    def checkGhostEvents(self):
       for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FREIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.game.sound.runningawaysfx()
                    self.game.updateScore(ghost.points)
                    self.game.textgroup.addText(str(ghost.points), 
                                            WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                    self.updatePoints()
                    self.pause.setPause(pauseTime=1, func=self.game.showEntities())
                    ghost.startSpawn()
                    self.game.NodeGroup.allowHomeAccess(ghost)
                elif ghost.mode.current is not SPAWN:
                     if self.pacman.alive:
                         self.game.lives -=  1
                         self.game.lifesprites.removeImage()
                         self.pacman.die()
                         self.hide()
                         if self.game.lives <= 0:
                             self.game.textgroup.showText(GAMEOVERTXT)
                             self.game.sound.gameover()
                             if self.game.score > self.game.high_score:
                                self.game.saveHighScore(self.game.score)
                                self.game.textgroup.updateHighScore(self.game.high_score)
                             self.game.pause.setPause(pauseTime=3, func=self.game.restartGame)
                         else:
                             self.game.pause.setPause(pauseTime=3, func=self.game.resetLevel)

    def update(self, dt):
        for ghost in self:
            ghost.update(dt)

    def startFreight(self):
        for ghost in self:
            ghost.startFreight()
        self.resetPoints()

    def setSpawnNode(self, node):
        for ghost in self:
            ghost.setSpawnNode(node)

    def updatePoints(self):
        for ghost in self:
            ghost.points *= 2

    def resetPoints(self):
        for ghost in self:
            ghost.points = 200

    def hide(self):
        for ghost in self:
            ghost.visible = False

    def show(self):
        for ghost in self:
            ghost.visible = True

    def reset(self):
        for ghost in self:
            ghost.reset()

    def render(self, screen):
        for ghost in self:
            ghost.render(screen)