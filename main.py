import pygame
import sys
pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
FPS = 20
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ADD_NEW_FLAME_RATE = 25
cactus_img = pygame.image.load('cactus_bricks.png')
cactus_img_rect = cactus_img.get_rect()
cactus_img_rect.left = 0
fire_img = pygame.image.load('fire_bricks.png')
fire_img_rect = fire_img.get_rect()
fire_img_rect.left = 0
CLOCK = pygame.time.Clock()
font = pygame.font.SysFont('forte', 20)

canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Mario')


class Topscore:
    def __init__(self):
        self.high_score = 0
    def top_score(self, score):
        if score > self.high_score:
            self.high_score = score
        return self.high_score

topscore = Topscore()


class Dragon:
    dragon_velocity = 10

    def __init__(self):
        self.dragon_img = pygame.image.load('dragon.png')
        self.dragon_img_rect = self.dragon_img.get_rect()
        self.dragon_img_rect.width -= 10
        self.dragon_img_rect.height -= 10
        self.dragon_img_rect.top = WINDOW_HEIGHT/2
        self.dragon_img_rect.right = WINDOW_WIDTH
        self.up = True
        self.down = False

    def update(self):
        canvas.blit(self.dragon_img, self.dragon_img_rect)
        if self.dragon_img_rect.top <= cactus_img_rect.bottom:
            self.up = False
            self.down = True
        elif self.dragon_img_rect.bottom >= fire_img_rect.top:
            self.up = True
            self.down = False

        if self.up:
            self.dragon_img_rect.top -= self.dragon_velocity
        elif self.down:
            self.dragon_img_rect.top += self.dragon_velocity


class Flames:
    flames_velocity = 20

    def __init__(self):
        self.flames = pygame.image.load('fireball.png')
        self.flames_img = pygame.transform.scale(self.flames, (20, 20))
        self.flames_img_rect = self.flames_img.get_rect()
        self.flames_img_rect.right = dragon.dragon_img_rect.left
        self.flames_img_rect.top = dragon.dragon_img_rect.top + 30


    def update(self):
        canvas.blit(self.flames_img, self.flames_img_rect)

        if self.flames_img_rect.left > 0:
            self.flames_img_rect.left -= self.flames_velocity


class Mario:
    velocity = 10

    def __init__(self):
        self.mario_img = pygame.image.load('maryo.png')
        self.mario_img_rect = self.mario_img.get_rect()
        self.mario_img_rect.left = 20
        self.mario_img_rect.top = WINDOW_HEIGHT/2 - 100
        self.down = True
        self.up = False

    def update(self):
        canvas.blit(self.mario_img, self.mario_img_rect)
        if self.mario_img_rect.top <= cactus_img_rect.bottom:
            game_over()
            if SCORE > self.mario_score:
                self.mario_score = SCORE
        if self.mario_img_rect.bottom >= fire_img_rect.top:
            game_over()
            if SCORE > self.mario_score:
                self.mario_score = SCORE
        if self.up:
            self.mario_img_rect.top -= 10
        if self.down:
            self.mario_img_rect.bottom += 10


