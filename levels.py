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
        self.xbrickNum = 3
        self.ybrickNum = 3
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
        self.xbrickNum = 5
        self.ybrickNum = 5
        Bricka.create_bricks(self)

class Level3(Bricka):
    def __init__(self):
        Bricka.__init__(self)
    def init_game(self):
        Bricka.init_game(self)
        self.start_message = "BE CAREFUL, PURPLE BRICKS ARE MORE DURABLE."
    def create_bricks(self):
        self.power_chance = .125
        self.double_chance = .1
        self.xbrickNum = 6
        self.ybrickNum = 6
        Bricka.create_bricks(self)

class Level4(Bricka):
    def __init__(self):
        Bricka.__init__(self)
    def init_game(self):
        Bricka.init_game(self)
        self.start_message = "BONUS ROUND:   POWERUP FRENZY"
    def create_bricks(self):
        self.power_chance = .625
        self.double_chance = .0
        self.xbrickNum = 8
        self.ybrickNum = 8
        Bricka.create_bricks(self)

class Level5(Bricka):
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

class Level6(Bricka):
    def __init__(self):
        Bricka.__init__(self)
    def init_game(self):
        Bricka.init_game(self)
        self.start_message = "THE MORE BRICKS THE MERRIER"
    def create_bricks(self):
        self.power_chance = .175
        self.double_chance = .3
        self.xbrickNum = 10
        self.ybrickNum = 10
        Bricka.create_bricks(self)

class Level7(Bricka):
    def __init__(self):
        Bricka.__init__(self)
    def init_game(self):
        Bricka.init_game(self)
        self.start_message = "ITS A HARD KNOCK LIFE, BUT POWERUPS WILL SAVE YOU"
    def create_bricks(self):
        self.power_chance = .25
        self.double_chance = .5
        self.xbrickNum = 10
        self.ybrickNum = 10
        Bricka.create_bricks(self)

class Level8(Bricka):
    def __init__(self):
        Bricka.__init__(self)
    def init_game(self):
        Bricka.init_game(self)
        self.power_chance = .0
        self.double_chance = .99
        self.start_message = "BONUS ROUND:   NO POWERUPS, NO HOPE"
    def create_bricks(self):
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
