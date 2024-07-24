import pygame
import time
import random
import csv
import matplotlib.pyplot as plt
from Utilities import draw_arrow, get_random_arrow
from Variables import SCREEN_WIDTH, SCREEN_HEIGHT, DARK_GRAY, WHITE, DIRECTIONS, MOVEMENT_KEYS

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Reaction Speed")

TIME_LIMIT = 2  #This will be the max time limit, up to 2 seconds
SCORE_FILE = 'reaction_speeds.csv'

def calculate_accuracy(cursor_x, cursor_y, arrow_x, arrow_y):
    distance = ((cursor_x - arrow_x) ** 2 + (cursor_y - arrow_y) ** 2) ** 0.5
    #Max distance of our arrow is 50
    max_distance = 50
    #Accuracy from 0 to 1
    accuracy = max(0, 1 - (distance / max_distance))
    return accuracy

def save_scores(record):
    #Saving as a CSV
    with open(SCORE_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        for reaction_time, accuracy in record:
            writer.writerow([reaction_time, accuracy])

def calculate_averages(record):
    if not record:
        return 0, 0
    total_reaction_time = sum(r[0] for r in record)
    total_accuracy = sum(r[1] for r in record)
    average_reaction_time = total_reaction_time / len(record)
    average_accuracy = total_accuracy / len(record)
    return average_reaction_time, average_accuracy

def plot_results(record):
    reaction_times = [r[0] for r in record]
    accuracies = [r[1] for r in record]
    
    plt.figure(figsize=(10, 5))
    
    plt.plot(reaction_times, accuracies, marker='o', linestyle='-', color='b')
    plt.title('Reaction Speed vs Accuracy')
    plt.xlabel('Reaction Time (ms)')
    plt.ylabel('Accuracy')
    
    plt.tight_layout()
    plt.savefig('results_chart.png')
    plt.show()

def game_loop():
    current_direction, arrow_x, arrow_y = get_random_arrow()
    start_time = time.time()
    record = []
    run = True

    while run:
        screen.fill(DARK_GRAY)
        
        #Drawing the arrow
        draw_arrow(screen, current_direction, arrow_x, arrow_y)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key in MOVEMENT_KEYS:
                    pressed_direction = MOVEMENT_KEYS[event.key]
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if pressed_direction == current_direction and (arrow_x - 50 < mouse_x < arrow_x + 50) and (arrow_y - 50 < mouse_y < arrow_y + 50):
                        reaction_time = round((time.time() - start_time) * 1000, 2)
                        accuracy = calculate_accuracy(mouse_x, mouse_y, arrow_x, arrow_y)
                        record.append((reaction_time, accuracy))
                        print(f"Reaction Time: {reaction_time} ms, Accuracy: {accuracy:.2f}")
                        # New arrow and to update the start time
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

    #Save the scores to the reaction_speed.csv
    save_scores(record)

    #This will be to calculate the average
    average_reaction_time, average_accuracy = calculate_averages(record)
    print(f"Average Reaction Time: {average_reaction_time:.2f} ms, Average Accuracy: {average_accuracy:.2f}")

    #Plotting
    plot_results(record)

    
    waiting_for_keypress = True
    while waiting_for_keypress:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                waiting_for_keypress = False
                return True

while True:
    if not game_loop():
        break

pygame.quit()
