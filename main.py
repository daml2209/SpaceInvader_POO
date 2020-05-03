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


class Game:
    def __init__(self, font, FPS, lives, window, clock = pygame.time.Clock()):
        self.font = font
        self.FPS = FPS
        self.lives = lives
        self.level = 0
        self.count = 0
        self.window = window
        self.clock = clock

    # Quitting the Game
    def escape(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            else:
                return False

    # Game Over
    def over(self):
        if self.lives <= 0:
            self.count = 0
            while True:
                self.clock.tick(self.FPS)
                lost_label = self.font.render('GAME OVER',  1, (255,255,255))
                self.window.blit(lost_label, ((WIDTH-lost_label.get_width())/2, (HEIGTH-lost_label.get_height())/2))
                pygame.display.update()
                self.count += 1
                if self.count == self.FPS*3:
                    break
            return True
        else:
            return False
            
    # Drawing the HUD
    def draw_HUD(self):
        lives_label = self.font.render(f'Lives: {self.lives}', 1, (255,255,255))
        level_label = self.font.render(f'Level: {self.level}', 1, (255,255,255))
        self.window.blit(lives_label, (10, 10))
        self.window.blit(level_label, (WIDTH-level_label.get_width()-10, 10))

class Drawing:
    def __init__(self, window):
        self.window = window

    def drawing(self, game, player, enemies):
        # Drawing the background
        self.window.blit(BACKGROUND, (0,0))

        # Drawing the enemies
        # We made a copy of the enemy list to avoid bugs because we are removing from the list at the same time that we are iterating on it
        for enemy in enemies[:]:
            enemy.draw(WIN)

        # Drawing the Player
        player.draw(WIN)

        # Drawing the HUD
        game.draw_HUD()

        pygame.display.update()

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
    def increase_speed(self):
        self.x_speed *= 1.1
        self.y_speed *= 1.1


class Enemy(Ship):
    COLOR = {'blue'   : (ENEMY_BLUE_IMAGE,   SHOT_BLUE_IMAGE),
             'green'  : (ENEMY_GREEN_IMAGE,  SHOT_GREEN_IMAGE),
             'purple' : (ENEMY_PURPLE_IMAGE, SHOT_PURPLE_IMAGE),}

    def __init__(self, speed, x= 50, y= 50, color= 'blue', health = 100):
        super().__init__(x, y, health)
        self.ship_img, self.bullet_img = self.COLOR[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.speed = speed

    def move(self):
        self.y += self.speed

    def create(self, amount):
        enemies = []
        for i in range(amount):
            enemy = Enemy(x = random.randrange(20, WIDTH-ENEMY_BLUE_IMAGE.get_width()-20),
                          y = random.randrange(-1000, -100),
                          color = random.choice(['blue', 'green', 'purple']),
                          speed = self.speed)
            enemies.append(enemy)
        return enemies


    def increase_speed(self):
        self.speed *= 1.1


def main():

    run = True
    clock = pygame.time.Clock()

    # Instancing the Game
    font = pygame.font.SysFont('comicsans', 50)
    game = Game(font, FPS= 60, lives= 3, window = WIN, clock = clock)
    
    # Player properties and Instancing it
    player_x = ((WIDTH)-(PLAYER_IMAGE.get_width()))/2
    player_y = 480
    player = Player(x = player_x, y = player_y, x_speed= 5,y_speed= 5)

    # Enemyes properties and Instancing it in a list of enemies
    enemy = Enemy(speed = 1)
    enemy_wave = 5
    enemies = enemy.create(enemy_wave)

    # Drawing
    draw = Drawing(WIN) 
    draw.drawing(game, player, enemies)


    while run:
        clock.tick(game.FPS)

        # Game Over
        if game.over():
            run = False
            continue
        # Quitting the
        if game.escape():
            run = False
            continue
          
        # Increasing the Level
        if len(enemies) == 0:
            game.level += 1
            enemy_wave += 1
            enemy.increase_speed()
            player.increase_speed()
            enemies = enemy.create(amount = enemy_wave)

        
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
            enemy.move()
            if enemy.y + enemy.get_height() >= HEIGTH:
                game.lives -= 1
                enemies.remove(enemy)

        draw.drawing(game, player, enemies)

main()