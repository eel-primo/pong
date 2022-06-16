import pygame
from pygame import time
from pygame import draw
from pygame import font
from pygame import Rect
import random
import os
import sys

"""
Pong

Remake of classic game by cd-con(eel-primo), 2022
"""
# Init
pygame.init()
font.init()

# Import for Pyinstaller
def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.abspath(relative)

# Configuration
FPS = 30
MAX_SCORE = 10
PLAYER_SPEED = 10
BALL_SPEED = 7
SCREEN_SIZE = [800, 600]

# Colors
C_WHITE = (255,255,255)
C_GRAY = (128,128,128)

FONT = pygame.font.Font(resource_path('font.ttf'), 30)

# Setup pygame window
GAME_RUNNING = True
GAME_CLOCK = time.Clock()
GAME_DISPLAY = pygame.display.set_mode(tuple(SCREEN_SIZE))
pygame.display.set_caption("Pong!")
pygame.display.set_icon(pygame.image.load(resource_path('icons\\icon_smooth.ico')))

# Player vars
PLAYER_SIZE = (16,64)
player1_pos, player2_pos, player1_score, player2_score = 0,0,0,0

# Ball vars
BALL_SIZE = 5
ball_pos = [300,200]
ball_dir = [False, False]
bounce_count = 0

# Restart game
def restart_game(reset_count = False):
    global player1_pos, player2_pos, player1_score, player2_score, ball_pos, ball_dir
    player1_pos, player2_pos = SCREEN_SIZE[1] / 2 - PLAYER_SIZE[1] / 2, SCREEN_SIZE[1] / 2 - PLAYER_SIZE[1] / 2
    ball_pos = [SCREEN_SIZE[0] / 2,SCREEN_SIZE[1] / 2 + 50 * random.randint(-2,2)]
    if reset_count: player1_score, player2_score = 0, 0; ball_dir = [bool(random.getrandbits(1)), bool(random.getrandbits(1))]

# Handle collisions
def intersect(obj, ball):
    edges = dict(left=Rect(obj.left, obj.top, 1, obj.height), right=Rect(obj.right, obj.top, 1, obj.height),
        top=Rect(obj.left, obj.top, obj.width, 1), bottom=Rect(obj.left, obj.bottom, obj.width, 1))
    collisions = set(edge for edge, rect in edges.items() if ball.collidelist([rect]) > -1)

    if not collisions: return None

    if len(collisions) == 1:
        return list(collisions)[0]

    if 'top' in collisions:
        if ball.centery >= obj.top:
            return 'top'
        if ball.centerx < obj.left:
            return 'left'
        else:
            return 'right'

    if 'bottom' in collisions:
        if ball.centery >= obj.bottom:
            return 'bottom'
        if ball.centerx < obj.left:
            return 'left'
        else:
            return 'right'

restart_game()

