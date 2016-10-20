##Basic script so far only sets up the screen and allows quiting##

import pygame, sys
from pygame.locals import *

ScreenWidth = 800
ScreenHeight = 600
##Golem = pygame.image.load("Golem.gif")

pygame.init()

screen = pygame.display.set_mode((ScreenWidth,ScreenHeight),0, 32)
pygame.display.set_caption('Collosi Arena')

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
            pygame.quit()
            sys.exit()



pygame.display.update()