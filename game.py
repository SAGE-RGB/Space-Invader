# importing all libraries
import pygame as pg
from random import *
from math import *
from pygame import mixer

# defining screen,bgimage,caption,icon and bg score
pg.init()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("SPACE-INVADER")
bgimg = pg.image.load("bg.png")
mixer.music.load("bg.wav")
mixer.music.play(-1)
icon = pg.image.load("spaceship.png")
pg.display.set_icon(icon)

# defining player image
playerimg = pg.image.load("player.png")
playerx = 370
playery = 480
playerx_change = 0


# defining enemy image
x = 3
num_of_enemies = x

enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
for x in range(num_of_enemies):  # this loop is used to create multiple enemies
    enemyimg.append(pg.image.load("polotno.png"))
    enemyx.append(randint(0, 735))
    enemyy.append(randint(30, 100))
    enemyx_change.append(2)
    enemyy_change.append(40)

# defining bullet
bulletimg = pg.image.load("bullet.png")
bulletx = 0
bullety = 480
bullet_state = "ready"
bullety_change = 5

bulletimg2 = pg.image.load("bullet.png")
bulletx2 = int(enemyx[0])
bullety2 = int(enemyy[0])
bullet_state2 = "ready"
bullety_change2 = -5

# score and gameover font
score_val = 0
font = pg.font.Font("freesansbold.ttf", 32)

textx = 10
texty = 10
gameover = pg.font.Font("freesansbold.ttf", 64)

# important functions


def game_over():  # function to end the game
    score = gameover.render("GAME OVER", True, (255, 255, 255))
    screen.blit(score, (200, 250))


def showscore(x, y):  # function to show score all the time on top of screen
    score = font.render("Score : "+str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):  # drawing player on screen
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):  # drawing enemy on screen
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):  # function to fire the bullet
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x+16, y+10))


def fire_enemy_bullet(x, y):
    global bullet_state2
    global bullety2
    bullet_state2 = "fire"
    screen.blit(bulletimg2, (x+16, y+10))
    bullety2 -= bullety_change2


# function checking wheter their is a colision or not


def iscollision(enemyx, enemyy, bulletx, bullety):
    distance = sqrt((pow(enemyx-bulletx, 2))+(pow(enemyy-bullety, 2)))
    if distance < 27:
        return True


# main loop
run = True
while run:  # an infinite loop for the game so that screen never goes off
    screen.fill((0, 0, 0))
    bg = screen.blit(bgimg, (0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:  # to close the screen
            run = False
        if event.type == pg.KEYDOWN:  # setting up keyboard buttons to work
            if event.key == pg.K_LEFT:  # setting up keys for movement
                playerx_change = -3
            if event.key == pg.K_RIGHT:
                playerx_change = 3
            if event.key == pg.K_SPACE:  # setting up key for firing
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("gunshot.wav")
                    bullet_sound.play()
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)
                    fire_enemy_bullet(int(enemyx[0]), int(enemyy[0]))
        if event.type == pg.KEYUP:
            playerx_change = 0

    playerx += playerx_change  # movement mechanics
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736
    for i in range(num_of_enemies):

        if enemyy[i] > 440:
            for j in range(num_of_enemies):
                enemyy[j] = 2000
            game_over()
            break
        ebiy_state = "fire"
        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] = 2
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i] = -2
            enemyy[i] += enemyy_change[i]
        collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            colli_sound = mixer.Sound("explosion.wav")
            colli_sound.play()
            bullety = 480
            bullet_state = "ready"
            score_val += 1
            if score_val % 20 == 0:
                num_of_enemies += 1
                enemyimg.append(pg.image.load("polotno.png"))
                enemyx.append(randint(0, 735))
                enemyy.append(randint(30, 100))
                enemyx_change.append(2)
                enemyy_change.append(40)
            if score_val % 100 == 0:  # increase enemy speed every 100 points
                for j in range(num_of_enemies):
                    enemyx_change[j] += 1
            enemyx[i] = randint(0, 735)
            enemyy[i] = randint(30, 100)
        enemy(enemyx[i], enemyy[i], i)

    def on_collision():
        # Fire an enemy bullet.
        fire_enemy_bullet(enemyx, enemyy)

    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change

    if bullety2 >= 480:
        bullety2 = int(enemyy[0])
        bullet_state2 = "ready"

    if bullet_state2 == "fire":
        fire_bullet(enemyx[0], enemyy[0])
        bullety2 -= bullety_change2

    player(playerx, playery)
    showscore(textx, texty)
    pg.display.update()