# Main loop
while GAME_RUNNING:
    # Clear display after running all cycle
    GAME_DISPLAY.fill((0,0,0))

    """
    Proceed events from pygame
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            GAME_RUNNING = False

        # Reload game if 'R' button is pressed
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            pygame.time.delay(1000)
            restart_game(True)

    """
    Proceed keyboard input and player control
    Not the best solution
    """
    try:
        keys = pygame.key.get_pressed()
    except pygame.error:
        sys.exit()
    target_player_speed = PLAYER_SPEED + bounce_count * 0.025

    # First player control
    if keys[pygame.K_w] and player1_pos - target_player_speed > 0:
            player1_pos -= target_player_speed

    if keys[pygame.K_s] and player1_pos + PLAYER_SIZE[1] + target_player_speed < SCREEN_SIZE[1]:
            player1_pos += target_player_speed

    # Second player control
    if keys[pygame.K_UP] and player2_pos - target_player_speed > 0:
        player2_pos -= target_player_speed

    if keys[pygame.K_DOWN] and player2_pos + PLAYER_SIZE[1] + target_player_speed < SCREEN_SIZE[1]:
        player2_pos += target_player_speed

    """
    Score logic
    """
    # If first player reach goal -> win!
    if player1_score == MAX_SCORE:
        GAME_DISPLAY.blit(FONT.render("Player 1 won!", False, C_WHITE), (SCREEN_SIZE[0] / 2 - 220 ,SCREEN_SIZE[1] / 2 - 120))
        pygame.display.update()
        pygame.time.delay(5000)
        restart_game(True)
            
    # If second player reach goal -> win!
    if player2_score == MAX_SCORE:
        GAME_DISPLAY.blit(FONT.render("Player 2 won!", False, C_WHITE), (SCREEN_SIZE[0] / 2 - 220 ,SCREEN_SIZE[1] / 2 - 120))
        pygame.display.update()
        pygame.time.delay(5000)
        restart_game(True)

    """
    Ball logic
    """
    # Ball movement
    # X-direction
    if ball_dir[0]:
        ball_pos[0] += BALL_SPEED + bounce_count * 0.1
    else:
        ball_pos[0] -= BALL_SPEED + bounce_count * 0.1

    # Y-direction
    if ball_dir[1]:
        ball_pos[1] += BALL_SPEED + bounce_count * 0.1
    else:
        ball_pos[1] -= BALL_SPEED + bounce_count * 0.1

    # Bounce off the side walls
    if  ball_pos[1] + BALL_SIZE * 2 > SCREEN_SIZE[1] or ball_pos[1] < BALL_SIZE * 2:
        bounce_count += 1
        ball_dir[1] = not ball_dir[1]
    
    # Add a score for the second player if ball hit the left side of the screen
    if ball_pos[0] < BALL_SIZE * 2:
        player2_score += 1
        bounce_count = 0

        # Pass timer if last round
        if not player2_score == MAX_SCORE: pygame.time.wait(3000)
        
        # Throw ball in side of second player
        ball_dir[0] = False
        restart_game()
    
    # Add a score for the first player if ball hit the right side of the screen
    if ball_pos[0] + BALL_SIZE * 2 > SCREEN_SIZE[0]:
        player1_score += 1     
        bounce_count = 0   

        # Pass timer if last round
        if not player1_score == MAX_SCORE: pygame.time.wait(3000)

        # Throw ball in side of first player
        ball_dir[0] = True        
        restart_game()

    """
    Drawing graphics

    Order to draw
    0 - UI
    1 - Players
    2 - Ball
    3 - Decor (background)
    """        
    
    # Draw UI
    GAME_DISPLAY.blit(FONT.render(str(player1_score), False, C_WHITE), (SCREEN_SIZE[0] / 4, 10))
    GAME_DISPLAY.blit(FONT.render(str(player2_score), False, C_WHITE), (SCREEN_SIZE[0] * 3 / 4 - 24, 10))

    # Draw players
    # First player
    p1 = draw.rect(GAME_DISPLAY, C_WHITE, (40, player1_pos, 
                                            PLAYER_SIZE[0],
                                            PLAYER_SIZE[1]), 1)
    # Second player
    p2 = draw.rect(GAME_DISPLAY, C_WHITE, (SCREEN_SIZE[0] - PLAYER_SIZE[0] - 40, player2_pos, 
                                            PLAYER_SIZE[0],
                                            PLAYER_SIZE[1]), 1)

    # Draw ball
    ball = draw.circle(GAME_DISPLAY, C_WHITE, tuple(ball_pos), 5, 1)

    # Check ball collision
    if ball.collidelist([p1,p2]) > -1:
        edge = intersect(p1, ball)
        print("Edge1 = ", edge)
        edge2 = intersect(p2, ball)
        print("Edge2 = ", edge2)
        if edge in ('top', 'bottom') or edge2 in ('top', 'bottom'):
            ball_dir[0] = not ball_dir[0]
            ball_dir[1] = not ball_dir[1]
        elif edge == 'right' or edge2 == 'left':
            ball_dir[0] = not ball_dir[0]

    # Draw line
    for x in range(int(SCREEN_SIZE[1] / 20)):
        draw.rect(GAME_DISPLAY, C_GRAY, (SCREEN_SIZE[0] / 2, x * 20 + 3, 2, 10))

    pygame.display.update()
    GAME_CLOCK.tick(FPS)
