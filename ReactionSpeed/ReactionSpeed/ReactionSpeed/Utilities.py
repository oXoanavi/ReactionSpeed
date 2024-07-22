import pygame
import random
from Variables import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, DIRECTIONS

def draw_arrow(screen, direction, x, y):
    """Main Arrow ok"""
    size = 50
    half_size = size // 2
    
    if direction == 'up':
        points = [(x, y - size), (x - half_size, y - half_size), (x + half_size, y - half_size)]
    elif direction == 'right':
        points = [(x + size, y), (x + half_size, y - half_size), (x + half_size, y + half_size)]
    elif direction == 'down':
        points = [(x, y + size), (x - half_size, y + half_size), (x + half_size, y + half_size)]
    elif direction == 'left':
        points = [(x - size, y), (x - half_size, y - half_size), (x - half_size, y + half_size)]
    
    pygame.draw.polygon(screen, WHITE, points)
    
    #For our Extra circle (This is where you click for accuracy)
    pygame.draw.circle(screen, WHITE, (x, y), 10)

def get_random_arrow():
    
    direction = random.choice(DIRECTIONS)
    x = random.randint(50, SCREEN_WIDTH - 50)
    y = random.randint(50, SCREEN_HEIGHT - 50)
    return direction, x, y
