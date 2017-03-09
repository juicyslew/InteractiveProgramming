
"""
Bricka (Breakout Clone)
Developed and Retouched by William Derksen and Alex Li

(Originally Developed by Leonel Machava)
"""
import sys
import pygame
import random
import math
from constants import *
from spritesheet_functions import SpriteSheet

class PowerUp: #Class for Powerups
    def __init__(self, name, shape):
        self.name = name #Give powerup a name
        self.shape = shape #Specify the drawing of the powerup

class Bricka: #Class of the game
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512) #PreInitialize sound Mixer (reduces sound latency)
        pygame.mixer.init() #Initialize Sound Mixer
        pygame.init() #Initialize game system

        #Specify Sound files
        self.brick_pop_sound = pygame.mixer.Sound("PopSound.wav")
        self.paddle_sound = pygame.mixer.Sound("paddleHit.wav")

        #Specify Brick amounts
        self.xbrickNum = 9
        self.ybrickNum = 9

        #Create game screen
        self.screen = pygame.display.set_mode(SCREEN_SIZE)

        #Create Pygame Clock (time keeper / fps setter)
        self.clock = pygame.time.Clock()

        #setting up fonts
        if pygame.font:
            self.font = pygame.font.Font(None,30)
        else:
            self.font = None

        #Run Method init_game
        self.init_game()


    def init_game(self):
        sprite_sheet = SpriteSheet("tiles_spritesheet.png")


        #set lives state and score
        self.lives = 3
        self.score = 0
        self.state = STATE_BALL_IN_PADDLE
        self.double_chance = .0
        self.power_chance = .2
        self.start_message = ""
        self.ball_speed = BALL_SPEED

        #create paddle, ball, collision object
        self.paddle   = pygame.Rect(300,PADDLE_Y,PADDLE_WIDTH,PADDLE_HEIGHT)
        self.ball     = pygame.Rect(300,PADDLE_Y - BALL_DIAMETER,BALL_DIAMETER,BALL_DIAMETER)

        #Create banner to be behind text for readability
        self.banner   = pygame.Rect(0, SCREEN_SIZE[1]/2 - BANNER_HEIGHT/2, SCREEN_SIZE[0], BANNER_HEIGHT)

        #Create sprite for paddle
        self.image = pygame.transform.scale(sprite_sheet.get_image(504, 504, 70, 40), (self.paddle.width, self.paddle.height))

        #Set starting angle, velocity, and setup powerups
        theta = random.random()*math.pi*(90.)/180. + math.pi*45./180.
        self.ball_vel = [self.ball_speed*math.cos(theta), self.ball_speed*-math.sin(theta)]
        self.ball_left = float(self.ball.left) #save float versions of ball location
        self.ball_top = float(self.ball.top) #save float versions of ball location
        self.ball_vel_orig = [self.ball_speed*math.cos(theta), self.ball_speed*-math.sin(theta)] #Save initial velocity
        self.pows = [] #list of PowerUp instances
        self.powtypes = ['fire', 'grow', 'shrink', 'airbounce','speedup', 'slowdown'] # list of powerup types
        self.powdict = {'fire':FIREBLAZE,'grow':GROW, 'shrink':SHRINK, 'airbounce':AIRBOUNCE, 'speedup':SPEEDUP, 'slowdown': SLOWDOWN} #Dictionary for powerups their shape and their colors
        self.totfiretime = 250 #50 frames a second, so 5 seconds
        self.totgrowtime = 400 #8 seconds
        self.totshrinktime = 400 #8 seconds
        self.totspeeduptime = 350 #7 seconds
        self.totslowdowntime = 350 #7 seconds
        self.create_bricks() #Run create_bricks method


    def create_bricks(self):
        #determine brick dimensions
        self.BRICK_WIDTH = (SCREEN_SIZE[0] - 2*marginx - (self.xbrickNum-1) * xspacing)/self.xbrickNum
        self.BRICK_HEIGHT = (SCREEN_SIZE[1] - 2*marginy - (self.ybrickNum-1) * yspacing - bottom_to_brick)/self.ybrickNum
        y_ofs = marginy #Offset bricks from ceiling
        self.bricks = [] #Initialize list of bricks
        self.doublebricks = [] #Initialize list of doublebricks
        for i in range(self.ybrickNum): #iterate through each row of bricks
            x_ofs = marginx #offset bricks from wall
            for j in range(self.xbrickNum): #iterate through each column of bricks
                if random.random() > self.double_chance:
                    self.bricks.append(pygame.Rect(x_ofs,y_ofs,self.BRICK_WIDTH,self.BRICK_HEIGHT)) #Add rectangle to brick list
                else:
                    self.doublebricks.append(pygame.Rect(x_ofs,y_ofs,self.BRICK_WIDTH,self.BRICK_HEIGHT))
                x_ofs += self.BRICK_WIDTH + xspacing # add to offset from wall
            y_ofs += self.BRICK_HEIGHT + yspacing #add to offset from ceiling

    def draw_bricks(self): #Draw bricks function
        for brick in self.bricks: #For each brick draw a brick
            pygame.draw.rect(self.screen, BRICK_COLOR, brick)
        for doublebrick in self.doublebricks:
            pygame.draw.rect(self.screen, DOUBLEBRICK_COLOR, doublebrick)

    def draw_Pow(self): #draw powerups
        for power_up in self.pows: #for each powerup get name, color, and shape and draw it.
            powcolor = self.powdict.get(power_up.name)
            pygame.draw.rect(self.screen, powcolor, power_up.shape)

    def check_input(self): #Check user inputs
        keys = pygame.key.get_pressed() #dictionary of pressed keys

        if keys[pygame.K_LEFT]: #if left pressed, move paddle left
            self.paddle.left -= PADDLE_SPEED
            if self.paddle.left < 0:
                self.paddle.left = 0

        if keys[pygame.K_RIGHT]: #if right pressed, move paddle right
            self.paddle.left += PADDLE_SPEED
            if self.paddle.left > MAX_PADDLE_X:
                self.paddle.left = MAX_PADDLE_X

        if self.airbounce and keys[pygame.K_SPACE] and self.state == STATE_PLAYING:
            self.airbounce = 0
            self.ball_vel[1] = -abs(self.ball_vel[1])

        if keys[pygame.K_SPACE] and self.state == STATE_BALL_IN_PADDLE: #if space pressed when ball is in paddle, release ball.
            self.ball_vel = self.ball_vel_orig
            self.state = STATE_PLAYING
        elif keys[pygame.K_RETURN] and (self.state == STATE_GAME_OVER): #restart game
            self.init_game()
        elif keys[pygame.K_RETURN] and self.state == STATE_WON: # if win, quit game and return True
            pygame.quit()
            return True

    def move_pow(self): #move all powerups down the screen
        for power_up in self.pows:
            power_up.shape.top += POW_FALL_SPD
            if power_up.shape.top > float(MAX_BALL_Y+30): #added 30 here to make sure powerups go offsceen before deleting
                self.pows.remove(power_up)


    def move_ball(self): #Move the ball
        #print(type(self.ball))

        #Keep the old values of the ball location and update new values (double versions)
        self.ball_top_old = self.ball_top
        self.ball_left_old = self.ball_left
        self.ball_left += self.ball_vel[0]
        self.ball_top += self.ball_vel[1]

        #Check if ball hits any walls.
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

        #Use double values to update int values (this allows for double precision ball movements)
        self.ball.left = int(self.ball_left)
        self.ball.top  = int(self.ball_top)

    def handle_collisions(self): # Function for Collision Handling
        for brick in self.bricks: #Did ball collide with brick for each brick?
            if self.ball.colliderect(brick): #If collided with brick
                self.brick_pop_sound.play() #Play brick pop sound
                #print(brick.topright)
                self.score += 5 # Add to score
                if self.fireball == False: #If not fireball then collide
                    if self.ball_left < brick.right and self.ball_left_old > brick.right: #Collisions on right of brick
                        self.ball_vel[0] = abs(self.ball_vel[0])
                    elif self.ball_left+BALL_DIAMETER > brick.left and self.ball_left_old+BALL_DIAMETER < brick.left: #Collisions on left of brick
                        self.ball_vel[0] = -abs(self.ball_vel[0])
                    else: #Vertical Collisions
                        self.ball_vel[1] = -self.ball_vel[1]
                self.bricks.remove(brick) #Remove brick
                if random.random() < self.power_chance: #Have chance of dropping Powerup
                    #create powshape and location to drop from
                    powshape = pygame.Rect(brick.centerx - POWER_WIDTH/2,brick.centery- POWER_HEIGHT/2,POWER_WIDTH,POWER_HEIGHT)
                    #Chooses random powerup and drops with powshape
                    self.pows.append(PowerUp(random.choice(self.powtypes),powshape))
                break
        for dbrick in self.doublebricks: #Did ball collide with dbrick for each dbrick?
            if self.ball.colliderect(dbrick): #If collided with dbrick
                self.brick_pop_sound.play() #Play brick pop sound
                #print(brick.topright)
                self.score += 3 # Add to score
                if self.ball_left < dbrick.right and self.ball_left_old > dbrick.right: #Collisions on right of brick
                    self.ball_vel[0] = abs(self.ball_vel[0])
                elif self.ball_left+BALL_DIAMETER > dbrick.left and self.ball_left_old+BALL_DIAMETER < dbrick.left: #Collisions on left of brick
                    self.ball_vel[0] = -abs(self.ball_vel[0])
                else: #Vertical Collisions
                    self.ball_vel[1] = -self.ball_vel[1]
                self.doublebricks.remove(dbrick) #Remove brick
                self.bricks.append(dbrick)
                break

        if len(self.bricks + self.doublebricks) == 0: #if no bricks, then win
            self.state = STATE_WON
        for power_up in self.pows: #for each powerup
            if power_up.shape.colliderect(self.paddle): #check if collide with paddle
                if power_up.name == 'fire': #Check each powerup
                    self.fireball = True
                    self.firetime = 0
                if power_up.name == 'grow':
                    self.grow = True
                    self.growtime = 0
                if power_up.name == 'shrink':
                    self.shrink = True
                    self.shrinktime = 0
                if power_up.name == 'airbounce':
                    self.airbounce = True
                if power_up.name == 'speedup':
                    self.speedup = True
                    self.speeduptime = 0
                    self.ball_speed = BALL_SPEEDUP
                    #theta = math.atan2(self.ball_vel[1], self.ball_vel[0])
                    self.ball_vel[0] *= BALL_SPEEDUP/BALL_SPEED
                    self.ball_vel[1] *= BALL_SPEEDUP/BALL_SPEED
                if power_up.name == 'slowdown':
                    self.slowdown = True
                    self.slowdowntime = 0
                    self.ball_speed = BALL_SLOWDOWN
                    #theta = math.atan2(self.ball_vel[1], self.ball_vel[0])
                    self.ball_vel[0] *= BALL_SLOWDOWN/BALL_SPEED
                    self.ball_vel[1] *= BALL_SLOWDOWN/BALL_SPEED
                self.pows.remove(power_up) #Remove powerup from existing powerups
        if self.ball.colliderect(self.paddle): #if ball collide with paddle
            self.paddle_sound.play() #Play paddle sound
            self.ball.top = PADDLE_Y - BALL_DIAMETER #Put ball on top of paddle
            balltopad = float(self.paddle.right - self.ball.center[0])/float(self.paddle.right - self.paddle.left) #check ball location in relation to paddle
            theta = balltopad*math.pi*(90)/180 + math.pi*(45)/180 #Make ball move off paddle based on location relative to paddle.
            self.ball_vel = [self.ball_speed*math.cos(theta), self.ball_speed*-math.sin(theta)] #set new ball trajectory
        elif self.ball.top > self.paddle.top: #if ball is under paddle
            self.lives -= 1 #Remove life
            if self.lives > 0: #if still has lives, reset ball on paddle
                self.state = STATE_BALL_IN_PADDLE
            else:
                self.state = STATE_GAME_OVER #End game

    def show_stats(self): #Show states at top of screen
        if self.font:
            font_surface = self.font.render("SCORE: " + str(self.score) + " LIVES: " + str(self.lives), False, WHITE) #Specify text
            self.screen.blit(font_surface, (205,5)) #put on screen

    def show_message(self,message): #Show message on screen
        if self.font:
            size = self.font.size(message) #use message font size
            font_surface = self.font.render(message,False, TEXT) #make font surface
            # Put font in center of screen
            x = (SCREEN_SIZE[0] - size[0]) / 2
            y = (SCREEN_SIZE[1] - size[1]) / 2
            pygame.draw.rect(self.screen, BLACK, self.banner) #place banner on screen
            self.screen.blit(font_surface, (x,y)) #Place on screen


    def run(self):
        # Set all powerup effects to 0
        self.fireball = 0
        self.firetime = 0
        self.grow = 0
        self.growtime = 0
        self.shrink = 0
        self.shrinktime = 0
        self.airbounce = 0
        self.speedup = 0
        self.speeduptime = 0
        self.slowdown = 0
        self.slowdowntime = 0

        # Set Start Message Params
        self.start_message_time = 200
        self.start_time = 0
        while 1: #While true
            self.start_time+=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #check if game is quit
                    pygame.quit() #quit the game
                    return None
            self.clock.tick(50) #set fps to 50
            self.screen.fill(BLACK) #fill background with black
            done = self.check_input() #check if game is done
            if done:
                return None #end game
            if self.grow and self.shrink: #if grow and shrink at same time, set back to normal
                self.growtime = 999
                self.shrinktime = 999
            elif self.grow: #grow power
                self.paddle.width = GROW_PADDLE
            elif self.shrink: #shrink power
                self.paddle.width = SHRINK_PADDLE
            if self.speedup and self.slowdown:
                self.speeduptime = self.totspeeduptime
                self.slowdowntime = self.totslowdowntime

            if self.state == STATE_PLAYING: #if playing run play functions
                self.move_ball()
                self.move_pow()
                self.handle_collisions()
            elif self.state == STATE_BALL_IN_PADDLE: #if ball in paddle move ball on paddle
                self.ball_top_old = self.ball_top
                self.ball_left_old = self.ball_left
                self.ball_left = float(self.paddle.left + self.paddle.width / 2)
                self.ball_top  = float(self.paddle.top - self.ball.height)
                self.ball.left = self.ball_left
                self.ball.top = self.ball_top

            self.draw_bricks() # draw bricks
            self.draw_Pow() #draw powerups
            #draw vector of ball and projections of vector onto sides of screen
            pygame.draw.line(self.screen, FIREBLAZE, (self.ball.center[0], self.ball.center[1]), (self.ball.center[0] + self.ball_vel[0]*3, self.ball.center[1]+self.ball_vel[1]*3), 4)
            pygame.draw.line(self.screen, AIRBOUNCE, (self.ball.center[0], SCREEN_SIZE[1]-20), (self.ball.center[0]+self.ball_vel[0]*3, SCREEN_SIZE[1]-20), 4)
            pygame.draw.line(self.screen, AIRBOUNCE, (SCREEN_SIZE[0]-20, self.ball.center[1]), (SCREEN_SIZE[0]-20, self.ball.center[1]+self.ball_vel[1]*3), 4)
            self.screen.blit(self.image, (self.paddle.left,self.paddle.top))

            # Draw paddle
            #pygame.draw.rect(self.screen, BLUE, self.paddle)

            # Draw ball (check for fireball powerup)
            if self.fireball == 0:
                pygame.draw.circle(self.screen, WHITE, (self.ball.left + BALL_RADIUS, self.ball.top + BALL_RADIUS), BALL_RADIUS)
            else:
                pygame.draw.circle(self.screen, FIREBLAZE, (self.ball.left + BALL_RADIUS, self.ball.top + BALL_RADIUS), BALL_RADIUS)
                pygame.draw.circle(self.screen, FIREAFTER, (int(self.ball_left_old) + BALL_RADIUS, int(self.ball_top_old)+ BALL_RADIUS), int(BALL_RADIUS/1.35))
            self.show_stats()
            #self.fireball = True

            #check all powerup attributes and update them as necessary
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
            if self.speedup and self.speeduptime < self.totspeeduptime:
                self.speeduptime += 1
            else:
                self.speeduptime = 0
                self.speedup = False
            if self.slowdown and self.slowdowntime < self.totslowdowntime:
                self.slowdowntime += 1
            else:
                self.slowdowntime = 0
                self.slowdown = False
            if not (self.speedup or self.slowdown):
                self.ball_speed = BALL_SPEED
                theta = math.atan2(self.ball_vel[1],self.ball_vel[0])
                self.ball_vel = [self.ball_speed*math.cos(theta), self.ball_speed*math.sin(theta)]



            #Update Screen Message
            if self.state == STATE_BALL_IN_PADDLE:
                if self.start_time < self.start_message_time:
                    self.show_message(self.start_message)
                else:
                    self.show_message("PRESS SPACE TO LAUNCH THE BALL")
            elif self.state == STATE_GAME_OVER:
                self.show_message("GAME OVER. PRESS ENTER TO PLAY AGAIN")
            elif self.state == STATE_WON:
                self.show_message("YOU WON! PRESS ENTER FOR THE NEXT LEVEL")
            pygame.display.flip()

if __name__ == "__main__":
    Bricka().run()
