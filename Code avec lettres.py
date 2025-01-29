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

BACKGROUND_COLOR = (112, 60, 27)

GRAVITY = 0.2

KEYS = {
    pygame.K_a: "A",
    pygame.K_z: "Z",
    pygame.K_e: "E",
    pygame.K_r: "R",
    pygame.K_t: "T",
    pygame.K_y: "Y"
}

# Police de texte
font = pygame.font.Font(None, 50)

# Fonction pour créer une nouvelle banane
def create_banana():
    return {
        'x': random.randint(100, WIDTH - 100),
        'y': HEIGHT,
        'speed_x': random.randint(-10, 10),
        'speed_y': random.randint(-20, -10),
        'throw': True,
        'cut': False,
        'required_key': random.choice(list(KEYS.keys()))  # Sélectionne une touche aléatoire parmi AZERTY
    }

banane = create_banana()

# Boucle principale
running = True
while running:
    screen.fill(BACKGROUND_COLOR)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == banane['required_key']:  
                if not banane['cut'] and 100 < banane['y'] < HEIGHT - 100:  
                    banane['cut'] = True  

    if banane['throw'] and not banane['cut']:
        banane['speed_y'] += GRAVITY  
        banane['x'] += banane['speed_x']
        banane['y'] += banane['speed_y']

        screen.blit(banane_img, (banane['x'], banane['y']))  

        
        key_text = font.render(KEYS[banane['required_key']], True, (255, 255, 255))
        screen.blit(key_text, (banane['x'] + 50, banane['y'] - 20))

        
        if banane['y'] > HEIGHT:
            banane = create_banana()  

   
    if banane['cut']:
        banane = create_banana()  

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
