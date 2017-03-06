"""
 bricka (a breakout clone)
 Developed by Leonel Machava <leonelmachava@gmail.com>

 http://codeNtronix.com

 Fixed up by William Derksen and Alex Li
"""
import sys
import pygame
import random
import math
from constants import *

class PowerUp:
    def __init__(self, name, shape):
        self.name = name
        self.shape = shape

class Bricka:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        self.brick_pop_sound = pygame.mixer.Sound("PopSound.wav")
        self.paddle_sound = pygame.mixer.Sound("paddleHit.wav")

        self.xbrickNum = 9
        self.ybrickNum = 9


        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("bricka (a breakout clone by codeNtronix.com)")

        self.clock = pygame.time.Clock()

        if pygame.font:
            self.font = pygame.font.Font(None,30)
        else:
            self.font = None

        self.init_game()


    def init_game(self):
        self.lives = 3
        self.score = 0
        self.state = STATE_BALL_IN_PADDLE

        self.paddle   = pygame.Rect(300,PADDLE_Y,PADDLE_WIDTH,PADDLE_HEIGHT)
        self.ball     = pygame.Rect(300,PADDLE_Y - BALL_DIAMETER,BALL_DIAMETER,BALL_DIAMETER)

        theta = random.random()*math.pi*(90.)/180. + math.pi*45./180.
        self.ball_vel = [BALL_SPEED*math.cos(theta), BALL_SPEED-math.sin(theta)]
        self.ball_left = float(self.ball.left)
        self.ball_top = float(self.ball.top)
        self.ball_vel_orig = [BALL_SPEED*math.cos(theta), BALL_SPEED-math.sin(theta)]
        self.pows = [] #list of PowerUp instances
        self.powtypes = ['fire', 'grow','shrink', 'airbounce']
        self.powdict = {'fire':FIREBLAZE,'grow':GROW, 'shrink':SHRINK, 'airbounce':AIRBOUNCE} #Dictionary for powerups their shape and their colors
        self.totfiretime = 150 #50 frames a second, so 4 seconds
        self.totgrowtime = 300
        self.totshrinktime = 300
        #self.pow_effect_dict = {'fire':self.fireball=1}
        self.create_bricks()


    def create_bricks(self):
        self.BRICK_WIDTH = (SCREEN_SIZE[0] - 2*marginx - (self.xbrickNum-1) * xspacing)/self.xbrickNum
        self.BRICK_HEIGHT = (SCREEN_SIZE[1] - 2*marginy - (self.ybrickNum-1) * yspacing - bottom_to_brick)/self.ybrickNum
        y_ofs = marginy
        self.bricks = []
        for i in range(self.ybrickNum):
            x_ofs = marginx
            for j in range(self.xbrickNum):
                self.bricks.append(pygame.Rect(x_ofs,y_ofs,self.BRICK_WIDTH,self.BRICK_HEIGHT))
                x_ofs += self.BRICK_WIDTH + xspacing
            y_ofs += self.BRICK_HEIGHT + yspacing

    def draw_bricks(self):
        for brick in self.bricks:
            pygame.draw.rect(self.screen, BRICK_COLOR, brick)

    def draw_Pow(self):
        for power_up in self.pows:
            powcolor = self.powdict.get(power_up.name)
            pygame.draw.rect(self.screen, powcolor, power_up.shape)

    def check_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.paddle.left -= PADDLE_SPEED
            if self.paddle.left < 0:
                self.paddle.left = 0

        if keys[pygame.K_RIGHT]:
            self.paddle.left += PADDLE_SPEED
            if self.paddle.left > MAX_PADDLE_X:
                self.paddle.left = MAX_PADDLE_X

        if keys[pygame.K_SPACE] and self.state == STATE_BALL_IN_PADDLE:
            self.ball_vel = self.ball_vel_orig
            self.state = STATE_PLAYING
        elif keys[pygame.K_RETURN] and (self.state == STATE_GAME_OVER):
            self.init_game()
        elif keys[pygame.K_RETURN] and self.state == STATE_WON:
            pygame.quit()
            return True

    def move_pow(self):
        for power_up in self.pows:
            power_up.shape.top += POW_FALL_SPD
            if power_up.shape.top > float(MAX_BALL_Y+30): #added 30 hear to make sure powerups go offsceen before solving.
                self.pows.remove(power_up)


    def move_ball(self):
        #print(type(self.ball))
        self.ball_top_old = self.ball_top
        self.ball_left_old = self.ball_left
        self.ball_left += self.ball_vel[0]
        self.ball_top += self.ball_vel[1]

        if self.ball_left <= 0:
            self.ball_left = 0.
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball_left >= MAX_BALL_X:
            self.ball_left = float(MAX_BALL_X)
            self.ball_vel[0] = -self.ball_vel[0]
        if self.ball_top < 0:
            self.ball_top = 0.
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball_top >= MAX_BALL_Y:
            self.ball_top =float(MAX_BALL_Y)
            self.ball_vel[1] = -self.ball_vel[1]
        self.ball.left = int(self.ball_left)
        self.ball.top  = int(self.ball_top)

    def handle_collisions(self):
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.brick_pop_sound.play()
                #print(brick.topright)
                self.score += 5
                if self.fireball == False:
                    if self.ball_left < brick.right and self.ball_left_old > brick.right:  #(self.ball.collidepoint(brick.topright) or self.ball.collidepoint(brick.bottomright)):
                        self.ball_vel[0] = abs(self.ball_vel[0])
                    elif self.ball_left+BALL_DIAMETER > brick.left and self.ball_left_old+BALL_DIAMETER < brick.left:  #(self.ball.collidepoint(brick.topleft) or self.ball.collidepoint(brick.bottomleft)):
                        self.ball_vel[0] = -abs(self.ball_vel[0])
                    else:
                        self.ball_vel[1] = -self.ball_vel[1]
                self.bricks.remove(brick)
                if random.random() > .925:
                    self.pows.append(PowerUp(random.choice(self.powtypes),pygame.Rect(brick.centerx - POWER_WIDTH/2,brick.centery- POWER_HEIGHT/2,POWER_WIDTH,POWER_HEIGHT)))
                break

        if len(self.bricks) == 0:
            self.state = STATE_WON
        for power_up in self.pows:
            if power_up.shape.colliderect(self.paddle):
                if power_up.name == 'fire': #change to dictionary of some sort ******
                    self.fireball = True
                    self.firetime = 0
                if power_up.name == 'grow':
                    self.grow = True
                    self.growtime = 0
                if power_up.name == 'shrink':
                    self.shrink = True
                    self.shrinktime = 0
                self.pows.remove(power_up)
        if self.ball.colliderect(self.paddle):
            self.paddle_sound.play()
            self.ball.top = PADDLE_Y - BALL_DIAMETER
            #print(type(self.paddle.right))
            #print(type(self.paddle.left))
            #print(type(self.ball.center[0]))
            balltopad = float(self.paddle.right - self.ball.center[0])/float(self.paddle.right - self.paddle.left)
            theta = balltopad*math.pi*(90)/180 + math.pi*(45)/180
            #print(theta)
            self.ball_vel = [BALL_SPEED*math.cos(theta), BALL_SPEED*-math.sin(theta)]
        elif self.ball.top > self.paddle.top:
            self.lives -= 1
            if self.lives > 0:
                self.state = STATE_BALL_IN_PADDLE
            else:
                self.state = STATE_GAME_OVER

    def show_stats(self):
        if self.font:
            font_surface = self.font.render("SCORE: " + str(self.score) + " LIVES: " + str(self.lives), False, WHITE)
            self.screen.blit(font_surface, (205,5))

    def show_message(self,message):
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message,False, WHITE)
            x = (SCREEN_SIZE[0] - size[0]) / 2
            y = (SCREEN_SIZE[1] - size[1]) / 2
            self.screen.blit(font_surface, (x,y))


    def run(self):
        self.fireball = 0
        self.firetime = 0
        self.grow = 0
        self.growtime = 0
        self.shrink = 0
        self.shrinktime = 0
        self.airbounce = 0
        self.level = 1
        self.levelloaded = 0
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
            self.clock.tick(50)
            self.screen.fill(BLACK)
            done = self.check_input()
            if done:
                return None
            if self.grow and self.shrink:
                self.growtime = 999
                self.shrinktime = 999
            elif self.grow:
                self.paddle.width = GROW_PADDLE
            elif self.shrink:
                self.paddle.width = SHRINK_PADDLE

            if self.state == STATE_PLAYING:
                self.move_ball()
                self.move_pow()
                self.handle_collisions()
            elif self.state == STATE_BALL_IN_PADDLE:
                self.ball_top_old = self.ball_top
                self.ball_left_old = self.ball_left
                self.ball_left = float(self.paddle.left + self.paddle.width / 2)
                self.ball_top  = float(self.paddle.top - self.ball.height)
                self.ball.left = self.ball_left
                self.ball.top = self.ball_top
                self.show_message("PRESS SPACE TO LAUNCH THE BALL")
            elif self.state == STATE_GAME_OVER:
                self.show_message("GAME OVER. PRESS ENTER TO PLAY AGAIN")
            elif self.state == STATE_WON:
                self.show_message("YOU WON! PRESS ENTER FOR THE NEXT LEVEL")

            self.draw_bricks()
            self.draw_Pow()
            pygame.draw.line(self.screen, FIREBLAZE, (self.ball.center[0], self.ball.center[1]), (self.ball.center[0] + self.ball_vel[0]*3, self.ball.center[1]+self.ball_vel[1]*3), 4)
            pygame.draw.line(self.screen, AIRBOUNCE, (self.ball.center[0], SCREEN_SIZE[1]-20), (self.ball.center[0]+self.ball_vel[0]*3, SCREEN_SIZE[1]-20), 4)
            pygame.draw.line(self.screen, AIRBOUNCE, (SCREEN_SIZE[0]-20, self.ball.center[1]), (SCREEN_SIZE[0]-20, self.ball.center[1]+self.ball_vel[1]*3), 4)
            # Draw paddle
            pygame.draw.rect(self.screen, BLUE, self.paddle)

            # Draw ball
            if self.fireball == 0:
                pygame.draw.circle(self.screen, WHITE, (self.ball.left + BALL_RADIUS, self.ball.top + BALL_RADIUS), BALL_RADIUS)
            else:
                pygame.draw.circle(self.screen, FIREBLAZE, (self.ball.left + BALL_RADIUS, self.ball.top + BALL_RADIUS), BALL_RADIUS)
                pygame.draw.circle(self.screen, FIREAFTER, (int(self.ball_left_old) + BALL_RADIUS, int(self.ball_top_old)+ BALL_RADIUS), int(BALL_RADIUS/1.35))
            self.show_stats()
            #self.fireball = True
            if self.fireball and self.firetime < self.totfiretime:
                self.firetime += 1
            else:
                self.firetime = 0
                self.fireball = False
            if self.grow and self.growtime < self.totgrowtime:
                self.growtime += 1
            else:
                self.growtime = 0
                self.grow = False
                self.paddle.width = PADDLE_WIDTH
            if self.shrink and self.shrinktime < self.totshrinktime:
                self.shrinktime += 1
            else:
                self.shrinktime = 0
                self.shrink = False
                self.paddle.width = PADDLE_WIDTH
            pygame.display.flip()

if __name__ == "__main__":
    Bricka().run()
