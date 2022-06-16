import pygame
from pygame import init,font, display, time, image, Rect, draw, key
import random
import os
import sys

"""
Pong

Remake of classic game by cd-con(eel-primo), 2022
"""
# Init
init()
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
C_DEBUG = (255,64,128)

FONT = font.Font(resource_path('font.ttf'), 30)
D_FONT = font.Font(resource_path('font.ttf'), 8)

# Setup pygame window
GAME_RUNNING = True
DRAW_DEBUG = False
GAME_CLOCK = time.Clock()
GAME_DISPLAY = display.set_mode(tuple(SCREEN_SIZE))
display.set_caption("Pong!")
display.set_icon(image.load(resource_path('icons\\icon_smooth.ico')))

# Player vars
PLAYER_SIZE = (8,32)
first_player_y, second_player_y, first_player_score, second_player_score = 0,0,0,0

# Ball vars
BALL_SIZE = 5
ball_position = [0,0]
ball_direction = [False, False]
bounce_count = 0

# Timer vars
minutes = 0
seconds = [0,0]

# Restart game
def restart_game(reset_count = False):
    global first_player_y, second_player_y, first_player_score, second_player_score, \
           ball_position, ball_direction, minutes, seconds, GAME_PAUSED
    pygame.event.clear()
    minutes = 0; seconds = [0,0]

    first_player_y, second_player_y = SCREEN_SIZE[1] / 2 - PLAYER_SIZE[1] / 2, \
                                      SCREEN_SIZE[1] / 2 - PLAYER_SIZE[1] / 2
    ball_position = [SCREEN_SIZE[0] / 2,SCREEN_SIZE[1] / 2 + 50 * random.randint(-2,2)]

    if reset_count:
        first_player_score, second_player_score = 0, 0
        ball_direction = [bool(random.getrandbits(1)), bool(random.getrandbits(1))]

# Handle collisions
def intersect(obj, ball):
    # Debug
    t_rect = Rect(obj.left, obj.top - 3, obj.width, 2)
    b_rect = Rect(obj.left, obj.bottom + 2, obj.width, 2)
    l_rect = Rect(obj.left - 3, obj.top, 2, obj.height)
    r_rect = Rect(obj.right + 2, obj.top, 2, obj.height)
    if DRAW_DEBUG:
        draw.rect(GAME_DISPLAY, C_DEBUG, t_rect)
        draw.rect(GAME_DISPLAY, C_DEBUG, b_rect)
        draw.rect(GAME_DISPLAY, C_DEBUG, l_rect)
        draw.rect(GAME_DISPLAY, C_DEBUG, r_rect)

    edges = dict(left = l_rect, right = r_rect,
        top = t_rect, bottom = b_rect)
    collisions = set(edge for edge, rect in edges.items() if ball.colliderect(rect))
    
    # Debug
    if DRAW_DEBUG: GAME_DISPLAY.blit(D_FONT.render("Obj collisions with ball: " + str(list(collisions)), False, C_DEBUG),(5,15))
    
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

