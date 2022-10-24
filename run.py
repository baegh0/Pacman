import pygame
import sys
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit
from pause import Pause
from text import TextGroup
from sound import Sound

class LifeIcons(object):
    def __init__(self, numlives) -> None:
        self.image = pygame.image.load('images/pumpkinman0.png')
        self.resetLives(numlives)

    def removeImage(self):
        if len(self.images) > 0:
            self.images.pop(0)

    def resetLives(self, numlives):
        self.images = []
        for i in range(numlives):
            self.images.append(self.image)

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE)
        self.background = None
        self.titlescreen = pygame.image.load('images/bg.png')
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.level = 0
        self.pause = Pause(True)
        self.lives = 3
        self.score = 0
        self.textgroup = TextGroup()
        self.lifesprites = LifeIcons(self.lives)
        # self.sound = Sound(bg_music="sounds/PacManOP.mp3")

    def startScreen(self):
        # self.sound.startupsfx()
        while True:
            self.screen.blit(self.titlescreen, (0,0))
            pygame.display.flip()
            self.check_button()

    # Checks if the play button is pressed or the high score button
    def check_button(self):
        mouse = pygame.mouse.get_pos()
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 248 <= mouse[0] <= 452 and 568 <= mouse[1] <= 644:
                 self.startGame()

    def nextLevel(self):
        # self.sound.levelupsfx()
        self.showEntities()
        self.level += 1
        self.pause.paused = True
        self.startGame()
        self.ghosts.SpeedIncrease()
        self.textgroup.updateLevel(self.level)

    def restartGame(self):
        self.lives = 3
        self.ghosts.ResetSpeed()
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.startGame()
        self.score = 0
        self.textgroup.updateScore(self.score)
        self.textgroup.updateLevel(self.level)
        self.textgroup.showText(READYTXT)
        self.lifesprites.resetLives(self.lives)

    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None
        self.textgroup.showText(READYTXT)

    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)
        self.screen.blit(self.background, (0, 0))

        

    def startGame(self):
        # self.sound.play_bg()
        self.NodeGroup = NodeGroup()
        self.NodeGroup.setPortalPair((0,17), (27,17))
        homekey = self.NodeGroup.createHomeNodes(11.5, 14)
        self.NodeGroup.connectHomeNodes(homekey, (12,14), LEFT)
        self.NodeGroup.connectHomeNodes(homekey, (15,14), RIGHT)
        self.pacman = Pacman(self.NodeGroup.getNodeFromTiles(15, 26))
        self.pellets = PelletGroup()
        self.ghosts = GhostGroup(self.NodeGroup.getStartTempNode(), self.pacman)
        self.ghosts.blinky.setStartNode(self.NodeGroup.getNodeFromTiles(2+11.5, 0+14))
        self.ghosts.pinky.setStartNode(self.NodeGroup.getNodeFromTiles(2+11.5, 3+14))
        self.ghosts.inky.setStartNode(self.NodeGroup.getNodeFromTiles(0+11.5, 3+14))
        self.ghosts.clyde.setStartNode(self.NodeGroup.getNodeFromTiles(4+11.5, 3+14))
        self.ghosts.setSpawnNode(self.NodeGroup.getNodeFromTiles(2+11.5, 3+14))
        self.NodeGroup.denyHomeAccess(self.pacman)
        self.NodeGroup.denyHomeAccessList(self.ghosts)
        self.NodeGroup.denyAccessList(2+11.5, 3+14, LEFT, self.ghosts)
        self.NodeGroup.denyAccessList(2+11.5, 3+14, RIGHT, self.ghosts)
        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)
        self.NodeGroup.denyAccessList(12, 14, UP, self.ghosts)
        self.NodeGroup.denyAccessList(15, 14, UP, self.ghosts)
        self.NodeGroup.denyAccessList(12, 26, UP, self.ghosts)
        self.NodeGroup.denyAccessList(15, 26, UP, self.ghosts)
        while True:
            self.setBackground()
            self.update()

    def update(self):
        dt = self.clock.tick(30) / 1000.0   
        self.textgroup.update(dt)    
        self.pellets.update(dt)
        if not self.pause.paused:
            self.pacman.update(dt, self.screen)
            self.ghosts.update(dt)        
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            self.checkGhostEvents()
            self.checkFruitEvents()
        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.render()

    def updateScore(self, points):
        self.score += points
        self.textgroup.updateScore(self.score)


    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman.alive:
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            self.textgroup.hideText()
                            self.showEntities()
                        else:
                            self.textgroup.showText(PAUSETXT)
                            self.hideEntities()

    def render(self):
        self.ghosts.render(self.screen)
        self.pacman.render(self.screen)
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.textgroup.render(self.screen)
        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x, y))
        pygame.display.update()

    def checkGhostEvents(self):
       for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FREIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.sound.runningawaysfx()
                    self.updateScore(ghost.points)
                    self.textgroup.addText(str(ghost.points), 
                                            WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                    self.ghosts.updatePoints()
                    self.pause.setPause(pauseTime=1, func=self.showEntities)
                    ghost.startSpawn()
                    self.NodeGroup.allowHomeAccess(ghost)
                elif ghost.mode.current is not SPAWN:
                     if self.pacman.alive:
                         self.lives -=  1
                         self.lifesprites.removeImage()
                         self.pacman.die()
                         self.ghosts.hide()
                         if self.lives <= 0:
                             self.textgroup.showText(GAMEOVERTXT)
                             self.sound.gameover()
                             self.pause.setPause(pauseTime=3, func=self.restartGame)
                         else:
                             self.pause.setPause(pauseTime=3, func=self.resetLevel)



    def showEntities(self):
        self.pacman.visible = True
        self.ghosts.show()

    def hideEntities(self):
        self.pacman.visible = False
        self.ghosts.hide()

    def checkFruitEvents(self):
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.NodeGroup.getNodeFromTiles(9, 20))
        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                self.sound.eatingsfx()
                self.updateScore(self.fruit.points)
                self.textgroup.addText(str(self.fruit.points), WHITE, 
                                      self.fruit.position.x, self.fruit.position.y, 8, time=1)
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.updateScore(pellet.points)
            if self.pellets.numEaten == 30:
                self.ghosts.inky.startNode.allowAccess(RIGHT, self.ghosts.inky)
            if self.pellets.numEaten == 70:
                self.ghosts.clyde.startNode.allowAccess(LEFT, self.ghosts.clyde)
            self.pellets.pelletList.remove(pellet)
            if pellet.name == POWERPELLET:
                self.ghosts.startFreight()
            if self.pellets.isEmpty():
                self.hideEntities()
                self.pause.setPause(pauseTime=3, func=self.nextLevel)

if __name__ == "__main__":
    game = GameController()
    while True:
        game.startScreen()


