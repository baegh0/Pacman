import pygame as pg
import sys
from pygame.locals import *
import settings as setting

class Game(object):
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(setting.SCREENSIZE, 0, 32)
        self.background = None
    
    def setBackground(self):
        self.background = pg.surface.Surface(setting.SCREENSIZE).convert()
        self.background.fill(setting.BLACK)
    
    def startGame(self):
        self.setBackground()
    
    def checkEvents(self):
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
    
    def render(self):
        self.screen.blit(self.background, (0,0))
        pg.display.update()
    
    def update(self):
        self.checkEvents()
        self.render()

if __name__ == "__main__":
    game = Game()
    game.startGame()
    while True:
        game.update()