import pygame
import sys
from pygame.locals import *

BLACK = (0, 0, 0, 0)
WHITE = (255, 255, 255, 255)
GREEN = (0, 255, 0, 255)
RED = (255, 0, 0, 255)
BLUE = (0, 0, 255, 255)

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 576


PlayerSprite = pygame.image.load('art/PlayerStillScaled.png')
Golem = pygame.image.load('art/GolemScaled.png')
Arrow = pygame.image.load('art/ArrowSprite.gif')
Background = pygame.image.load('art/BackgroundScaled.jpg')
PlatformSprite = pygame.image.load('art/platform.png')
HealthBar = pygame.image.load('art/HealthBar.png')

class AI(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.PosX = 900
        self.PosY = 200
        self.HealthPosX = 100
        self.HealthPosY = 50
        self.Health = 800
        self.Attacking = False
        self.Slept = False
        width = 160
        height = 324
        self.image = pygame.Surface([width,height])
        self.image.set_alpha(0)
        self.image.fill(RED)
        self.rect = self.image.get_rect()

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


class Player(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)


        width = 55
        height = 82
        self.image = pygame.Surface([width, height])
        self.image.set_alpha(0)
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        self.change_x = 0
        self.change_y = 0

        self.level = None

    def ImageBlit(self,screen):
        screen.blit(Player,(self.rect.x,self.rect.y))
        screen.blit(self.image, (0, 0))

    def update(self):
        self.calc_grav()


        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            self.change_y = 0

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):


        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    def go_left(self):

        self.change_x = -6

    def go_right(self):

        self.change_x = 6

    def stop(self):

         self.change_x = 0


class Platform(pygame.sprite.Sprite):


    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.set_alpha(0)
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()


class Bullet(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([10, 4])
        self.image.set_alpha(0)
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()

    def update(self):

        self.rect.x += 10


class Level(object):

    def __init__(self, player):

        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

    def update(self):
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):



        screen.blit(Background,(0,0))

        self.platform_list.draw(screen)




class Level_01(Level):

    def __init__(self, player):



        Level.__init__(self, player)
        level = [[210, 70, 450, 600],
                 [150, 70, 80, 450],
                 [150, 70, 650, 450],
                 ]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)



def main():

    Fired = False
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Platformer Jumper")


    player = Player()
    bullet = Bullet()
    Boss = AI()

    level_list = []
    level_list.append(Level_01(player))

    current_level_no = 0
    current_level = level_list[current_level_no]

    bullet_list = pygame.sprite.Group()
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    done = False

    clock = pygame.time.Clock()
    keys_pressed = pygame.key.get_pressed()
    splashscreenLoop = True

    while True:
        keys_pressed = pygame.key.get_pressed()


        keys_up = pygame.KEYUP
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

            if event.type == pygame.MOUSEBUTTONDOWN and not bullet_list:
                Fired = True
                bullet.rect.x = player.rect.x + 40
                bullet.rect.y = player.rect.y + 20
                # Add the bullet to the lists
                active_sprite_list.add(bullet)
                bullet_list.add(bullet)




        if bullet.rect.x > 815:
            bullet_list.empty()
            active_sprite_list.remove(bullet)

        active_sprite_list.update()

        current_level.update()

        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

        if player.rect.left < 0:
            player.rect.left = 0
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        screen.blit(PlayerSprite, (player.rect.x, player.rect.y))
        if Fired:
            screen.blit(Arrow, (bullet.rect.x, bullet.rect.y))
        screen.blit(PlatformSprite, (450, 600))
        screen.blit(PlatformSprite, (80, 450))
        screen.blit(PlatformSprite, (650, 450))

        if keys_pressed[K_l] and Boss.Health > 10:
            Boss.Health -= 1

        if Boss.Health != 10:
            screen.blit(Golem, (Boss.PosX, Boss.PosY))
            pygame.draw.rect(screen, RED, (100, 50, Boss.Health, 50))
            screen.blit(HealthBar, (Boss.HealthPosX, Boss.HealthPosY))

        if splashscreenLoop == True:
            splashscreen = pygame.image.load('art/splashtest.PNG')
            screen.blit(splashscreen, (0, 0))
            if keys_pressed[K_SPACE]:
                splashscreenLoop = False

        clock.tick(60)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()