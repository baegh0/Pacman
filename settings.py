#===============================
#       Screen Dimensions
#===============================
# 24x24 Blocks
BLOCK_WIDTH = 24
BLOCK_HEIGHT = 24
# There are 28x36 Blocks
NUM_COLS = 28
NUM_ROWS = 36
# Tuple of screen size
SCREENWIDTH = NUM_COLS*BLOCK_WIDTH
SCREENHEIGHT = NUM_ROWS*BLOCK_HEIGHT
SCREENSIZE = (SCREENWIDTH, SCREENHEIGHT)

#===============================
#           Colors
#===============================
BLACK = (0,0,0)
YELLOW = (255, 255, 0)

#===============================
#           Controls
#===============================
STOP = 0
UP = 1
DOWN = -1
LEFT = 2
RIGHT = -2