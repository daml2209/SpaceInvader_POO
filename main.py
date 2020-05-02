import os
import time
import random
import pygame
from pygame import mixer
pygame.font.init()

# Player:
    # Images
PLAYER_IMAGE = pygame.image.load(os.path.join('img', 'player_image.png'))
BULLET_IMAGE = pygame.image.load(os.path.join('img', 'bullet_image.png'))
    # SFX


# Enemy:
    # Images
ENEMY_BLUE_IMAGE = pygame.image.load(os.path.join('img', 'enemy_blue_image.png'))
ENEMY_GREEN_IMAGE = pygame.image.load(os.path.join('img', 'enemy_green_image.png'))
ENEMY_PURPLE_IMAGE = pygame.image.load(os.path.join('img', 'enemy_purple_image.png'))
SHOT_BLUE_IMAGE = pygame.image.load(os.path.join('img', 'shot_blue.png'))
SHOT_GREEN_IMAGE = pygame.image.load(os.path.join('img', 'shot_green.png'))
SHOT_PURPLE_IMAGE = pygame.image.load(os.path.join('img', 'shot_purple.png'))
    # SFX


# Background:
BACKGROUND = pygame.image.load(os.path.join('img', 'background.png'))
ICON_IMAGE = pygame.image.load(os.path.join('img', 'title_icon.png'))
TITLE = 'Doony Invaders'
# Game window
WIDTH, HEIGTH = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption(TITLE)
pygame.display.set_icon(ICON_IMAGE)


class Ship:
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.bullet_img = None
        self.bullets = []
        self.bullet_cooldown = 0
            
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img = PLAYER_IMAGE
        self.bullet_img = BULLET_IMAGE
        self.bullet_x = x + (self.ship_img.get_width() - self.bullet_img.get_width())/2
        self.bullet_y = y + 10
        self.max_health = health
        self.mask = pygame.mask.from_surface(self.ship_img)

    def fire(self, speed):
        self.bullet_y -= speed


class Enemy(Ship):
    COLOR = {'blue' : (ENEMY_BLUE_IMAGE, SHOT_BLUE_IMAGE), 'green' : (ENEMY_GREEN_IMAGE, SHOT_GREEN_IMAGE), 'purple' : (ENEMY_PURPLE_IMAGE, SHOT_PURPLE_IMAGE),}

    def __init__(self, x, y, color, health = 100):
        super().__init__(x, y, health)
        self.ship_img, self.bullet_img = self.COLOR[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, speed):
        self.y += speed


def main():
    run = True
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('comicsans', 50)
    FPS = 60
    lives = 3
    level = 0

    # Player stats
    player_speed_x = 5
    player_speed_y = 4
    player = Player(((WIDTH)-(PLAYER_IMAGE.get_width()))/2, 480)
    bullet_speed = 10
    status = 'ready'

    # Enemyes stats
    enemies = []
    enemy_wave = 5
    enemy_speed = 1


    def drawing(window):
        # Drawing the background
        window.blit(BACKGROUND, (0,0))

        # Drawing the enemies
        for enemy in enemies:
            enemy.draw(WIN)

        # Drawing the Player
        player.draw(WIN)
        WIN.blit(player.bullet_img, (player.bullet_x, player.bullet_y))

        # Drawing the HUD
        lives_label = font.render(f'Lives: {lives}', 1, (255,255,255))
        level_label = font.render(f'Level: {level}', 1, (255,255,255))
        window.blit(lives_label, (10, 10))
        window.blit(lives_label, (WIDTH-level_label.get_width()-10, 10))

        pygame.display.update()


    while run:
        clock.tick(FPS)

        # Quitting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        # Increasing the Level
        if len(enemies) == 0:
            level += 1
            enemy_wave += 4
            enemy_speed *= 1.1
            player_speed_x *= 1.1
            player_speed_y *= 1.1
            for i in range(enemy_wave):
                enemy = Enemy(random.randrange(20, WIDTH-ENEMY_BLUE_IMAGE.get_width()-20), random.randrange(-1000, -100-i*50), random.choice(['blue', 'green', 'purple'])) 
                enemies.append(enemy)
        
        # Player Movement
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and (player.y > 0):
            player.y -= player_speed_y
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and (player.y < HEIGTH - player.get_height()):
            player.y += player_speed_y
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (player.x < WIDTH - player.get_width()):
            player.x += player_speed_x
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (player.x > 0):
            player.x -= player_speed_x


        # Enemy Movement
        for enemy in enemies:
            enemy.move(enemy_speed)


        drawing(WIN)



main()