
import pygame
import random

import math
from pygame import mixer

#Initialization
pygame.init()

screen = pygame.display.set_mode((800, 600))
# Title and icon
pygame.display.set_caption("Space-Invader")
icon = pygame.image.load("anchor.png")
pygame.display.set_icon(icon)

#Player
Player_img = pygame.image.load("ufo.png")
PlayerX = 370
PlayerY = 500
PlayerX_change = 0

#Enemy
Enemy_img = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []
no_of_enemies = 5

for i in range(no_of_enemies):
  Enemy_img.append(pygame.image.load("octopus.png"))
  EnemyX.append(random.randint(0, 800))
  EnemyY.append(random.randint(0, 150))
  EnemyX_change.append(0.4)
  EnemyY_change.append(40)


#Background
Background = pygame.image.load("—Pngtree—star space celestial body astronomy_616162.jpg")
# Background music
mixer.music.load("background.wav")
mixer.music.play(-1)

#Bullet
Bullet_img = pygame.image.load("bullet.png")
BulletX = 0
BulletY = 500
BulletX_change = 0
BulletY_change = 0.9
Bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10
# GAME OVER

over_text = pygame.font.Font("freesansbold.ttf", 128)

# Functions
def game_over():
    OVER = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(OVER, (340, 250))

def player(x, y):
    screen.blit(Player_img, (x, y))
def enemy(x, y, i):
    screen.blit(Enemy_img[i], (x, y))
def show_score(x, y):
    score = font.render("SCORE:" + str(score_value), True, (255,255, 255))
    screen.blit(score, (x, y))
def fire_bullet(x, y):
    global Bullet_state
    Bullet_state = "fire"
    screen.blit(Bullet_img, (x + 10, y))

def is_collisiom(enemyX, enemyy, bulletx, bullety):
 distance = math.sqrt(math.pow(enemyX - bulletx, 2) + math.pow(enemyy - bullety, 2))
 if distance < 25:
     return True
 else:
     return False
#Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(Background, (0, 0))
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_LEFT:
               PlayerX_change = -0.8
           if event.key == pygame.K_RIGHT:
               PlayerX_change = 0.8
           if event.key == pygame.K_SPACE:
               if Bullet_state == "ready":
                  bullet_sound = mixer.Sound("laser.wav")
                  bullet_sound.play()
                  BulletX = PlayerX
                  fire_bullet(BulletX, BulletY)
        if event.type == pygame.KEYUP:
           if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
               PlayerX_change = 0

     # Player movement
    PlayerX += PlayerX_change
    if PlayerX >= 736:
        PlayerX = 736
    if PlayerX <= 0:
         PlayerX = 0
    # Enemy movement
    for i in range(no_of_enemies):

      # Game over
      if EnemyY[i] > 460:
          for j in range(no_of_enemies):
              EnemyY[j] = 2000
          game_over()
          break
      EnemyX[i] += EnemyX_change[i]
      if EnemyX[i] >= 736:
          EnemyX_change[i] = -0.6
          EnemyY[i] += EnemyY_change[i]
      if EnemyX[i] <= 0:
          EnemyX_change[i] = 0.6
          EnemyY[i] += EnemyY_change[i]

      # collision
      collision = is_collisiom(EnemyX[i], EnemyY[i], BulletX, BulletY)
      if collision:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        BulletY = 500
        Bullet_state = "ready"
        score_value += 1
        EnemyX[i] = random.randint(0, 736)
        EnemyY[i] = random.randint(50, 150)
      enemy(EnemyX[i], EnemyY[i], i)

    #bullet movement
    if BulletY <= 0:
        BulletY = 500
        Bullet_state = "ready"
    if Bullet_state == "fire":
         fire_bullet(BulletX, BulletY)
         BulletY -= BulletY_change


    player(PlayerX, PlayerY)
    show_score(textX, textY)
    pygame.display.update()