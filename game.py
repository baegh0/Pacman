import pygame as pg
import sys
from pygame.locals import *
from node import Nodes
import settings as setting
from ghost import Ghost
from player import Player
from candy import CandyGroup

class Game(object):
    def __init__(self):
        pg.init()
        self.settings = setting
        self.screen = pg.display.set_mode(setting.SCREENSIZE, 0, 32)
        self.background = None
        self.clock = pg.time.Clock()
    
    def setBackground(self):
        self.background = pg.surface.Surface(setting.SCREENSIZE).convert()
        self.background.fill(setting.BLACK)
    
    def startGame(self):
        self.setBackground()
        self.nodes = Nodes("maze.txt")
        self.nodes.setSides((0,17), (27,17))
        self.player = Player(self.nodes.getStartNode())
        self.candy = CandyGroup()
        # self.ghost = Ghost(self.nodes.getStartNode(), self.player) #getStartNode() has not been implemeneted in node.py yet

    
    def checkEvents(self):
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

    # creates ghosts at locations on screen? 
    # def createGhosts(self):
    #     self.angel.rect.left, self.angel.rect.top = 336, 432
    #     self.butterfly.rect.left, self.butterfly.rect.top = 336, 432
    #     self.devil.rect.left, self.devil.rect.top = 336, 432
    #     self.witch.rect.left, self.witch.rect.top = 336, 432
    
    def update(self):
        timer = self.clock.tick(30) / 1000
        self.player.update(timer)
        # self.ghost.update(timer)
        self.candy.update(timer)
        self.checkEvents()
        self.draw()
    
    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.player.draw(self.screen)
        self.nodes.draw(self.screen)
        self.candy.draw(self.screen)
        # self.ghost.draw(self.screen)
        pg.display.update()

if __name__ == "__main__":
    game = Game()
    game.startGame()
    while True:
        game.update()