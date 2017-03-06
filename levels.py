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
        self.score = 10000

    def create_bricks(self):
        self.xbrickNum = 2
        self.ybrickNum = 1
        Bricka.create_bricks(self)

#class Level2(Game):
#    print('blah')
class Level2(Bricka):
    def __init__(self):
        Bricka.__init__(self)

    def create_bricks(self):
        self.xbrickNum = 2
        self.ybrickNum = 2
        Bricka.create_bricks(self)

#class Level3(Game):
#    print('blah')

if __name__ == "__main__":
    Level1().run()
    Level2().run()
    main()
