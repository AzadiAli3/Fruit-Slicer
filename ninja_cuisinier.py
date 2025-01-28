import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1280, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60

try:
    banane_img = pygame.image.load("images/banane.png")
except pygame.error as e:
    print(f"Erreur de chargement de l'image : {e}")
    pygame.quit()
    exit()

GRAVITY = 0.5

banane = {
    'x': random.randint(100, WIDTH - 100),
    'y': HEIGHT,
    'speed_x': random.randint(-10, 10),
    'speed_y': random.randint(-20, -10),
    'throw': True
}

running = True
while running:
    screen.fill((112, 60, 27))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if banane['throw']:
        banane['speed_y'] += GRAVITY 
        banane['x'] += banane['speed_x']
        banane['y'] += banane['speed_y']

        screen.blit(banane_img, (banane['x'], banane['y']))

        if banane['y'] > HEIGHT:
            banane['x'] = random.randint(100, WIDTH - 100)
            banane['y'] = HEIGHT
            banane['speed_x'] = random.randint(-10, 10)
            banane['speed_y'] = random.randint(-30, -20)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
