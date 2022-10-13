import pygame as pg
from pygame.sprite import Sprite, Group
from vector import Vector

class Ghost(Sprite):
    angel_ghost = [pg.image.load(f'images/angel ghost-{n}.png') for n in range(2)]
    butterfly_ghost = [pg.image.load(f'images/butterfly ghost-{n}.png') for n in range(2)]
    devil_ghost = [pg.image.load(f'images/devil ghost-{n}.png') for n in range(2)]
    witch_ghost = [pg.image.load(f'images/witch ghost-{n}.png') for n in range(2)]
    
class Ghosts(self, screen):
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
    def choose_node(self): pass
    def change_direction(self): pass