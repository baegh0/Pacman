import pygame
import sys
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import *
from fruit import Fruit
from pause import Pause
from text import TextGroup
from sound import Sound
from timer import Timer

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
        self.background = pygame.image.load('images/game_bg.png')
        self.titlescreen = pygame.image.load('images/bg.png')
        self.sound = Sound(bg_music="sounds/PacManOP.mp3")
        self.NodeGroup = NodeGroup()
        self.pacman = Pacman(self.NodeGroup.getNodeFromTiles(15, 26))
        self.ghosts = GhostGroup(self.NodeGroup.getStartTempNode(), self)
        self.pellets = PelletGroup(self)
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.level = 0
        self.pause = Pause(True)
        self.score = 0
        self.high_score = self.getHighScore()
        self.textgroup = TextGroup(self.high_score)
<<<<<<< HEAD:run.py
        self.lifesprites = LifeIcons(self.pacman.lives)
=======
        self.lifesprites = LifeIcons(self.lives)
        self.NodeGroup = NodeGroup()
        self.sound = Sound(bg_music="sounds/PacManOP.mp3")
>>>>>>> e2c5edd7ef8cf79e866648218b5aca801c9ac439:game.py

    def startScreen(self):
        self.sound.startupsfx()
        pacman = [pygame.image.load('images/pumpkinman0.png'), pygame.image.load('images/pumpkinman1.png')]
        ghost_1 = [pygame.transform.flip(pygame.image.load(f'images/angelghost-{n}.png'), True, False) for n in range(2)]
        ghost_2 = [pygame.transform.flip(pygame.image.load(f'images/butterflyghost-{n}.png'),True, False) for n in range(2)]
        ghost_3 = [pygame.transform.flip(pygame.image.load(f'images/devilghost-{n}.png'), True, False) for n in range(2)]
        ghost_4 = [pygame.transform.flip(pygame.image.load(f'images/witchghost-{n}.png'), True, False) for n in range(2)]
        ghost_list = [ghost_1, ghost_2, ghost_3, ghost_4]
        pacman_timer = Timer(image_list = pacman, delay = 200)
        ghost_timer_list = [Timer(image_list=ghost, delay=150) for ghost in ghost_list]

        start_position = 672
        while True:
            self.screen.blit(self.titlescreen, (0,0))
            image = pacman_timer.image()
            self.screen.blit(image, (start_position, SCREENHEIGHT / 2))
            for n,timer in enumerate(ghost_timer_list):
                self.screen.blit(timer.image(), (start_position + 70*n, SCREENHEIGHT / 2))
            start_position -= 2
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
        self.sound.levelupsfx()
        self.showEntities()
        self.level += 1
        self.pause.paused = True
        self.ghosts.SpeedIncrease()
        self.textgroup.updateLevel(self.level)
        self.startGame()

    def restartGame(self):
        self.ghosts.ResetSpeed()
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.startGame()

    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None
        self.textgroup.showText(READYTXT)

    def setBackground(self):
        self.screen.blit(self.background, (0, 0))

    def startGame(self):
        self.sound.play_bg()
        self.high_score = self.getHighScore()
        self.NodeGroup.setPortalPair((0,17), (27,17))
        homekey = self.NodeGroup.createHomeNodes(11.5, 14)
        self.NodeGroup.connectHomeNodes(homekey, (12,14), LEFT)
        self.NodeGroup.connectHomeNodes(homekey, (15,14), RIGHT)
        self.pacman = Pacman(self.NodeGroup.getNodeFromTiles(15, 26))
        self.pellets = PelletGroup()
        self.ghosts = GhostGroup(self.NodeGroup.getStartTempNode(), self.pacman)
        self.ghosts.angel.setStartNode(self.NodeGroup.getNodeFromTiles(2+11.5, 0+14))
        self.ghosts.butterfly.setStartNode(self.NodeGroup.getNodeFromTiles(2+11.5, 3+14))
        self.ghosts.witch.setStartNode(self.NodeGroup.getNodeFromTiles(0+11.5, 3+14))
        self.ghosts.devil.setStartNode(self.NodeGroup.getNodeFromTiles(4+11.5, 3+14))
        self.ghosts.setSpawnNode(self.NodeGroup.getNodeFromTiles(2+11.5, 3+14))
        self.NodeGroup.denyHomeAccess(self.pacman)
        self.NodeGroup.denyHomeAccessList(self.ghosts)
<<<<<<< HEAD:run.py
        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)
        for dir in [LEFT, RIGHT]:
            NodeGroup().denyAccessList(2+11.5, 3+14, dir, self.ghosts)
        for x, y in [(x, y) for x in X for y in Y]:
            NodeGroup().denyAccessList(x, y, UP, self.ghosts)
=======
        self.NodeGroup.denyAccessList(2+11.5, 3+14, LEFT, self.ghosts)
        self.NodeGroup.denyAccessList(2+11.5, 3+14, RIGHT, self.ghosts)
        self.ghosts.witch.startNode.denyAccess(RIGHT, self.ghosts.witch)
        self.ghosts.devil.startNode.denyAccess(LEFT, self.ghosts.devil)
        self.NodeGroup.denyAccessList(12, 14, UP, self.ghosts)
        self.NodeGroup.denyAccessList(15, 14, UP, self.ghosts)
        self.NodeGroup.denyAccessList(12, 26, UP, self.ghosts)
        self.NodeGroup.denyAccessList(15, 26, UP, self.ghosts)
>>>>>>> e2c5edd7ef8cf79e866648218b5aca801c9ac439:game.py
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
        self.draw()

    def updateScore(self, points):
        self.score += points
        self.textgroup.updateScore(self.score)
    
    def getHighScore(self):
    # Try to read the high score from a file
        try:
            high_score_file = open("high_score.txt", "r")
            high_score = int(high_score_file.read())
            high_score_file.close()
            print("The high score is", high_score)
        except IOError:
            # Error reading file, no high score
            print("There is no high score yet.")
        except ValueError:
            # There's a file there, but we don't understand the number.
            print("I'm confused. Starting with no high score.")
 
        return high_score
    
    def saveHighScore(self, new_high_score):
        try:
        # Write the file to disk
            high_score_file = open("high_score.txt", "w")
            high_score_file.write(str(new_high_score))
            high_score_file.close()
        except IOError:
            # Hm, can't write it.
            print("Unable to save the high score.")

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

    def draw(self):
        self.ghosts.render(self.screen)
        self.pacman.draw(self.screen)
        self.pellets.draw(self.screen)
        if self.fruit is not None:
            self.fruit.draw(self.screen)
        self.textgroup.draw(self.screen)
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
                             if self.score > self.high_score:
                                self.saveHighScore(self.score)
                                self.textgroup.updateHighScore(self.high_score)
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
        pp = self.pacman.eatPellets(self.pellets.powerpellets)
        if pellet:
            self.pellets.numEaten += 1
            self.updateScore(pellet.points)
            if self.pellets.numEaten == 30:
                self.ghosts.witch.startNode.allowAccess(RIGHT, self.ghosts.witch)
            if self.pellets.numEaten == 70:
                self.ghosts.devil.startNode.allowAccess(LEFT, self.ghosts.devil)
            self.pellets.pelletList.remove(pellet)
            if pp:
                self.ghosts.startFreight()
                self.pellets.powerpellets.remove(pp)
            if self.pellets.isEmpty():
                self.hideEntities()
                self.pause.setPause(pauseTime=3, func=self.nextLevel)

if __name__ == "__main__":
    game = GameController()
    while True:
        game.startScreen()