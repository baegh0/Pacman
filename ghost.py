import pygame as pg
from pygame.sprite import Sprite, Group
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


    def __init__(self, game, type):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pg.image.load('images/angel ghost-0.png')
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.height
        self.type = type # will be the list of images that determine which ghost it is, make a dict with keys to determine which ghost it is
        self.hit = False # will control when the ghost is hit and changes to the secondary form
        self.timer_regular = Timer(self.type)
        self.mode = self.chase_dict[type]# decides which version (chase mode, scatter mode, or run mode)

    def choose_node(self): pass

    def switch_scatter(self): pass # If pacman eats the candy, ghosts will change to scatter mode and run awway

    def switch_chase(self):


# 
class Ghosts:
    def __init__(self): pass

    def draw(self): pass

    def update(self): pass
    # Switch to chasing PacMan
    def switch_chase(self): pass
    # Switch to scatter, running away
    def switch_scatter(self): pass
    # Switch to running key
    def switch_run(self): pass

    def switch_spawn(self): pass
    def change_direction(self): pass