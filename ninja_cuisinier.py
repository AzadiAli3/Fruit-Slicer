import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 1280, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("None", 30)
FPS = 60

banane_img = pygame.image.load("images/bloc.png")

GRAVITY = 0.4

banane = {
    'x': random.randint(100, WIDTH - 100),
    'y': HEIGHT,
    'speed_x': random.randint(-10, 10),
    'speed_y': random.randint(-30, -20),
    'throw': True
}

def menu():
    screen.fill((255, 255, 255))
    title = font.render("Salut !", True, (0, 0, 0))
    option1 = font.render("1 - Jouer", True, (80, 80, 80))
    option2 = font.render("2 - Difficulté", True, (80, 80, 80))
    screen.blit(title, (200, 150))
    screen.blit(option1, (200, 250))
    screen.blit(option2, (200, 300))
    pygame.display.update()

    choosing = True
    while choosing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    choosing = False
                elif event.key == pygame.K_2:
                    choosing = False
                    difficulté = AppelÀLaFonctionDeDifficulté()

def AppelÀLaFonctionDeDifficulté():
    "faut bien un truc pour une def"
    
menu()

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
        
        if banane['x'] < 0:
            banane['x'] = 0
            banane['speed_x'] = -banane['speed_x']
        elif banane['x'] > WIDTH - banane_img.get_width():
            banane['x'] = WIDTH - banane_img.get_width()
            banane['speed_x'] = -banane['speed_x']

        screen.blit(banane_img, (banane['x'], banane['y']))

        if banane['y'] > HEIGHT:
            banane['x'] = random.randint(100, WIDTH - 100)
            banane['y'] = HEIGHT
            banane['speed_x'] = random.randint(-10, 10)
            banane['speed_y'] = random.randint(-30, -20)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()