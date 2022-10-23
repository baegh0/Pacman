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
        self.bg_image = pg.image.load('images/bg.png')
        self.background = None
        self.clock = pg.time.Clock()
        self.createComponents()
    
    #creates the Starting Screen Menu
    def startScreen(self):
        while True:
            self.screen.blit(self.bg_image, (0,0))
            pg.display.flip()
            self.check_button()

    def setBackground(self):
        self.background = pg.surface.Surface(setting.SCREENSIZE).convert()
        self.background.fill(setting.BLACK)

    # Checks if the play button is pressed or the high score button
    def check_button(self):
        mouse = pg.mouse.get_pos()
        ev = pg.event.get()
        for event in ev:
            if event.type == pg.MOUSEBUTTONDOWN:
                if 248 <= mouse[0] <= 452 and 568 <= mouse[1] <= 644:
                 self.startGame()
                # if 286 <= mouse[0] <= 515 and 438 <= mouse[1] <= 492:
                #     pg.quit()
                #     sys.exit()
                # if 290 <= mouse[0] <= 515 and 372 <= mouse[1] <= 421:
                #     self.hs_screen()
    
    def createComponents(self):
        self.nodes = Nodes("maze.txt")
        self.nodes.setSides((0,17), (27,17))
        self.player = Player(self.nodes.getStartNode())
        self.candy = CandyGroup()

    def startGame(self):
        self.setBackground()
        self.nodes = Nodes("maze.txt")
        self.nodes.setSides((0,17), (27,17))
        self.player = Player(self.nodes.getStartNode())
        self.candy = CandyGroup()
        while True:
            self.update()

    def checkEvents(self):
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
    
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
        pg.display.update()

if __name__ == "__main__":
    game = Game()
    game.startScreen()
    # game.startGame()