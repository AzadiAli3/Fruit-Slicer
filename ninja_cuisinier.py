import pygame
import random

# Initialisation de Pygame
pygame.init()

# Définition des constantes
WIDTH, HEIGHT = 1280, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("None", 30)
FPS = 60

# Chargement des images de fruits
fruit_images = [
    pygame.image.load("images/fruits/pasteque-crop.gif"),
    pygame.image.load("images/fruits/banane-crop.gif"),
    pygame.image.load("images/fruits/coco-crop.gif"),
    pygame.image.load("images/fruits/citron-crop.gif"),
    pygame.image.load("images/fruits/pomme-crop.gif"),
    pygame.image.load("images/fruits/fraise-crop.gif"),
    pygame.image.load("images/fruits/poire-crop.gif"),
    pygame.image.load("images/fruits/orange-crop.gif"),
    pygame.image.load("images/fruits/dragon-crop.gif"),
    pygame.image.load("images/fruits/bleue-crop.gif"),
    pygame.image.load("images/fruits/rouge-crop.gif"),
    pygame.image.load("images/fruits/glace-crop.gif"),
    pygame.image.load("images/fruits/bombe-crop.gif"),
    pygame.image.load("images/fruits/grenade-crop.gif")
]

# Définition de la gravité
GRAVITY = 0.4

# Liste pour stocker les fruits en vol
fruits = []

def spawn_fruits():
    """Génère un nombre aléatoire de fruits et les ajoute à la liste avec des probabilités ajustées"""
    
    # Liste des fruits avec des poids en fonction des pourcentages désirés
    fruits_list = [
        ("pasteque-crop.gif", 10),  # 10% de chance
        ("banane-crop.gif", 10),    # 10% de chance
        ("coco-crop.gif", 10),      # 10% de chance
        ("citron-crop.gif", 8),     # 8% de chance
        ("pomme-crop.gif", 10),     # 10% de chance
        ("fraise-crop.gif", 8),     # 8% de chance
        ("poire-crop.gif", 8),      # 8% de chance
        ("orange-crop.gif", 10),    # 10% de chance
        ("dragon-crop.gif", 0.1),   # 0.1% de chance
        ("bleue-crop.gif", 0.5),    # 0.5% de chance
        ("rouge-crop.gif", 0.5),    # 0.5% de chance
        ("glace-crop.gif", 0.3),    # 0.3% de chance
        ("bombe-crop.gif", 2),      # 2% de chance
        ("grenade-crop.gif", 1)     # 1% de chance
    ]
    
    # Calculer la somme de tous les poids
    total_weight = sum(weight for _, weight in fruits_list)
    
    for _ in range(random.randint(1, 3)):  # Entre 1 et 3 fruits
        rand = random.uniform(0, total_weight)  # Choisir un nombre entre 0 et la somme des poids
        current_weight = 0
        
        # Choisir un fruit en fonction du nombre généré
        for fruit_name, weight in fruits_list:
            current_weight += weight
            if rand <= current_weight:
                fruit_image = pygame.image.load(f"images/fruits/{fruit_name}")
                break

        fruit = {
            'x': random.randint(100, WIDTH - 100),
            'y': HEIGHT,
            'speed_x': random.randint(-10, 10),
            'speed_y': random.randint(-25, -20),
            'throw': True,
            'image': fruit_image,
            'spin': random.randint(0, 360)
        }
        fruits.append(fruit)

# --- MENU PRINCIPAL ---
def menu():
    """Affichage du menu principal avec les options"""
    screen.blit(pygame.image.load("images/fond.png"), (0, 0))
    screen.blit(pygame.image.load("images/play.png"), (0, 50))
    screen.blit(pygame.image.load("images/diff.png"), (0, 270))
    pygame.display.update()

    choosing = True
    while choosing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    choosing = False  # Commence le jeu
                elif event.key == pygame.K_2:
                    choosing = False
                    difficulté = AppelÀLaFonctionDeDifficulté()  # Appelle la fonction de difficulté

# --- FONCTION PLACEHOLDER POUR LE CHOIX DE LA DIFFICULTÉ ---
def AppelÀLaFonctionDeDifficulté():
    """Fonction de sélection de la difficulté (à implémenter)"""
    pass

# Affichage du menu avant de commencer le jeu
menu()

# --- BOUCLE PRINCIPALE DU JEU ---
running = True
spawn_timer = 0  # Timer pour générer de nouveaux fruits

while running:
    screen.blit(pygame.image.load("images/fond.png"), (0, 0))

    # Gestion des événements (fermeture de la fenêtre)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Générer de nouveaux fruits toutes les 60 frames (~1 seconde)
    spawn_timer += random.randint(0, 3)
    if spawn_timer > 180:
        spawn_fruits()
        spawn_timer = 0

    # --- MOUVEMENT DES FRUITS ---
    for fruit in fruits[:]:  # Copier la liste pour éviter des erreurs lors de la suppression
        if fruit['throw']:
            fruit['speed_y'] += GRAVITY  # Appliquer la gravité
            fruit['x'] += fruit['speed_x']
            fruit['y'] += fruit['speed_y']

            # Gestion des rebonds sur les bords de l'écran
            if fruit['x'] < 0:
                fruit['x'] = 0
                fruit['speed_x'] = -fruit['speed_x']
            elif fruit['x'] > WIDTH - fruit['image'].get_width():
                fruit['x'] = WIDTH - fruit['image'].get_width()
                fruit['speed_x'] = -fruit['speed_x']
            
            fruit['spin'] += 1

            # Affichage du fruit
            screen.blit(pygame.transform.rotate(fruit['image'], fruit['spin']), (fruit['x'], fruit['y']))

            # Retirer le fruit s'il tombe en bas de l'écran
            if fruit['y'] > HEIGHT:
                fruits.remove(fruit)

    # Mise à jour de l'affichage et gestion du framerate
    pygame.display.update()
    clock.tick(FPS)

# --- FIN DU PROGRAMME ---
pygame.quit()
