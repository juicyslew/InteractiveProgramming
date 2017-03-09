from BrickBreaker import *
from testOne import *
from constants import *
import sys
import pygame
import random
import math

class Level1(Bricka):
    def __init__(self):
        Bricka.__init__(self)
    def init_game(self):
        Bricka.init_game(self)
        self.start_message = "WELCOME TO OUR BEAUTIFUL BREAKOUT CLONE"
    def create_bricks(self):
        self.power_chance = .125
        self.double_chance = .0
        self.xbrickNum = 4
        self.ybrickNum = 4
        Bricka.create_bricks(self)

#class Level2(Game):
#    print('blah')
class Level2(Bricka):
    def __init__(self):
        Bricka.__init__(self)
    def init_game(self):
        Bricka.init_game(self)
        self.start_message = "WE HOPE YOU LIKE BRICKS! THERE ARE MANY MORE TO COME"
    def create_bricks(self):
        self.power_chance = .125
        self.double_chance = .0
        self.xbrickNum = 6
        self.ybrickNum = 6
        Bricka.create_bricks(self)

class Level3(Bricka):
    def __init__(self):
        Bricka.__init__(self)
    def init_game(self):
        Bricka.init_game(self)
        self.start_message = "BONUS ROUND:   SMASH THAT POWERUP BUTTOM"
    def create_bricks(self):
        self.power_chance = .625
        self.double_chance = .0
        self.xbrickNum = 8
        self.ybrickNum = 8
        Bricka.create_bricks(self)

class Level4(Bricka):
    def __init__(self):
        Bricka.__init__(self)
    def init_game(self):
        Bricka.init_game(self)
        self.start_message = "BE CAREFUL, PURPLE BRICKS ARE MORE DURABLE."
    def create_bricks(self):
        self.power_chance = .125
        self.double_chance = .2
        self.xbrickNum = 6
        self.ybrickNum = 6
        Bricka.create_bricks(self)

class Level5(Bricka):
    def __init__(self):
        Bricka.__init__(self)
    def init_game(self):
        Bricka.init_game(self)
        self.start_message = "BONUS ROUND:   GET SCHWIFTY"
        self.start_total_time = 50*120 #after 2 minutes (120 seconds) the player will have survived long enough
    def create_bricks(self):
        self.power_chance = .35
        self.double_chance = 0
        self.xbrickNum = 12
        self.ybrickNum = 12
        Bricka.create_bricks(self)
    def move_ball(self):
        self.ball_vel[0] += random.random()*2-1
        self.ball_vel[1] += random.random()*2-1
        Bricka.move_ball(self)

class Level6(Bricka):
    def __init__(self):
        Bricka.__init__(self)
    def init_game(self):
        Bricka.init_game(self)
        self.start_message = "THESE PURPLE BLOCKS JUST WON'T QUIT"
    def create_bricks(self):
        self.power_chance = .175
        self.double_chance = .3
        self.xbrickNum = 8
        self.ybrickNum = 8
        Bricka.create_bricks(self)

class Level7(Bricka):
    def __init__(self):
        Bricka.__init__(self)
    def init_game(self):
        Bricka.init_game(self)
        self.start_message = "BONUS ROUND:   WHAT IN FRESH HECK IS GOING ON?"
    def create_bricks(self):
        self.power_chance = .4
        self.double_chance = 0
        self.xbrickNum = 10
        self.ybrickNum = 10
        Bricka.create_bricks(self)
    def handle_collisions(self):
        self.randcolor = (random.random()*200 +55, random.random()*200 +55, random.random()*200 +55)
        self.powdict = {'fire':self.randcolor,'grow':self.randcolor, 'shrink':self.randcolor, 'airbounce':self.randcolor, 'speedup':self.randcolor, 'slowdown': self.randcolor}
        Bricka.handle_collisions(self)

class Level8(Bricka):
    def __init__(self):
        Bricka.__init__(self)
    def init_game(self):
        Bricka.init_game(self)
        self.start_message = "THE MORE BRICKS THE MERRIER"
    def create_bricks(self):
        self.power_chance = .25
        self.double_chance = .5
        self.xbrickNum = 10
        self.ybrickNum = 10
        Bricka.create_bricks(self)

class Level9(Bricka):
    def __init__(self):
        Bricka.__init__(self)
    def init_game(self):
        Bricka.init_game(self)
        self.start_message = "BONUS ROUND:   ITS A HARD KNOCK LIFE"
    def create_bricks(self):
        self.power_chance = .4
        self.double_chance = 1
        self.xbrickNum = 12
        self.ybrickNum = 12
        Bricka.create_bricks(self)

class Level10(Bricka):
    def __init__(self):
        Bricka.__init__(self)
    def init_game(self):
        Bricka.init_game(self)
        self.start_message = "BONUS ROUND:   NO HELP, NO HOPE, NO PROBLEM"
    def create_bricks(self):
        self.power_chance = .0
        self.double_chance = 1
        self.xbrickNum = 12
        self.ybrickNum = 12
        Bricka.create_bricks(self)

#class Level3(Game):
#    print('blah')

if __name__ == "__main__":
    Level1().run()
    Level2().run()
    Level3().run()
    Level4().run()
    Level5().run()
    Level6().run()
    Level7().run()
    Level8().run()
    Level9().run()
    Level10().run()
