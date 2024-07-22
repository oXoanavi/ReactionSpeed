import pygame
import time
import random
import os
import csv
from Utilities import draw_arrow, get_random_arrow
from Variables import SCREEN_WIDTH, SCREEN_HEIGHT, DARK_GRAY, WHITE, DIRECTIONS, MOVEMENT_KEYS

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Reaction Speed")

TIME_LIMIT = 2  #This will be the max time limit, upto 2 seconds lang
SCORE_FILE = 'reaction_speeds.csv'

current_direction, arrow_x, arrow_y = get_random_arrow()
start_time = time.time()
record = []

def calculate_accuracy(cursor_x, cursor_y, arrow_x, arrow_y):
    
    distance = ((cursor_x - arrow_x) ** 2 + (cursor_y - arrow_y) ** 2) ** 0.5
    #Max distance of our arrow is 50
    max_distance = 50
    #Accuracy from 0 to 1
    accuracy = max(0, 1 - (distance / max_distance))
    return accuracy

def save_scores(record):
    # Saving as a CSV
    with open(SCORE_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        for reaction_time, accuracy in record:
            writer.writerow([reaction_time, accuracy])

run = True
while run:
    screen.fill(DARK_GRAY)
    
    #Drawing the arrow
    draw_arrow(screen, current_direction, arrow_x, arrow_y)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key in MOVEMENT_KEYS:
                pressed_direction = MOVEMENT_KEYS[event.key]
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if pressed_direction == current_direction and (arrow_x - 50 < mouse_x < arrow_x + 50) and (arrow_y - 50 < mouse_y < arrow_y + 50):
                    reaction_time = round((time.time() - start_time) * 1000, 2)
                    accuracy = calculate_accuracy(mouse_x, mouse_y, arrow_x, arrow_y)
                    record.append((reaction_time, accuracy))
                    print(f"Reaction Time: {reaction_time} ms, Accuracy: {accuracy:.2f}")
                    #New arrow and to update the start time
                    current_direction, arrow_x, arrow_y = get_random_arrow()
                    start_time = time.time()
                else:
                    print("Wrong input!")
                    run = False
            else:
                print("Invalid key!")
                run = False

    #Our time limit
    if time.time() - start_time > TIME_LIMIT:
        print("Time's up!")
        run = False

    pygame.display.flip()

#Save the score on the reaction_speed.csv
save_scores(record)
pygame.quit()
