#No-Wall Pong
#Project by Hunter Gerace
#CPSC 386
#20 September 2019


# Import and initialize interpreter
import pygame
import sys
import random
from pygame.locals import *
from time import sleep

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

# Defined colors, although unneeded
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Window creation
WINDOWWIDTH = 1024
WINDOWHEIGHT = 576
screen = pygame.display.set_mode(
    (WINDOWWIDTH, WINDOWHEIGHT), 0, 32)  # PAL 1024x576 (suitable for landscape game)
pygame.display.set_caption("No-Wall Pong")
pongBack = pygame.Rect(0, 0, 1024, 576)
pongBackground = pygame.image.load('pong.png')

# Score and text creation
playerScore = 0
cpuScore = 0
bf = pygame.font.SysFont(None, 48)
# Rest has been placed inside game loop, to keep score updated.


# Player creation
playerCenter = pygame.Rect(1000, 192, 6, 192)  # set vertical of center paddle
playerTop = pygame.Rect(800, 12, 192, 6)  # set horizontal of top paddle
playerBottom = pygame.Rect(800, 564, 192, 6)  # set horizontal of bottom paddle
playerCenterImage = pygame.image.load('center_player_pad.png')  # image for player's center paddle
playerTopImage = pygame.image.load('top_player_pad.png')  # image for player's top paddle
playerBottomImage = pygame.image.load('bottom_player_pad.png')  # image for player's bottom paddle

# CPU creation
cpuCenter = pygame.Rect(24, 192, 6, 192)  # set vertical of center paddle
cpuTop = pygame.Rect(128, 12, 192, 6)  # set horizontal of top paddle
cpuBottom = pygame.Rect(128, 564, 192, 6)  # set horizontal of bottom paddle
cpuCenterImage = pygame.image.load('center_cpu_pad.png')  # image for player's center paddle
cpuTopImage = pygame.image.load('top_cpu_pad.png')  # image for player's top paddle
cpuBottomImage = pygame.image.load('bottom_cpu_pad.png')  # image for player's bottom paddle

# Ball & net creation
pongBall = pygame.Rect(512, 288, 13, 13)  # set size and position of pong ball
pongNet = pygame.Rect(512, 0, 6, 572)  # set size and position of net
pongBallImage = pygame.image.load('ball.png')  # image for pong ball
pongNetImage = pygame.image.load('dashed_net.png')  # image for dashed net

# Generate random ball direction
direction = random.randint(1, 4)
if direction == 1:
    ball = {'rect': pongBall, 'dir': 'downleft'}
if direction == 2:
    ball = {'rect': pongBall, 'dir': 'downright'}
if direction == 3:
    ball = {'rect': pongBall, 'dir': 'upleft'}
if direction == 4:
    ball = {'rect': pongBall, 'dir': 'upright'}

# Music and sound
hitSound = pygame.mixer.Sound('hit.wav')
winSound = pygame.mixer.Sound('win.wav')
loseSound = pygame.mixer.Sound('lose.wav')
pygame.mixer.music.load('pong.wav')
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1, 0.0)
musicPlaying = True

# Keyboard variables
moveLeft = False
moveRight = False
moveUp = False
moveDown = False
MOVESPEED = 6
CPUSPEED = 5.5

# Miscellaneous initialization
clock = pygame.time.Clock()
game_On = False


# Reset function
def reset():
    cpuCenter.center = (24, 192)
    cpuTop.left = cpuBottom.left = 128
    cpuTop.top = 12
    cpuBottom.top = 564
    pongBall.center = (512, 288)

    newDirect = random.randint(1, 4)
    if newDirect == 1:
        ball['dir'] = 'downleft'
    if newDirect == 2:
        ball['dir'] = 'downright'
    if newDirect == 3:
        ball['dir'] = 'upleft'
    if newDirect == 4:
        ball['dir'] = 'upright'


def end_Game():  # Prompt that occurs after game ends
    prompt = bf.render("'R' = Reset Game, 'Q' = Quit Game'", False, WHITE, BLACK)
    pr = prompt.get_rect()
    pr.centerx = 512
    pr.centery = 322
    screen.blit(prompt, pr)


