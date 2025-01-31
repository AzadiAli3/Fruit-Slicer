import pygame
import random

pygame.init()
WIDTH, HEIGHT = 1280, 750
screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont("None", 30)
running = True
KEYS = {
    pygame.K_a: "A",
    pygame.K_z: "Z",
    pygame.K_e: "E",
    pygame.K_r: "R",
    pygame.K_t: "T",
    pygame.K_y: "Y"
}

loose = False
bomb = {
    'x': random.randint(100, WIDTH - 100),
    'y': HEIGHT,
    'speed_x': random.randint(-10, 10),
    'speed_y': random.randint(-30, -20),
    'throw': True}

key_text = font.render(KEYS[bomb['required_key']], True, (255, 255, 255))
screen.blit(key_text, (bomb['x'] + 50, bomb['y'] - 20))

while running :
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == 'f':  
                    if not bomb['cut'] and 100 < bomb['y'] < HEIGHT - 100:  
                        bomb['cut'] = True
                        loose = True