time.set_timer(pygame.USEREVENT,1000)
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

        if event.type == pygame.USEREVENT:
            print(random.choice(['tick','tock','tack']))
            seconds[1] += 1
            if seconds[1] > 9: seconds[1] = 0; seconds[0] += 1
            if seconds[0] == 5: seconds = [0,0]; minutes += 1

        # Reload game if 'R' button is pressed
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            time.delay(1000)
            restart_game(True)
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F2:
            DRAW_DEBUG = not DRAW_DEBUG
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F5: FPS += 5
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F4: FPS -= 5

    """
    Proceed keyboard input and player control
    Not the best solution
    """
    try:
        keys = key.get_pressed()
    except pygame.error:
        sys.exit()
    # Debug
        
    GAME_DISPLAY.blit(D_FONT.render("Target FPS:" + str(FPS), False, C_DEBUG),(5,0))
    
    target_player_speed = PLAYER_SPEED + bounce_count * 0.025

    # First player control
    if keys[pygame.K_w] and first_player_y - target_player_speed > 0:
            first_player_y -= target_player_speed

    if keys[pygame.K_s] and first_player_y + PLAYER_SIZE[1] + target_player_speed < SCREEN_SIZE[1]:
            first_player_y += target_player_speed

    # Second player control
    if keys[pygame.K_UP] and second_player_y - target_player_speed > 0:
        second_player_y -= target_player_speed

    if keys[pygame.K_DOWN] and second_player_y + PLAYER_SIZE[1] + target_player_speed < SCREEN_SIZE[1]:
        second_player_y += target_player_speed

    """
    Score logic
    """
    # If first player reach goal -> win!
    if first_player_score == MAX_SCORE:
        GAME_DISPLAY.blit(FONT.render("Player 1 won!", False, C_WHITE), (SCREEN_SIZE[0] / 2 - 220 ,SCREEN_SIZE[1] / 2 - 120))
        display.update()
        time.delay(2000)
        restart_game(True)
            
    # If second player reach goal -> win!
    if second_player_score == MAX_SCORE:
        GAME_DISPLAY.blit(FONT.render("Player 2 won!", False, C_WHITE), (SCREEN_SIZE[0] / 2 - 220 ,SCREEN_SIZE[1] / 2 - 120))
        display.update()
        time.delay(2000)
        restart_game(True)

    """
    Ball logic
    """
    # Ball movement
    # X-direction
    if ball_direction[0]:
        ball_position[0] += BALL_SPEED + bounce_count * 0.1
    else:
        ball_position[0] -= BALL_SPEED + bounce_count * 0.1

    # Y-direction
    if ball_direction[1]:
        ball_position[1] += BALL_SPEED + bounce_count * 0.1
    else:
        ball_position[1] -= BALL_SPEED + bounce_count * 0.1

    # Bounce off the side walls
    if  ball_position[1] + BALL_SIZE * 2 > SCREEN_SIZE[1] or ball_position[1] < BALL_SIZE * 2:
        bounce_count += 1
        ball_direction[1] = not ball_direction[1]
    
    # Add a score for the second player if ball hit the left side of the screen
    if ball_position[0] < BALL_SIZE * 2:
        second_player_score += 1
        bounce_count = 0
        time.wait(3000)        
        # Throw ball in side of second player
        ball_direction[0] = False
        restart_game()
    
    # Add a score for the first player if ball hit the right side of the screen
    if ball_position[0] + BALL_SIZE * 2 > SCREEN_SIZE[0]:
        first_player_score += 1     
        bounce_count = 0 
        time.delay(3000)
        # Throw ball in side of first player
        ball_direction[0] = True        
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
    GAME_DISPLAY.blit(FONT.render(str(first_player_score), False, C_WHITE), (SCREEN_SIZE[0] / 4, 10))
    GAME_DISPLAY.blit(FONT.render(str(second_player_score), False, C_WHITE), (SCREEN_SIZE[0] * 3 / 4 - 24, 10))

    # Draw players
    # First player
    p1 = draw.rect(GAME_DISPLAY, C_WHITE, (40, first_player_y, 
                                            PLAYER_SIZE[0],
                                            PLAYER_SIZE[1]), 1)
    # Second player
    p2 = draw.rect(GAME_DISPLAY, C_WHITE, (SCREEN_SIZE[0] - PLAYER_SIZE[0] - 40, second_player_y, 
                                            PLAYER_SIZE[0],
                                            PLAYER_SIZE[1]), 1)

    # Draw ball
    ball = draw.circle(GAME_DISPLAY, C_WHITE, tuple(ball_position), 5, 1)

    # Check ball collision
    #if ball.collidelist([p1,p2]) > -1:
    edges = (intersect(p1, ball), intersect(p2, ball))
    if edges[0] in ('top', 'bottom') or edges[1] in ('top', 'bottom'):
        ball_direction[1] = not ball_direction[1]
    elif edges[0] == 'right' or edges[1] == 'left':
        ball_direction[0] = not ball_direction[0]

    # Draw line
    for x in range(int(SCREEN_SIZE[1] / 20) - 1):
        draw.rect(GAME_DISPLAY, C_GRAY, (SCREEN_SIZE[0] / 2, x * 20 + 3, 2, 10))

    # Debug
    if DRAW_DEBUG: GAME_DISPLAY.blit(D_FONT.render("Ball pos: " + str(ball_position), False, C_DEBUG),(5,30))
    GAME_DISPLAY.blit(D_FONT.render(str(minutes) + ":" + str(seconds[0]) + str(seconds[1]), False, C_WHITE),(SCREEN_SIZE[0]/2 - 13, SCREEN_SIZE[1] * 31 / 32))
    pygame.display.update()
    GAME_CLOCK.tick(FPS)
