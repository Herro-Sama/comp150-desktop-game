##Test Arena##

import pygame
import sys
from pygame.locals import *
import time

ScreenWidth = 1920
ScreenHeight = 1080
Black = (0,0,0)
Counter = 0

pygame.init()

Screen = pygame.display.set_mode((ScreenWidth,ScreenHeight),pygame.FULLSCREEN, 32)
pygame.display.set_caption('Collosi Arena')
class Sprite:
    def __init__(self):
        self.BackgroundImage = pygame.image.load('Background.jpg')

    def Update(self):
        Screen.blit(self.BackgroundImage, (0, 0))
class Player:
    def __init__(self):
        self.PosX = 200
        self.PosY = 600
        self.Health = 5
        self.PlayerSprite = pygame.image.load('CharacterPlaceholder.jpg')

    def Update(self):
        Screen.blit(self.PlayerSprite, (self.PosX, self.PosY))


class AI:
    def __init__(self):
        self.PosX = 1400
        self.PosY = 300
        self.Health = 100
        self.Attacking = False
        self.image = pygame.image.load('Golem.gif')



    def AIMovement (self,PlayerPosition):
        if self.Attacking == False:
            self.PosX -= 10
            if self.PosX == PlayerPosition + 100:
                self.AIAttack()
        elif self.PosX < 1401:
            self.PosX += 3

    def AIAttack (self):
        self.Attacking = True

    def Update(self):
        self.HealthBar = pygame.image.load('HealthBar.png')
        Screen.blit(self.image, (self.PosX, self.PosY))
        Screen.blit(self.HealthBar, (self.PosX, self.PosY))


sprite = Sprite()
player = Player()
Golem = AI()

while True:
    if Golem.Attacking == False:
       Counter += 1
    keys_pressed = pygame.key.get_pressed()
    if Counter > 30:
        Golem.AIMovement(player.PosX)
        if Golem.PosX > 1400:
            Golem.Attacking = False
            Counter = 0
    if keys_pressed[K_a]:
        player.PosX -= 3
    if keys_pressed[K_d]:
        player.PosX += 3
    print Golem.Attacking
    sprite.Update()
    player.Update()
    Golem.Update()





    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
            pygame.quit()
            sys.exit()

    pygame.display.flip()