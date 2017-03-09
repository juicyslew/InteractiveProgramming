'''
global constants
'''
SCREEN_SIZE   = 1020, 1020

xbrickNum = 9
ybrickNum = 9
xspacing = 10
yspacing = 10

marginx = 50
marginy = 50

bottom_to_brick = 300

BRICK_WIDTH = (SCREEN_SIZE[0] - 2*marginx - (xbrickNum-1) * xspacing)/xbrickNum
BRICK_HEIGHT = (SCREEN_SIZE[1] - 2*marginy - (ybrickNum-1) * yspacing - bottom_to_brick)/ybrickNum

#print(BRICK_WIDTH)
#print(BRICK_HEIGHT)
# Object dimensions
#BRICK_WIDTH   = 60
#BRICK_HEIGHT  = 60
PADDLE_WIDTH  = 100

PADDLE_HEIGHT = 12
POWER_WIDTH = 14
POWER_HEIGHT = 8
BALL_DIAMETER = 16
BALL_RADIUS   = int(BALL_DIAMETER / 2)
POW_FALL_SPD = 6.0
BALL_SPEED = 11.0
PADDLE_SPEED = 10.0
GROW_PADDLE = 150
SHRINK_PADDLE = 50



MAX_PADDLE_X = SCREEN_SIZE[0] - PADDLE_WIDTH
MAX_BALL_X   = SCREEN_SIZE[0] - BALL_DIAMETER
MAX_BALL_Y   = SCREEN_SIZE[1] - BALL_DIAMETER

# Paddle Y coordinate
PADDLE_Y = SCREEN_SIZE[1] - PADDLE_HEIGHT - 10

# Color constants
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE  = (50,100,200)
BRICK_COLOR = (20,200,150)
FIREBLAZE = (225, 225, 0)
FIREAFTER = (225, 100, 0)
GROW = (50, 240, 50)
SHRINK = (240, 50, 50)
AIRBOUNCE =(200, 40, 230)

# State constants
STATE_BALL_IN_PADDLE = 0
STATE_PLAYING = 1
STATE_WON = 2
STATE_GAME_OVER = 3
