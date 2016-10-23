##Basic script so far only sets up the screen and allows quiting##

import pygame, sys
from pygame.locals import *

ScreenWidth = 1920
ScreenHeight = 1080
Black = (0,0,0)
Golem = pygame.image.load('Golem.gif')
Player = pygame.image.load('CharacterPlaceholder.jpg')

PlayerPosX = 200
PlayerPosY = 600
GolemPosX = 1400
GolemPosY = 300

pygame.init()

Screen = pygame.display.set_mode((ScreenWidth,ScreenHeight),pygame.FULLSCREEN, 32)
pygame.display.set_caption('Collosi Arena')





while True:
    keys_pressed = pygame.key.get_pressed()
    Screen.fill(Black)
    Screen.blit(Golem, (GolemPosX, GolemPosY))
    Screen.blit(Player, (PlayerPosX, PlayerPosY))

    if keys_pressed[K_a]:
        PlayerPosX -= 3
    if keys_pressed[K_d]:
        PlayerPosX += 3

    if (GolemPosX - PlayerPosX) > 300 and (GolemPosX - PlayerPosX) < 900 :
        GolemPosX -= 4
    ##if (GolemPosX - PlayerPosX) <= 300:
        ##Attack
    if (GolemPosX - PlayerPosX) <= 150:
        GolemPosX += 4




    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
            pygame.quit()
            sys.exit()

    pygame.display.update()