def game_over():
    pygame.mixer.music.stop()
    music = pygame.mixer.Sound('mario_dies.wav')
    music.play()
    topscore.top_score(SCORE)
    game_over_img = pygame.image.load('end.png')
    game_over_img_rect = game_over_img.get_rect()
    game_over_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    canvas.blit(game_over_img, game_over_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                music.stop()
                game_loop()
        pygame.display.update()


def start_game():
    canvas.fill(BLACK)
    start_img = pygame.image.load('start.png')
    start_img_rect = start_img.get_rect()
    start_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    canvas.blit(start_img, start_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                game_loop()
        pygame.display.update()


def check_level(SCORE):
    global LEVEL
    if SCORE in range(0, 10):
        cactus_img_rect.bottom = 50
        fire_img_rect.top = WINDOW_HEIGHT - 50
        LEVEL = 1
    elif SCORE in range(10, 20):
        cactus_img_rect.bottom = 100
        fire_img_rect.top = WINDOW_HEIGHT - 100
        LEVEL = 2
    elif SCORE in range(20, 30):
        cactus_img_rect.bottom = 150
        fire_img_rect.top = WINDOW_HEIGHT - 150
        LEVEL = 3
    elif SCORE > 30:
        cactus_img_rect.bottom = 200
        fire_img_rect.top = WINDOW_HEIGHT - 200
        LEVEL = 4





def game_loop():
    while True:
        global dragon
        dragon = Dragon()
        flames = Flames()
        mario = Mario()
        add_new_flame_counter = 0
        global SCORE
        SCORE = 0
        global  HIGH_SCORE
        flames_list = []
        pygame.mixer.music.load('mario_theme.wav')
        pygame.mixer.music.play(-1, 0.0)
        while True:
            canvas.fill(BLACK)
            check_level(SCORE)
            dragon.update()
            add_new_flame_counter += 1

            if add_new_flame_counter == ADD_NEW_FLAME_RATE:
                add_new_flame_counter = 0
                new_flame = Flames()
                flames_list.append(new_flame)
            for f in flames_list:
                if f.flames_img_rect.left <= 0:
                    flames_list.remove(f)
                    SCORE += 1
                f.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        mario.up = True
                        mario.down = False
                    elif event.key == pygame.K_DOWN:
                        mario.down = True
                        mario.up = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        mario.up = False
                        mario.down = True
                    elif event.key == pygame.K_DOWN:
                        mario.down = True
                        mario.up = False

            score_font = font.render('Score:'+str(SCORE), True, GREEN)
            score_font_rect = score_font.get_rect()
            score_font_rect.center = (200, cactus_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(score_font, score_font_rect)

            level_font = font.render('Level:'+str(LEVEL), True, GREEN)
            level_font_rect = level_font.get_rect()
            level_font_rect.center = (500, cactus_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(level_font, level_font_rect)

            top_score_font = font.render('Top Score:'+str(topscore.high_score),True,GREEN)
            top_score_font_rect = top_score_font.get_rect()
            top_score_font_rect.center = (800, cactus_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(top_score_font, top_score_font_rect)

            canvas.blit(cactus_img, cactus_img_rect)
            canvas.blit(fire_img, fire_img_rect)
            mario.update()
            for f in flames_list:
                if f.flames_img_rect.colliderect(mario.mario_img_rect):
                    game_over()
                    if SCORE > mario.mario_score:
                        mario.mario_score = SCORE
            pygame.display.update()
            CLOCK.tick(FPS)


start_game()


# Import modules

import pygame, random, sys
from pygame.locals import *

pygame.init()

# intialising variables for ease

window_height = 600
window_width = 1200

blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)

fps = 25
level = 0
addnewflamerate = 20

# defining the required function


class dragon:

    global firerect, imagerect, Canvas
    up = False
    down = True
    velocity = 15
    
    def __init__(self):
        self.image = load_image('dragon.png')
        self.imagerect = self.image.get_rect()
        self.imagerect.right = window_width
        self.imagerect.top = window_height/2

    def update(self):
        
        if self.imagerect.top < cactusrect.bottom:
            self.up = False
            self.down = True

        if self.imagerect.bottom > firerect.top:
            self.up = True
            self.down = False
            
        if self.down:
            self.imagerect.bottom += self.velocity

        if self.up:
            self.imagerect.top -= self.velocity

        Canvas.blit(self.image, self.imagerect)

    def return_height(self):

        h = self.imagerect.top
        return h

class flames:
    flamespeed = 20

    def __init__(self):
        self.image = load_image('fireball.png')
        self.imagerect = self.image.get_rect()
        self.height = Dragon.return_height() + 20
        self.surface = pygame.transform.scale(self.image, (20, 20))
        self.imagerect = pygame.Rect(window_width - 106, self.height, 20, 20)

    def update(self):
            self.imagerect.left -= self.flamespeed

    def collision(self):
        if self.imagerect.left == 0:
            return True
        else:
            return False

class maryo:
    global moveup, movedown, gravity, cactusrect, firerect
    speed = 10
    downspeed = 20

    def __init__(self):
        self.image = load_image('maryo.png')
        self.imagerect = self.image.get_rect()
        self.imagerect.topleft = (50, window_height/2)
        self.score = 0

    def update(self):
        
        if moveup and self.imagerect.top > cactusrect.bottom:
            self.imagerect.top -= self.speed
            self.score += 1
            
        if movedown and self.imagerect.bottom < firerect.top:
            self.imagerect.bottom += self.downspeed
            self.score += 1
            
        if gravity and self.imagerect.bottom < firerect.top:
            self.imagerect.bottom += self.speed


def terminate():        # to end the program
    pygame.quit()
    sys.exit()

def waitforkey():
    while True :                                        # to wait for user to start
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:     # to terminate if the user presses the escape key
                if event.key == pygame.K_ESCAPE:
                    terminate()
                return


def flamehitsmario(playerrect, flames):      # to check if flame has hit mario or not
    for f in flame_list:
        if playerrect.colliderect(f.imagerect):
            return True
        return False


def drawtext(text, font, surface, x, y):        # to display text on the screen
    textobj = font.render(text, 1, white)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)


def check_level(score):
    global window_height, level, cactusrect, firerect
    if score in range(0, 250):
        firerect.top = window_height - 50
        cactusrect.bottom = 50
        level = 1
    elif score in range(250, 500):
        firerect.top = window_height - 100
        cactusrect.bottom = 100
        level = 2
    elif score in range(500, 750):
        level = 3
        firerect.top = window_height-150
        cactusrect.bottom = 150
    elif score in range(750, 1000):
        level = 4
        firerect.top = window_height - 200
        cactusrect.bottom = 200


def load_image(imagename):
    return pygame.image.load(imagename)

# end of functions, begin to start the main code


mainClock = pygame.time.Clock()
Canvas = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('MARYO')

# setting up font and sounds and images

font = pygame.font.SysFont(None, 48)
scorefont = pygame.font.SysFont(None, 30)

fireimage = load_image('fire_bricks.png')
firerect = fireimage.get_rect()

cactusimage = load_image('cactus_bricks.png')
cactusrect = cactusimage.get_rect()

startimage = load_image('start.png')
startimagerect = startimage.get_rect()
startimagerect.centerx = window_width/2
startimagerect.centery = window_height/2

endimage = load_image('end.png')
endimagerect = startimage.get_rect()
endimagerect.centerx = window_width/2
endimagerect.centery = window_height/2

pygame.mixer.music.load('mario_theme.wav')
gameover = pygame.mixer.Sound('mario_dies.wav')

# getting to the start screen

drawtext('Mario', font, Canvas, (window_width/3), (window_height/3))
Canvas.blit(startimage, startimagerect)

pygame.display.update()
waitforkey()

# start for the main code

topscore = 0
Dragon = dragon()

while True:

    flame_list = []
    player = maryo()
    moveup = movedown = gravity = False
    flameaddcounter = 0

    gameover.stop()
    pygame.mixer.music.play(-1, 0.0)

    while True:     # the main game loop
        
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                
                if event.key == K_UP:
                    movedown = False
                    moveup = True
                    gravity = False

                if event.key == K_DOWN:
                    movedown = True
                    moveup = False
                    gravity = False

            if event.type == KEYUP:

                if event.key == K_UP:
                    moveup = False
                    gravity = True
                if event.key == K_DOWN:
                    movedown = False
                    gravity = True
                    
                if event.key == K_ESCAPE:
                    terminate()

        flameaddcounter += 1
        check_level(player.score)
        
        if flameaddcounter == addnewflamerate:

            flameaddcounter = 0
            newflame = flames()
            flame_list.append(newflame)

        for f in flame_list:
            flames.update(f)

        for f in flame_list:
            if f.imagerect.left <= 0:
                flame_list.remove(f)

        player.update()
        Dragon.update()

        Canvas.fill(black)
        Canvas.blit(fireimage, firerect)
        Canvas.blit(cactusimage, cactusrect)
        Canvas.blit(player.image, player.imagerect)
        Canvas.blit(Dragon.image, Dragon.imagerect)

        drawtext('Score : %s | Top score : %s | Level : %s' % (player.score, topscore, level), scorefont, Canvas, 350, cactusrect.bottom + 10)
        
        for f in flame_list:
            Canvas.blit(f.surface, f.imagerect)

        if flamehitsmario(player.imagerect, flame_list):
            if player.score > topscore:
                topscore = player.score
            break
        
        if player.imagerect.top <= cactusrect.bottom or player.imagerect.bottom >= firerect.top:
            if player.score > topscore:
                topscore = player.score
            break

        pygame.display.update()

        mainClock.tick(fps)
    
    pygame.mixer.music.stop()
    gameover.play()
    Canvas.blit(endimage, endimagerect)
    pygame.display.update()
    waitforkey()
import pygame
import sys
pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
FPS = 20
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ADD_NEW_FLAME_RATE = 25
cactus_img = pygame.image.load('cactus_bricks.png')
cactus_img_rect = cactus_img.get_rect()
cactus_img_rect.left = 0
fire_img = pygame.image.load('fire_bricks.png')
fire_img_rect = fire_img.get_rect()
fire_img_rect.left = 0
CLOCK = pygame.time.Clock()
font = pygame.font.SysFont('forte', 20)

canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Mario')


class Topscore:
    def __init__(self):
        self.high_score = 0
    def top_score(self, score):
        if score > self.high_score:
            self.high_score = score
        return self.high_score

topscore = Topscore()


class Dragon:
    dragon_velocity = 10

    def __init__(self):
        self.dragon_img = pygame.image.load('dragon.png')
        self.dragon_img_rect = self.dragon_img.get_rect()
        self.dragon_img_rect.width -= 10
        self.dragon_img_rect.height -= 10
        self.dragon_img_rect.top = WINDOW_HEIGHT/2
        self.dragon_img_rect.right = WINDOW_WIDTH
        self.up = True
        self.down = False

    def update(self):
        canvas.blit(self.dragon_img, self.dragon_img_rect)
        if self.dragon_img_rect.top <= cactus_img_rect.bottom:
            self.up = False
            self.down = True
        elif self.dragon_img_rect.bottom >= fire_img_rect.top:
            self.up = True
            self.down = False

        if self.up:
            self.dragon_img_rect.top -= self.dragon_velocity
        elif self.down:
            self.dragon_img_rect.top += self.dragon_velocity


class Flames:
    flames_velocity = 20

    def __init__(self):
        self.flames = pygame.image.load('fireball.png')
        self.flames_img = pygame.transform.scale(self.flames, (20, 20))
        self.flames_img_rect = self.flames_img.get_rect()
        self.flames_img_rect.right = dragon.dragon_img_rect.left
        self.flames_img_rect.top = dragon.dragon_img_rect.top + 30


    def update(self):
        canvas.blit(self.flames_img, self.flames_img_rect)

        if self.flames_img_rect.left > 0:
            self.flames_img_rect.left -= self.flames_velocity


class Mario:
    velocity = 10

    def __init__(self):
        self.mario_img = pygame.image.load('maryo.png')
        self.mario_img_rect = self.mario_img.get_rect()
        self.mario_img_rect.left = 20
        self.mario_img_rect.top = WINDOW_HEIGHT/2 - 100
        self.down = True
        self.up = False

    def update(self):
        canvas.blit(self.mario_img, self.mario_img_rect)
        if self.mario_img_rect.top <= cactus_img_rect.bottom:
            game_over()
            if SCORE > self.mario_score:
                self.mario_score = SCORE
        if self.mario_img_rect.bottom >= fire_img_rect.top:
            game_over()
            if SCORE > self.mario_score:
                self.mario_score = SCORE
        if self.up:
            self.mario_img_rect.top -= 10
        if self.down:
            self.mario_img_rect.bottom += 10


def game_over():
    pygame.mixer.music.stop()
    music = pygame.mixer.Sound('mario_dies.wav')
    music.play()
    topscore.top_score(SCORE)
    game_over_img = pygame.image.load('end.png')
    game_over_img_rect = game_over_img.get_rect()
    game_over_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    canvas.blit(game_over_img, game_over_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                music.stop()
                game_loop()
        pygame.display.update()


def start_game():
    canvas.fill(BLACK)
    start_img = pygame.image.load('start.png')
    start_img_rect = start_img.get_rect()
    start_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    canvas.blit(start_img, start_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                game_loop()
        pygame.display.update()


def check_level(SCORE):
    global LEVEL
    if SCORE in range(0, 10):
        cactus_img_rect.bottom = 50
        fire_img_rect.top = WINDOW_HEIGHT - 50
        LEVEL = 1
    elif SCORE in range(10, 20):
        cactus_img_rect.bottom = 100
        fire_img_rect.top = WINDOW_HEIGHT - 100
        LEVEL = 2
    elif SCORE in range(20, 30):
        cactus_img_rect.bottom = 150
        fire_img_rect.top = WINDOW_HEIGHT - 150
        LEVEL = 3
    elif SCORE > 30:
        cactus_img_rect.bottom = 200
        fire_img_rect.top = WINDOW_HEIGHT - 200
        LEVEL = 4





def game_loop():
    while True:
        global dragon
        dragon = Dragon()
        flames = Flames()
        mario = Mario()
        add_new_flame_counter = 0
        global SCORE
        SCORE = 0
        global  HIGH_SCORE
        flames_list = []
        pygame.mixer.music.load('mario_theme.wav')
        pygame.mixer.music.play(-1, 0.0)
        while True:
            canvas.fill(BLACK)
            check_level(SCORE)
            dragon.update()
            add_new_flame_counter += 1

            if add_new_flame_counter == ADD_NEW_FLAME_RATE:
                add_new_flame_counter = 0
                new_flame = Flames()
                flames_list.append(new_flame)
            for f in flames_list:
                if f.flames_img_rect.left <= 0:
                    flames_list.remove(f)
                    SCORE += 1
                f.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        mario.up = True
                        mario.down = False
                    elif event.key == pygame.K_DOWN:
                        mario.down = True
                        mario.up = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        mario.up = False
                        mario.down = True
                    elif event.key == pygame.K_DOWN:
                        mario.down = True
                        mario.up = False

            score_font = font.render('Score:'+str(SCORE), True, GREEN)
            score_font_rect = score_font.get_rect()
            score_font_rect.center = (200, cactus_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(score_font, score_font_rect)

            level_font = font.render('Level:'+str(LEVEL), True, GREEN)
            level_font_rect = level_font.get_rect()
            level_font_rect.center = (500, cactus_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(level_font, level_font_rect)

            top_score_font = font.render('Top Score:'+str(topscore.high_score),True,GREEN)
            top_score_font_rect = top_score_font.get_rect()
            top_score_font_rect.center = (800, cactus_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(top_score_font, top_score_font_rect)

            canvas.blit(cactus_img, cactus_img_rect)
            canvas.blit(fire_img, fire_img_rect)
            mario.update()
            for f in flames_list:
                if f.flames_img_rect.colliderect(mario.mario_img_rect):
                    game_over()
                    if SCORE > mario.mario_score:
                        mario.mario_score = SCORE
            pygame.display.update()
            CLOCK.tick(FPS)


start_game()


