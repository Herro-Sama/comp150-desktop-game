##Test Arena##

import pygame
import sys
from pygame.locals import *
import time

ScreenWidth = 1920
ScreenHeight = 1080
Black = (0,0,0)
Counter = 0
GolemImage = pygame.image.load('Golem.gif')
PlayerImage = pygame.image.load('PlayerCharacter.PNG')
Background = pygame.image.load('Background.jpg')
clock = pygame.time.Clock()

pygame.init()

Screen = pygame.display.set_mode((ScreenWidth,ScreenHeight),pygame.FULLSCREEN, 32)
pygame.display.set_caption('Collosi Arena')

class Player:
    def __init__(self):
        self.PosX = 200
        self.PosY = 600
        self.Health = 5
class AI:
    def __init__(self):
        self.PosX = 1400
        self.PosY = 300
        self.Health = 100
        self.Attacking = False

    def AIMovement (self,PlayerPosition):
        if self.Attacking == False:
            self.PosX -= 10
            if self.PosX == PlayerPosition + 100:
                self.AIAttack()
        elif self.PosX < 1401:
            self.PosX += 3

    def AIAttack (self):
        self.Attacking = True




player = Player()
Golem = AI()

while True:
    if Golem.Attacking == False:
       Counter += 1
    keys_pressed = pygame.key.get_pressed()
    Screen.blit(Background, (0, 0))
    Screen.blit(GolemImage, (Golem.PosX, Golem.PosY))
    Screen.blit(PlayerImage, (player.PosX, player.PosY))
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






    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
            pygame.quit()
            sys.exit()
    clock.tick(60)

    pygame.display.flip()
