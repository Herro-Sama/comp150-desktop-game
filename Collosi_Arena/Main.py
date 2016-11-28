##Test Arena##

import pygame
import sys
from pygame.locals import *
import time

ScreenWidth = 1024
ScreenHeight = 576
Black = (0,0,0)
Red = (255,0,0)
Green = (0,255,0)
Counter = 0

pygame.init()

Screen = pygame.display.set_mode((ScreenWidth,ScreenHeight),pygame.FULLSCREEN, 32)
pygame.display.set_caption('Collosi Arena')


class Sprite:
    def __init__(self):
        self.BackgroundImage = pygame.image.load('BackgroundScaled.jpg')

    def Update(self):
        Screen.blit(self.BackgroundImage, (0, 0))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.PosX = 100
        self.PosY = 440
        self.Health = 5
        self.PlayerSprite = pygame.image.load('PlayerStillScaled.PNG')
        self.Jumped = False
        self.player_rect = self.PlayerSprite.get_rect()
        self.floor = pygame.draw.rect(Screen, Green, (0, 546, 1024, 30))
        self.floor_rect = self.floor

    def Update(self):
        self.player_rect = self.PlayerSprite.get_rect()
        Screen.blit(self.PlayerSprite, (self.PosX, self.PosY))
        self.floor = pygame.draw.rect(Screen, Green, (0, 546, 1024, 30))

    def Move(self):
        if keys_pressed[K_a]:
            self.PosX -= 3
        if keys_pressed[K_d]:
            self.PosX += 3

    def Jump(self):

        if self.Jumped == True:
                if self.PosY >= 0:
                    self.PosY += 3

        if self.PosY < 0:
            self.PosY = 60

        if keys_pressed[K_w] and self.Jumped == False:
                self.PosY -= 102
                self.Jumped = True

        if self.player_rect.colliderect(self.floor_rect):
            print "collision happened"
            self.PosY = 440
            self.Jumped = False

        if self.PosY >= 468:
            self.PosY = 467
            self.Jumped = False

    def Health(self):
        self.Health = 5


class AI:
    def __init__(self):
        self.PosX = 900
        self.PosY = 200
        self.HealthPosX = 100
        self.HealthPosY = 50
        self.Health = 800
        self.Attacking = False
        self.image = pygame.image.load('GolemScaled.PNG')
        self.Slept = False



    def AIMovement (self,PlayerPosition):
        if self.Attacking == False:
            self.PosX -= 20
            if self.PosX <= PlayerPosition + 30 or self.PosX <= PlayerPosition + 100:
                self.AIAttack()
        elif self.PosX < 901:
            self.PosX += 3

    def AIAttack (self):
        self.Attacking = True




    def HealthClass(self):
        if self.Health < 10:
            self.Health = 10

    def Update(self):
        self.HealthClass()
        self.HealthBar = pygame.image.load('HealthBar.png')
        if self.Health != 10:
            Screen.blit(self.image, (self.PosX, self.PosY))
            pygame.draw.rect(Screen, Red, (100, 50, self.Health, 50))
            Screen.blit(self.HealthBar, (self.HealthPosX, self.HealthPosY))

        if keys_pressed[K_l] and self.Health > 10:
            self.Health -= 1





sprite = Sprite()
player = Player()
Golem = AI()
splashscreenLoop = True
deathscreenloop = False
#Health = Player()
while True:

    if Golem.Attacking == False:
       Counter += 1
    keys_pressed = pygame.key.get_pressed()

    if Counter > 5:
        Golem.AIMovement(player.PosX)
        if Golem.PosX > 800:
            Golem.Attacking = False
            Counter = 0


    if splashscreenLoop == True:
        splashscreen = pygame.image.load('splashtest.PNG')
        Screen.blit(splashscreen, (0, 0))
        if keys_pressed [K_SPACE]:
            splashscreenLoop = False

    #if Health == 0:
       # splashscreen = pygame.image.load('deathscreen.png')
       # Screen.blit(splashscreen, (0, 0))
       # if keys_pressed[K_SPACE]:
       #     deathscreenloop = True

    else:
        player.Move()
        player.Jump()
        sprite.Update()
        player.Update()
        Golem.Update()

    if keys_pressed[K_j]:
        Arrow = pygame.image.load('ArrowSprite.GIF')
        Screen.blit(Arrow, (player.PosX + 50, player.PosY + 18))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
            pygame.quit()
            sys.exit()

    pygame.display.flip()
