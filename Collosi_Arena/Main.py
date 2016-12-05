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
        self.HealthPosX = 100
        self.HealthPosY = 50
        self.Health = 800
        self.Attacking = False
        self.Slept = False
        width = 160
        height = 324
        self.HealthBar = None

        self.level = None

        self.image = pygame.Surface([width, height])
        self.image.set_alpha(0)
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.y = 275
        self.rect.x = 900

    def ai_movement(self, player_position):
        if self.Attacking == False:
            self.rect.y = 275
            self.rect.x -= 20
            if self.rect.x <= player_position + 30 or self.rect.x <= player_position + 100:
                self.ai_attack()
        elif self.rect.x < 901:
            self.rect.x += 3

    def ai_attack(self):
        self.Attacking = True

    def health_class(self):
        if self.Health < 10:
            self.Health = 10

    def update(self):
        self.health_class()
        self.HealthBar = pygame.image.load('art/HealthBar.png')


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

    def imageblit(self, screen):
        screen.blit(Player, (self.rect.x, self.rect.y))
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

    def __init__(self, player, ai):

        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
        self.Boss = ai

    def update(self):
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):

        screen.blit(Background,  (0, 0))

        self.platform_list.draw(screen)


class Level01(Level):

    def __init__(self, player):
        Level.__init__(self, player, AI)
        level = [[210, 70, 450, 200],
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

    fired = False
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Platformer Jumper")
    player = Player()
    bullet = Bullet()
    boss = AI()

    level_list = []
    level_list.append(Level01(player))

    current_level_no = 0
    current_level = level_list[current_level_no]

    enemy_list = pygame.sprite.Group()
    bullet_list = pygame.sprite.Group()
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)
    active_sprite_list.add(boss)
    enemy_list.add(boss)
    clock = pygame.time.Clock()
    splash_screen_loop = True
    counter = 0
    boss_dead = False

    while True:
        keys_pressed = pygame.key.get_pressed()

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
                fired = True
                bullet.rect.x = player.rect.x + 40
                bullet.rect.y = player.rect.y + 20
                # Add the bullet to the lists
                active_sprite_list.add(bullet)
                bullet_list.add(bullet)
        if pygame.sprite.spritecollide(boss, bullet_list, True):
            boss.Health -= 60
            bullet_list.remove(bullet)
            active_sprite_list.remove(bullet)
        if bullet.rect.x > 1030:
            bullet_list.empty()
            active_sprite_list.remove(bullet)
        active_sprite_list.update()
        bullet_list.update()
        current_level.update()

        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

        if player.rect.left < 0:
            player.rect.left = 0
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        screen.blit(PlayerSprite, (player.rect.x, player.rect.y))
        if fired:
            for bullet in bullet_list:
                screen.blit(Arrow, (bullet.rect.x, bullet.rect.y))
        screen.blit(PlatformSprite, (450, 200))
        screen.blit(PlatformSprite, (80, 450))
        screen.blit(PlatformSprite, (650, 450))
        if boss.Health <= 10:
            boss_dead = True
        if boss.Health != 10 and boss_dead == False:
            screen.blit(Golem, (boss.rect.x, boss.rect.y))
            pygame.draw.rect(screen, RED, (100, 50, boss.Health, 50))
            screen.blit(HealthBar, (boss.HealthPosX, boss.HealthPosY))
        if boss.Attacking == False:
            counter += 1
        if counter > 5:
            boss.ai_movement(player.rect.x)
            if boss.rect.x > 800:
                boss.Attacking = False
                counter = 0
        boss.update()

        if splash_screen_loop == True:
            splashscreen = pygame.image.load('art/splashtest.PNG')
            screen.blit(splashscreen, (0, 0))
            if keys_pressed[K_SPACE]:
                splash_screen_loop = False

        if boss_dead == True:
            winningscreen = pygame.image.load('art/winscreen.jpg')
            screen.blit(winningscreen, (0,0))

        clock.tick(60)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()