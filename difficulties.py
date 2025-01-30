import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont("None", 30)


WIDTH, HEIGHT = 1280, 750
difficulty = "Normal"
fruit = {
    'x': random.randint(100, WIDTH - 100),
    'y': HEIGHT,
    'speed_x': random.randint(-10, 10),
    'speed_y': random.randint(-30, -20),
    'throw': True
}

def diff(difficulty):
    chosing = True
    while chosing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    chosing = False
                    GRAVITY = 0.2
                    fruit["speed_y"] * 0.7
                    menu(difficulty)
                    return difficulty
                elif event.key == pygame.K_2:
                    chosing = False
                    GRAVITY = 0.4
                    fruit['speed_y'] += 1
                    menu(difficulty)
                    return difficulty
                elif event.key == pygame.K_3:
                    chosing = False
                    GRAVITY = 0.7
                    fruit["speed_y"] += 2
                    menu(difficulty)
                    return difficulty

diff(difficulty)