# TITLE SCREEN
while not game_On:
    screen.blit(pongBackground, pongBack)
    title = bf.render("Welcome to No-Wall Pong!", False, WHITE, BLACK)
    rules = bf.render("First player to 11 points wins.", False, WHITE, BLACK)
    start = bf.render("Press any arrow key to begin.", False, WHITE, BLACK)
    t = title.get_rect()
    t.centerx = 512
    t.centery = 240
    r = rules.get_rect()
    r.centerx = 512
    r.centery = 288
    s = start.get_rect()
    s.centerx = 512
    s.centery = 326
    screen.blit(title, t)
    screen.blit(rules, r)
    screen.blit(start, s)

    for event in pygame.event.get():  # User performs an action
        if event.type == pygame.QUIT:  # User clicks the "close" button
            pygame.quit()
            sys.exit()  # Breaks loop and closes the game
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                # screen.fill(BLACK)
                game_On = True
            if event.key == K_q or event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Update screen
    pygame.display.flip()
    # Set clock to 60fps
    clock.tick(60)

# Main game loop
while game_On:
    for event in pygame.event.get():  # User performs an action
        if event.type == pygame.QUIT:  # User clicks the "close" button
            pygame.quit()
            sys.exit()  # Breaks loop and closes the game
        if event.type == KEYDOWN:
            # Change the keyboard variables.
            if event.key == K_LEFT:
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT:
                moveLeft = False
                moveRight = True
            if event.key == K_UP:
                moveDown = False
                moveUp = True
            if event.key == K_DOWN:
                moveDown = True
                moveUp = False
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT:
                moveLeft = False
            if event.key == K_RIGHT:
                moveRight = False
            if event.key == K_UP:
                moveUp = False
            if event.key == K_DOWN:
                moveDown = False
            if event.key == K_r:  # Reset game
                playerScore = 0
                cpuScore = 0
                reset()
            if event.key == K_q or event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Create screen, background and text.
    screen.fill(BLACK)
    screen.blit(pongBackground, pongBack)

    playerText = bf.render(str(playerScore), False, WHITE, None)
    pText = playerText.get_rect()
    pText.centerx = 738  # 768
    pText.centery = 288
    cpuText = bf.render(str(cpuScore), False, WHITE, None)
    cText = cpuText.get_rect()
    cText.centerx = 288
    cText.centery = 288
    screen.blit(playerText, pText)
    screen.blit(cpuText, cText)

    # Create paddles
    screen.blit(playerCenterImage, playerCenter)
    screen.blit(playerTopImage, playerTop)
    screen.blit(playerBottomImage, playerBottom)
    screen.blit(cpuCenterImage, cpuCenter)
    screen.blit(cpuTopImage, cpuTop)
    screen.blit(cpuBottomImage, cpuBottom)

    # Create ball & dashed net
    screen.blit(pongBallImage, pongBall)
    screen.blit(pongNetImage, pongNet)

    # Move the player paddles
    if moveDown and playerCenter.bottom < WINDOWHEIGHT:
        playerCenter.top += MOVESPEED
    if moveUp and playerCenter.top > 0:
        playerCenter.top -= MOVESPEED
    if moveLeft and playerTop.left > WINDOWWIDTH / 2 and playerBottom.left > WINDOWWIDTH / 2:
        playerTop.left -= MOVESPEED
        playerBottom.left -= MOVESPEED
    if moveRight and playerTop.right < WINDOWWIDTH and playerBottom.right < WINDOWWIDTH:
        playerTop.right += MOVESPEED
        playerBottom.right += MOVESPEED

    # Move the CPU paddles according to ball, but at slower speed
    if pongBall.top < cpuCenter.top:
        if pongBall.top < 100:
            cpuCenter.centery -= CPUSPEED * 2
        else:
            cpuCenter.centery -= CPUSPEED
    elif pongBall.bottom > cpuCenter.bottom:
        if pongBall.bottom > 400:
            cpuCenter.centery += CPUSPEED * 2
        else:
            cpuCenter.centery += CPUSPEED

    if pongBall.left < cpuBottom.left and pongBall.left < cpuTop.left:
        if cpuBottom.left > 0 and cpuTop.left > 0:
            if pongBall.left < 100:
                cpuBottom.centerx -= CPUSPEED * 2
                cpuTop.centerx -= CPUSPEED * 2
            else:
                cpuBottom.centerx -= CPUSPEED * 2
                cpuTop.centerx -= CPUSPEED * 2
    elif pongBall.right > cpuBottom.right and pongBall.right > cpuTop.right:
        if cpuBottom.right < 500 and cpuTop.right < 500:
            if pongBall.right > 400:
                cpuBottom.centerx += CPUSPEED * 2
                cpuTop.centerx += CPUSPEED * 2
            else:
                cpuBottom.centerx += CPUSPEED
                cpuTop.centerx += CPUSPEED

    # Set movement of ball
    if ball['dir'] == 'downleft':
        ball['rect'].left -= MOVESPEED
        ball['rect'].top += MOVESPEED
    if ball['dir'] == 'downright':
        ball['rect'].left += MOVESPEED
        ball['rect'].top += MOVESPEED
    if ball['dir'] == 'upleft':
        ball['rect'].left -= MOVESPEED
        ball['rect'].top -= MOVESPEED
    if ball['dir'] == 'upright':
        ball['rect'].left += MOVESPEED
        ball['rect'].top -= MOVESPEED

    # Check for collision
    if ball['dir'] == 'downleft':
        # if hit CPU center
        if pongBall.colliderect(cpuCenter):
            # change to downright
            ball['dir'] = 'downright'
            hitSound.play()
        # if hit CPU bottom
        if pongBall.colliderect(cpuBottom):
            # change to upleft
            ball['dir'] = 'upleft'
            hitSound.play()
        # if hit player bottom
        if pongBall.colliderect(playerBottom):
            # change to upleft
            ball['dir'] = 'upleft'
            hitSound.play()
    if ball['dir'] == 'downright':
        # if hit player center
        if pongBall.colliderect(playerCenter):
            # change to downleft
            ball['dir'] = 'downleft'
            hitSound.play()
        # if hit player bottom
        if pongBall.colliderect(playerBottom):
            # change to upright
            ball['dir'] = 'upright'
            hitSound.play()
        # if hit CPU bottom
        if pongBall.colliderect(cpuBottom):
            # change to upright
            ball['dir'] = 'upright'
            hitSound.play()
    if ball['dir'] == 'upleft':
        # if hit CPU center
        if pongBall.colliderect(cpuCenter):
            # change to upright
            ball['dir'] = 'upright'
            hitSound.play()
        # if hit CPU top
        if pongBall.colliderect(cpuTop):
            # change to downleft
            ball['dir'] = 'downleft'
            hitSound.play()
        # if hit player top
        if pongBall.colliderect(playerTop):
            # change to downleft
            ball['dir'] = 'downleft'
            hitSound.play()
    if ball['dir'] == 'upright':
        # if hit player center
        if pongBall.colliderect(playerCenter):
            # change to upleft
            ball['dir'] = 'upleft'
            hitSound.play()
        # if hit player top
        if pongBall.colliderect(playerTop):
            # change to downright
            ball['dir'] = 'downright'
            hitSound.play()
        # if hit CPU top
        if pongBall.colliderect(cpuTop):
            # change to downright
            ball['dir'] = 'downright'
            hitSound.play()

    # Check for goal (or whether the box has moved out of the window)
    if ball['rect'].right < 0 \
            or (ball['rect'].top > WINDOWHEIGHT and ball['rect'].centerx < 512) \
            or (ball['rect'].bottom < 0 and ball['rect'].centerx < 512):
        # Player scores a goal
        winSound.play()
        playerScore += 1
        sleep(3)
        reset()
    if ball['rect'].left > WINDOWWIDTH \
            or (ball['rect'].top > WINDOWHEIGHT and ball['rect'].centerx > 512) \
            or (ball['rect'].bottom < 0 and ball['rect'].centerx > 512):
        # CPU scores a goal
        loseSound.play()
        cpuScore += 1
        sleep(3)
        reset()

    # Check for win
    if cpuScore >= 11 and cpuScore >= (playerScore - 2):
        # CPU wins
        cpuWin = bf.render("Computer player wins!", False, WHITE, BLACK)
        cWin = cpuWin.get_rect()
        cWin.centerx = 512
        cWin.centery = 288
        screen.blit(cpuWin, cWin)
        end_Game()
    if playerScore >= 11 and playerScore >= (cpuScore - 2):
        # Player wins
        playerWin = bf.render("The player wins!", False, WHITE, BLACK)
        pWin = playerWin.get_rect()
        pWin.centerx = 512
        pWin.centery = 288
        screen.blit(playerWin, pWin)
        end_Game()

    # Update screen
    pygame.display.flip()
    # Set clock to 60fps
    clock.tick(60)