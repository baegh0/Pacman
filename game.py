import pygame as pg
import sys
from pygame.locals import *
from node import Nodes
import settings as setting
from ghost import Ghost

class Game(object):
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(setting.SCREENSIZE, 0, 32)
        self.background = None
        self.angel = Ghost(game=self, type=0)
        self.butterfly = Ghost(game=self, type=1)
        self.devil = Ghost(game=self, type=2)
        self.witch = Ghost(game=self, type=3)
    
    def setBackground(self):
        self.background = pg.surface.Surface(setting.SCREENSIZE).convert()
        self.background.fill(setting.BLACK)
    
    def startGame(self):
        self.setBackground()
        self.createGhosts()
        self.nodes = Nodes()
        self.nodes.test()
    
    def checkEvents(self):
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

    # creates ghosts at locations on screen? 
    def createGhosts(self):
        self.angel.rect.left, self.angel.rect.top = 336, 432
        self.butterfly.rect.left, self.butterfly.rect.top = 336, 432
        self.devil.rect.left, self.devil.rect.top = 336, 432
        self.witch.rect.left, self.witch.rect.top = 336, 432
    
    def update(self):
        self.checkEvents()
        self.draw()
    
    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.angel.draw()
        self.butterfly.draw()
        self.devil.draw()
        self.witch.draw()
        self.nodes.draw(self.screen)
        pg.display.update()

if __name__ == "__main__":
    game = Game()
    game.startGame()
    while True:
        game.update()