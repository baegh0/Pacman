# SCREEN
TILEWIDTH = 24
TILEHEIGHT = 24
NROWS = 36
NCOLS = 28
SCREENWIDTH = NCOLS*TILEWIDTH
SCREENHEIGHT = NROWS*TILEHEIGHT
SCREENSIZE = (SCREENWIDTH, SCREENHEIGHT)

#===============================
#           Colors
#===============================
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255,100,150)
TEAL = (100,255,255)
ORANGE = (230,190,40)
GREEN = (0, 255, 0)

#===============================
#           Controls
#===============================
STOP = 0
UP = 1
DOWN = -1
LEFT = 2
RIGHT = -2

#===============================
#         Compononents
#===============================
PACMAN = 0
GHOST = 3
PORTAL = 3
PELLET = 1
POWERPELLET = 2
BLINKY = 4
PINKY = 5
INKY = 6
CLYDE = 7
FRUIT = 8

#===============================
#            Modes
#===============================
SCATTER = 0
CHASE = 1
FREIGHT = 2
SPAWN = 3

#===============================
#            Score
#===============================
SCORETXT = 0
LEVELTXT = 1
HIGHSCORETXT = 2

#===============================
#            UI TXT
#===============================

READYTXT = 3
PAUSETXT = 4
GAMEOVERTXT = 5


#===============================
#      Deny Access Points
#===============================
X = [12, 15]
Y = [14, 24]