# font form https://www.dafont.com/babyblocks.font?text=Best+Score%3A
# idea form https://techwithtim.net/tutorials/game-development-with-python/

# import
import pygame
from pygame.locals import *
import os
import sys
import math
import random

# setup
pygame.init()

W, H = 800, 576
surface = pygame.display.set_mode((W,H))
pygame.display.set_caption('Corgi Run')
icon = pygame.image.load(os.path.join('images', 'dog1.png')).convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load(os.path.join('images', 'bg.png')).convert()
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()

# class and function
class dog(object):
    run = [pygame.image.load(os.path.join('images', 'dog_1.png')), pygame.image.load(os.path.join('images', 'dog_2.png'))]
    fall = run
    jumpList = [3]*60 + [0]*10  + [-3]*60
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.falling = False
        self.jumpCount = 0
        self.runCount = 0

    def draw(self, surface):
        if self.runCount > 39:
                self.runCount = 0
        if self.falling:
            surface.blit(self.fall[self.runCount//20], (self.x, self.y))
                
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.
            surface.blit(self.run[self.runCount//20], (self.x,self.y))
            self.jumpCount += 1
            if self.jumpCount >= 130:
                self.jumpCount = 0
                self.jumping = False
        else:
            surface.blit(self.run[self.runCount//20], (self.x,self.y))
            self.runCount += 1
        self.hitbox = (self.x, self.y, self.width - 3, self.height - 3)

        # pygame.draw.rect(surface, (255,0,0), self.hitbox, 2)

class tr33(object):
    tr33 = pygame.image.load(os.path.join('images', 'tr33.png'))
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, surface):
        self.hitbox = (self.x + 3, self.y + 5, self.width - 5, self.height - 5)
        surface.blit(pygame.transform.scale(self.tr33, (60,92)), (self.x,self.y))
        # pygame.draw.rect(surface, (255,0,0), self.hitbox, 2)

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False

class tr33s(tr33):
    img = pygame.image.load(os.path.join('images', 'tr33s.png'))
    def draw(self,surface):
        self.hitbox = (self.x, self.y, self.width - 3, self.height - 3)
        surface.blit(pygame.transform.scale(self.img, (56,76)), (self.x,self.y))
        # pygame.draw.rect(surface, (255,0,0), self.hitbox, 2)

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False

class Button(object):
    def __init__(self, image, x, y):
        self.image = pygame.image.load(os.path.join('images', image)).convert_alpha()
        self.x = x
        self.y = y
        self.w = self.image.get_width()
        self.h = self.image.get_height()

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def triggered(self, mouse):
        if (self.x + self.w > mouse[0] > self.x) and (self.y + self.h > mouse[1] > self.y):
            return True
        return False

def updateFile():
    f = open('scores.txt','r')
    file = f.readlines()
    try:
        last = int(file[0])
    except IndexError:
        last = 0
    
    if last < int(score):
        f.close()
        file = open('scores.txt', 'w')
        file.write(str(score))
        file.close()

        return score
               
    return last

def endScreen():
    global score, obstacles, bgX, bgX2
    menu = Button('menu.png', 50, 400)
    restart = Button('restart.png', 275, 400)
    exit = Button('exit.png', 575, 400)
    obstacles = []

    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if restart.triggered(mouse):
                    GameLoop()
                    
                if exit.triggered(mouse):
                    pygame.quit()
                    quit()
                    
                if menu.triggered(mouse):
                    MenuLoop()
                
        surface.blit(bg, (bgX, 0))
        surface.blit(bg, (bgX2,0))
        largeFont = pygame.font.Font(os.path.join('baby-blocks.ttf'), 72)
        lastScore = largeFont.render('highest score: ' + str(updateFile()), 1, (0,0,102))
        currentScore = largeFont.render('your score: '+ str(score), 1, (0,0,102))
        surface.blit(lastScore, (W/2 - lastScore.get_width()/2,150))
        surface.blit(currentScore, (W/2 - currentScore.get_width()/2, 240))
        menu.draw(surface)
        restart.draw(surface)
        exit.draw(surface)
        pygame.display.update()
        
def Scoring():
    global W, played, start, how_to, exit
    largeFont = pygame.font.Font(os.path.join('baby-blocks.ttf'), 22)
    surface.blit(bg, (bgX, 0))
    surface.blit(bg, (bgX2,0))
    text = largeFont.render('score: ' + str(score), 1, (0,0,102))
    surface.blit(text, (0, 0))
    runner.draw(surface)
    for obstacle in obstacles:
        obstacle.draw(surface)
    pygame.display.update()

def GameLoop():
    global runner, score, obstacles, bg, bgX, bgX2, speed
    pygame.time.set_timer(USEREVENT+1, 500)
    pygame.time.set_timer(USEREVENT+2, 3000)
    speed = 60
    score = 0

    run = True
    runner = dog(150, 428, 78, 60)

    obstacles = []

    while run:
        for obstacle in obstacles:
            if obstacle.collide(runner.hitbox):
                endScreen()
            if obstacle.x < -64:
                obstacles.pop(obstacles.index(obstacle))
            else:
                obstacle.x -= 2.4
        
        bgX -= 2.4
        bgX2 -= 2.4

        if bgX < bg.get_width() * -1:
            bgX = bg.get_width()
        if bgX2 < bg.get_width() * -1:
            bgX2 = bg.get_width() 
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == USEREVENT+1:
                speed += 1
                
            if event.type == USEREVENT+2:
                r = random.randrange(0,2)
                if r == 0:
                    obstacles.append(tr33(700, 396, 60, 92))
                elif r == 1:
                    obstacles.append(tr33s(700, 412, 56, 76))
                    
        if runner.falling == False:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                if not(runner.jumping):
                    score += 1
                    runner.jumping = True
        clock.tick(speed)
        Scoring()

def how_to_menu():
    how = pygame.image.load(os.path.join('images', 'howto.png')).convert()
    surface.blit(how, (0,0))
    menu = Button('menu.png', 625, 500)
    while True:
        pygame.time.delay(100)
        menu.draw(surface)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()                        
                if menu.triggered(mouse):
                    MenuLoop()
                    
        pygame.display.update()

def MenuLoop():
    global bg, bgX2, bgX
    start = Button('start.png', 50, 400)
    how_to = Button('how2.png', 316, 400)
    exit = Button('exit.png', 625, 400)
    cg = Button('cg.png', 199, 125)
    while True:
        bgX -= 2.4
        bgX2 -= 2.4

        if bgX < bg.get_width() * -1:
            bgX = bg.get_width()
        if bgX2 < bg.get_width() * -1:
            bgX2 = bg.get_width() 
            
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if start.triggered(mouse):
                if click[0] == 1:
                    GameLoop()
                    
            if exit.triggered(mouse):
                if click[0] == 1:
                    pygame.quit()
                    quit()
                    

            if how_to.triggered(mouse):
                if click[0] == 1:
                    how_to_menu()
                    

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                

        surface.blit(bg, (bgX, 0))
        surface.blit(bg, (bgX2,0))
        start.draw(surface)
        how_to.draw(surface)
        exit.draw(surface)
        cg.draw(surface)
        pygame.display.update()
        clock.tick(60)

# start
MenuLoop()
pygame.quit()