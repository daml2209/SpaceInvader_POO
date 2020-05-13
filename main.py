import os
import time
import random
import pygame
from pygame import mixer
pygame.font.init()
pygame.init()

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
# mixer.music.load('sounds/background_song.mp3')

# Game window
WIDTH, HEIGTH = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption(TITLE)
pygame.display.set_icon(ICON_IMAGE)


class Game:
    def __init__(self, font, FPS, lives, window, bullets= 0, clock = pygame.time.Clock()):
        self.font = font
        self.FPS = FPS
        self.lives = lives
        self.level = 1
        self.count = 0
        self.window = window
        self.clock = clock
        self.bullets = bullets
        self.bullet_img = BULLET_IMAGE

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
    
    def reload_bullet(self, bullet):
        self.bullets = bullet

    # Drawing the HUD
    def draw_HUD(self):
        offset = 0
        lives_label = self.font.render(f'Lives: {self.lives}', 1, (255,255,255))
        level_label = self.font.render(f'Level: {self.level}', 1, (255,255,255))
        self.window.blit(lives_label, (10, 10))
        self.window.blit(level_label, (WIDTH-level_label.get_width()-10, 10))
        for i in range(self.bullets):
            offset += self.bullet_img.get_width() 
            self.window.blit(self.bullet_img, (WIDTH - offset, HEIGTH - 50))

class Drawing:
    def __init__(self, window):
        self.window = window

    def drawing(self, game, player, enemies, FPS):
        # Drawing the background
        self.window.blit(BACKGROUND, (0,0))

        # Drawing bullets
        player.fire(WIN)

        # Drawing the enemies
        # We made a copy of the enemy list to avoid bugs because we are removing from the list at the same time that we are iterating on it
        for enemy in enemies[:]:
            enemy.draw(WIN)
        
        # Drawing the Player
        player.draw(WIN)

        # Drawing the HUD
        game.draw_HUD()

        pygame.display.update()


class Bullet:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    
    def move(self, speed):
        self.y += speed
    
    def collision(self, obj):
        offset = (int(self.x - obj.x - 30), int(self.y - obj.y - 20))
        return self.mask.overlap(obj.mask, (offset))


class Ship:
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.bullet_img = None
        self.bullet_cooldown_counter = 0
        self.bullets = []
        self.fired_bullets = []
        self.cool_down = 120
            
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
        self.bullet_speed = -10
        self.max_health = health
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.creation_cooldown_counter = 0
        self.max_amount_bullets = 3

    # Movement
    def move(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and (self.y > 0):
            self.y -= self.y_speed
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and (self.y < HEIGTH - self.ship_img.get_height() - 60):
            self.y += self.y_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (self.x < WIDTH - self.ship_img.get_width()):
            self.x += self.x_speed
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (self.x > 0):
            self.x -= self.x_speed

    def increase_speed(self):
        if self.x_speed < 10:
            self.x_speed += 1.25
            self.y_speed += 1.25
        elif self.x_speed >= 10:
            self.x_speed = 10
            self.y_speed = 8
        if self.cool_down > 25:
            self.cool_down *= 0.9

    def create_bullets(self):
        if (len(self.bullets) < self.max_amount_bullets) and (self.creation_cooldown_counter == 0):
            bullet = Bullet(self.x, self.y, self.bullet_img)
            self.bullets.append(bullet)
            self.creation_cooldown_counter = 1
        for bullet in self.fired_bullets:
            if bullet.y <= -40:
                self.fired_bullets.pop(0) 

    
    def cooldown(self):
        if self.bullet_cooldown_counter >= 20:
            self.bullet_cooldown_counter = 0
        elif self.bullet_cooldown_counter > 0:
            self.bullet_cooldown_counter += 1

        if self.creation_cooldown_counter >= self.cool_down :
            self.creation_cooldown_counter = 0
        elif self.creation_cooldown_counter > 0:
            self.creation_cooldown_counter += 1
            
    # Fire
    def fire(self, window):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_SPACE]) and (len(self.bullets) > 0) and (self.bullet_cooldown_counter == 0):
            self.bullets[-1].x = self.x + (self.ship_img.get_width() - self.bullet_img.get_width())/2
            self.bullets[-1].y = self.y + 10
            self.fired_bullets.append(self.bullets.pop())
            self.bullet_cooldown_counter = 1
            self.creation_cooldown_counter = 1

        for i in range(len(self.fired_bullets)):
            self.fired_bullets[i].move(self.bullet_speed)
            self.fired_bullets[i].draw(window)
    
    def hit(self, enemy):
        for i in range(len(self.fired_bullets)):
            self.creation_cooldown_counter = self.cool_down *0.8
            return self.fired_bullets[i].collision(enemy)
            

           
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
        self.speed *= 1.02
    

def main():

    run = True
    clock = pygame.time.Clock()
    FPS = 60
    # mixer.music.play(-1)

    # Instancing the Game
    font = pygame.font.SysFont('comicsans', 50)
    game = Game(font, FPS, lives= 3, window = WIN, clock = clock)
    
    # Player properties and Instancing it
    player_x = ((WIDTH)-(PLAYER_IMAGE.get_width())) / 2
    player_y = 480
    player = Player(x= player_x, y= player_y, x_speed= 5, y_speed= 4)

    # Enemyes properties and Instancing it in a list of enemies
    enemy_init = Enemy(speed = 0.8)
    enemy_wave = 4
    enemies = enemy_init.create(enemy_wave)

    # Drawing
    draw = Drawing(WIN) 
    draw.drawing(game, player, enemies, FPS= 60)


    while run:
        clock.tick(FPS)

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
            if game.level % 3 == 0:
                if player.max_amount_bullets < 10:
                    player.max_amount_bullets += 1
                if game.lives < 6:
                    game.lives += 1

        
        # Player Movement
        player.move()
        player.create_bullets()
        game.reload_bullet(len(player.bullets))
        player.cooldown()

        # Enemy Movement
        for enemy in enemies:
            enemy.move()
            if player.hit(enemy):
                enemies.remove(enemy)
                player.fired_bullets.pop(0)
            if enemy.y + enemy.get_height() >= HEIGTH:
                game.lives -= 1
                enemies.remove(enemy)

        draw.drawing(game, player, enemies, FPS)

if __name__ == "__main__":
    main()