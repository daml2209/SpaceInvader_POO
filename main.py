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
        self.bullets = []
        self.bullet_cooldown = 0
            
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()
    

class Player(Ship):
    def __init__(self, x, y, x_speed, y_speed, health = 100):
        super().__init__(x, y, health)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.ship_img = PLAYER_IMAGE
        self.bullet_img = BULLET_IMAGE
        self.bullet_x = self.x + (self.ship_img.get_width() - self.bullet_img.get_width())/2
        self.bullet_y = self.y + 10
        self.max_health = health
        self.mask = pygame.mask.from_surface(self.ship_img)

    def up(self):
        self.y -= self.y_speed
    def down(self):
        self.y += self.y_speed
    def right(self):
        self.x += self.x_speed
    def left(self):
        self.x -= self.x_speed


class Enemy(Ship):
    COLOR = {'blue' : (ENEMY_BLUE_IMAGE, SHOT_BLUE_IMAGE), 'green' : (ENEMY_GREEN_IMAGE, SHOT_GREEN_IMAGE), 'purple' : (ENEMY_PURPLE_IMAGE, SHOT_PURPLE_IMAGE),}

    def __init__(self, x, y, color, health = 100):
        super().__init__(x, y, health)
        self.ship_img, self.bullet_img = self.COLOR[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, speed):
        self.y += speed

class Game:
    def __init__(self, font, FPS, lives):
        self.font = font
        self.FPS = FPS
        self.lives = lives
        self.level = 0
        self.count = 0
        self.lost = False

    # def quitting(self):
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             return False
    #         else:
    #             return True



def main():

    run = True
    clock = pygame.time.Clock()

    # Game Parameters
    font = pygame.font.SysFont('comicsans', 50)
    game = Game(font, FPS= 60, lives= 3)
    
    # Player stats
    player_speed_x = 5
    player_speed_y = 4
    player = Player(((WIDTH)-(PLAYER_IMAGE.get_width()))/2, 480, player_speed_x, player_speed_y)

    # Enemyes stats
    enemies = []
    enemy_wave = 5
    enemy_speed = 1

    def drawing(window):

        # Drawing the background
        window.blit(BACKGROUND, (0,0))

        # Drawing the enemies
        # We made a copy of the enemy list to avoid bugs because we are removing from the list at the same time that we are iterating on it
        for enemy in enemies[:]:
            enemy.draw(WIN)

        # Drawing the Player
        player.draw(WIN)

        # Drawing the HUD
        lives_label = font.render(f'Lives: {game.lives}', 1, (255,255,255))
        level_label = font.render(f'Level: {game.level}', 1, (255,255,255))
        window.blit(lives_label, (10, 10))
        window.blit(level_label, (WIDTH-level_label.get_width()-10, 10))

        if game.lost:
            lost_label = font.render('GAME OVER',  1, (255,255,255))
            window.blit(lost_label, ((WIDTH-lost_label.get_width())/2, (HEIGTH-lost_label.get_height())/2))

        pygame.display.update()


    while run:
        clock.tick(game.FPS)

        # Quitting, loosing or winning the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if game.lost:
            game.count += 1
            if game.count == game.FPS*3:
                run = False
            else:
                continue
        if game.lives <= 0:
            game.lost = True


        # Increasing the Level
        if len(enemies) == 0:
            game.level += 1
            enemy_wave += 4
            enemy_speed *= 1.1
            player_speed_x *= 1.1
            player_speed_y *= 1.1
            for i in range(enemy_wave):
                enemy = Enemy(random.randrange(20, WIDTH-ENEMY_BLUE_IMAGE.get_width()-20), random.randrange(-1000, -100), random.choice(['blue', 'green', 'purple'])) 
                enemies.append(enemy)
        
        # Player Movement
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and (player.y > 0):
            player.up()
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and (player.y < HEIGTH - player.get_height()):
            player.down()
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (player.x < WIDTH - player.get_width()):
            player.right()
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (player.x > 0):
            player.left()

        # Enemy Movement
        for enemy in enemies:
            enemy.move(enemy_speed)
            if enemy.y + enemy.get_height() >= HEIGTH:
                game.lives -= 1
                enemies.remove(enemy)

        
        drawing(WIN)



main()