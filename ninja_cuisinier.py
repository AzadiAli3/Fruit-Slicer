import pygame
import random
import time
import json

# Initialization of Pygame
pygame.init()
pygame.mixer.init()
# Load the sound
# sound1 = pygame.mixer.Sound("son/slicer.mp3")
# sound2 = pygame.mixer.Sound("son/slicermenu.mp3")

# Definition of constants
WIDTH, HEIGHT = 1280, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("None", 30)
FPS = 60
GRAVITY = 0.4

# Restart game
def everything():
    # Open json file
    with open('score.json', 'r') as f:
        data = json.load(f)
    
    # Set the value from zero
    best_score = data["best_score"]
    difficulty = 'mid'
    slow = 1
    slow_duration = 0
    fruits = []
    combo_count = 0
    combo_duration = 0
    current_score = 0
    lifes = 3
    frenzy = False
    frenzy_duration = 0
    frenzy_bonus = 0

    # Spawn fruit
    def spawn_fruits():
        
        fruits_list = [
            ("pasteque.gif", 10),  # 10% de chance
            ("banane.gif", 10),    # 10% de chance
            ("coco.gif", 10),      # 10% de chance
            ("citron.gif", 8),     # 8% de chance
            ("pomme.gif", 10),     # 10% de chance
            ("fraise.gif", 8),     # 8% de chance
            ("poire.gif", 8),      # 8% de chance
            ("orange.gif", 10),    # 10% de chance
            ("dragon.gif", 0.1),   # 0.1% de chance
            ("bleue.gif", 0.5),    # 0.5% de chance
            ("rouge.gif", 0.5),    # 0.5% de chance
            ("glace.gif", 0.3),    # 0.3% de chance
            ("bombe.gif", 5),      # 5% de chance
            ("grenade.gif", 1)     # 1% de chance
        ]

        # Spawn only normal fruit in frenzy mode
        if frenzy:
            fruits_list = [(name, weight) for name, weight in fruits_list if name not in ["dragon.gif", "glace.gif", "bleue.gif", "rouge.gif", "bombe.gif", "grenade.gif"]]
        
        total_weight = sum(weight for _, weight in fruits_list)

        # Manage the fruit spawn rate
        if frenzy:
            actual_difficulty = random.randint(5, 7)
        elif difficulty == 'easy':
            actual_difficulty = random.randint(1, 3)
        elif difficulty == 'mid':
            actual_difficulty = random.randint(2, 4)
        elif difficulty == 'hard':
            actual_difficulty = random.randint(3, 5)
        
        # Choose a random fruit in relation to their chance to be picked
        for _ in range(actual_difficulty):
            rand = random.uniform(0, total_weight)
            current_weight = 0
            
            for fruit_name, weight in fruits_list:
                current_weight += weight
                if rand <= current_weight:
                    fruit_image = pygame.image.load(f"images/fruits/{fruit_name}")
                    break

            # Give fruit initial value
            fruit = {
                'x': random.randint(100, WIDTH - 100),
                'y': HEIGHT,
                'speed_x': random.randint(-10, 10),
                'speed_y': random.randint(-25, -20),
                'throw': True,
                'image': fruit_image,
                'spin': random.randint(0, 360),
                'cut': False,
                'required_key': random.choice(list(KEYS.keys())),
                'image_name': fruit_name
            }
            fruits.append(fruit)

    # happen when a fruit is cut
    def cutting_fruit(fruit, slow_duration, current_score, frenzy):
        # Take the name of the fruit cut
        fruit_extension = fruit['image_name'].split('.')[0]   

        # Manage which fruit make what
        if fruit_extension in ['pasteque', 'banane', 'coco', 'citron', 'pomme', 'fraise', 'poire', 'orange']:
            current_score += 1
        if fruit_extension == 'dragon' :
            current_score += 50
        if fruit_extension == 'glace':
            current_score += 1
            fruit['cut'] = True
            slow_duration = 60
            return [], slow_duration, current_score, frenzy
        if fruit_extension == 'bleue':
            current_score += 1
            fruit['cut'] = True
            return [], slow_duration, current_score, frenzy
        if fruit_extension == 'rouge':
            current_score += 1
            fruit['cut'] = True
            frenzy = True
            return [], slow_duration, current_score, frenzy
        if fruit_extension == 'grenade':
            current_score += 1
            fruit['cut'] = True
            return [], slow_duration, current_score, frenzy
        if fruit_extension == 'bombe':
            fruit['cut'] = True
            game_over()
            return [], slow_duration, current_score, frenzy
        
        # replace the fruit with itd two pieces
        left_piece = fruit.copy()
        right_piece = fruit.copy()

        try:
            left_piece['image'] = pygame.image.load(f"images/coupe/{fruit_extension}_gauche.gif")
            right_piece['image'] = pygame.image.load(f"images/coupe/{fruit_extension}_droite.gif")
        except:
            return  

        left_piece['speed_x'] = fruit['speed_x'] - random.uniform(2, 5)
        right_piece['speed_x'] = fruit['speed_x'] + random.uniform(2, 5)
        left_piece['speed_y'] = fruit['speed_y'] * 0.8
        right_piece['speed_y'] = fruit['speed_y'] * 0.8

        fruit['cut'] = True

        left_piece['is_piece'] = True
        right_piece['is_piece'] = True

        return [left_piece, right_piece], slow_duration, current_score, frenzy


    # Main menu
    def menu(difficulty, begin):
        # sound2.play(loops=-1, fade_ms=2000)
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
                    if event.key == pygame.K_1: # Launch the game
                        begin = False
                        choosing = False
                        # sound2.fadeout(2000)
                        time.sleep(1)
                        # sound1.play(loops=-1, fade_ms=2000)
                    elif event.key == pygame.K_2: # Sent to choice of difficulty
                        choosing = False
                        difficulty = choose_difficulty(difficulty)
        return difficulty, begin
    
    # Allows you to choose the difficulty
    def choose_difficulty(difficulty):
        choosing = True
        while choosing:
            screen.fill((255, 0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_1:
                        difficulty = 'easy'
                        choosing = False
                    elif event.key == pygame.K_2:
                        difficulty = 'mid'
                        choosing = False
                    elif event.key == pygame.K_3:
                        difficulty = 'hard'
                        choosing = False
        return difficulty
    
    # Make loose the game
    def game_over():
        y = -HEIGHT
        while y <= 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            screen.blit(pygame.image.load("images/fond.png"), (0, 0))
            screen.blit(pygame.image.load("images/fail.png"), (0, y))
            screen.blit(pygame.image.load("images/restart.png"), (0, y + 200))

            pygame.display.update()

            y += 187.5 # Animate the loosing screen with a sliding effect

        choosing = True
        while choosing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        choosing = False
                        everything()

    # Update the best score
    def update_best_score(current_score, best_score):
        with open('score.json', 'r') as f:
            data = json.load(f)
        
        best_score = data["best_score"]
        if current_score > best_score: # compares scores to modify the best score if it's exceeded
            data["best_score"] = current_score
            with open('score.json', 'w') as f:
                json.dump(data, f)
            best_score = current_score
        return current_score, best_score










    # Start of the main loops
    begin = True
    while begin:
        difficulty, begin = menu(difficulty, begin)


    # Set the keys to use due to their difficulty
    if difficulty == 'easy':
        KEYS = {
            pygame.K_a: "A",
            pygame.K_z: "Z",
            pygame.K_e: "E",
            pygame.K_r: "R",
            pygame.K_t: "T",
            pygame.K_y: "Y",
            pygame.K_u: "U",
            pygame.K_i: "I",
            pygame.K_o: "O",
            pygame.K_p: "P"
        }
    elif difficulty == 'mid':
        KEYS = {
            pygame.K_q: "Q",
            pygame.K_s: "S",
            pygame.K_d: "D",
            pygame.K_f: "F",
            pygame.K_g: "G",
            pygame.K_h: "H",
            pygame.K_j: "J",
            pygame.K_k: "K",
            pygame.K_l: "L",
            pygame.K_m: "M",
            pygame.K_w: "W",
            pygame.K_x: "X",
            pygame.K_c: "C",
            pygame.K_v: "V",
            pygame.K_b: "B",
            pygame.K_n: "N"
        }
    elif difficulty == 'hard':
        KEYS = {
            pygame.K_a: "A",
            pygame.K_z: "Z",
            pygame.K_e: "E",
            pygame.K_r: "R",
            pygame.K_t: "T",
            pygame.K_y: "Y",
            pygame.K_u: "U",
            pygame.K_i: "I",
            pygame.K_o: "O",
            pygame.K_p: "P",
            pygame.K_q: "Q",
            pygame.K_s: "S",
            pygame.K_d: "D",
            pygame.K_f: "F",
            pygame.K_g: "G",
            pygame.K_h: "H",
            pygame.K_j: "J",
            pygame.K_k: "K",
            pygame.K_l: "L",
            pygame.K_m: "M",
            pygame.K_w: "W",
            pygame.K_x: "X",
            pygame.K_c: "C",
            pygame.K_v: "V",
            pygame.K_b: "B",
            pygame.K_n: "N"
        }
    

    # The MAIN loop
    running = True
    spawn_timer = 0  # Timer to generate new fruits
    fruits_to_add = []  # Temporary list to add cut fruit pieces

    while running:
        screen.blit(pygame.image.load("images/fond.png"), (0, 0))

        # The slow effect from the ice banana
        slow_duration -= 0.5
        if slow_duration >= 0:
            slow = 0.5
            screen.blit(pygame.image.load("images/glace.png"), (0, 0))
        else:
            slow = 1
        
        # Display of numerical values
        font = pygame.font.Font(None, 36)
        text_combo = font.render(f"Combo count: {combo_count}", True, (0, 0, 0))
        text_score = font.render(f"Score: {current_score}", True, (0, 0, 0))
        text_best_score = font.render(f"Best Score: {best_score}", True, (0, 0, 0))
        text_life = font.render(f"lives: {lifes}", True, (0, 0, 0))
        screen.blit(text_combo, (20, 20))
        screen.blit(text_score, (20, 60))
        screen.blit(text_best_score, (20, 100))
        screen.blit(text_life, (20, 140))

        combo_duration -= 0.5
        frenzy_bonus -= 0.5

        # Manage the frenzy timer
        if not frenzy:
            frenzy_duration = 100
        if frenzy:
            frenzy_bonus = 100
            frenzy_duration -= 0.5
            if frenzy_duration <= 0:
                frenzy = False

        # Event management
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                for fruit in fruits:
                    # Check that the fruit is not a piece and has not already been cut
                    if event.key == fruit['required_key'] and not fruit['cut'] and not fruit.get('is_piece', False):
                        morceaux, slow_duration, current_score, frenzy = cutting_fruit(fruit, slow_duration, current_score, frenzy)
                        if fruit['cut']:
                            combo_duration = 40
                            combo_count += 1
                        if morceaux:
                            fruits_to_add.extend(morceaux)

        # Generate new fruits every 60 frames
        spawn_timer += random.randint(0, 3)
        if frenzy:
            if spawn_timer > 30:
                spawn_fruits()
                spawn_timer = 0
        elif not frenzy:
            if spawn_timer > 180:
                spawn_fruits()
                spawn_timer = 0

        # Fruit movement
        for fruit in fruits[:]:  # Copy the list to avoid errors when deleting
            if fruit['throw'] and not fruit['cut']:
                fruit['speed_y'] += GRAVITY  # Apply gravity
                fruit['x'] += fruit['speed_x']
                fruit['y'] += fruit['speed_y']

                # Managing bounces at the edges of the screen
                if fruit['x'] < 0:
                    fruit['x'] = 0
                    fruit['speed_x'] = -fruit['speed_x']
                elif fruit['x'] > WIDTH - fruit['image'].get_width():
                    fruit['x'] = WIDTH - fruit['image'].get_width()
                    fruit['speed_x'] = -fruit['speed_x']
                
                fruit['spin'] += 1
                
                # Fruit display
                screen.blit(pygame.transform.rotate(fruit['image'], fruit['spin']), (fruit['x'], fruit['y']))

                # Display of the key only if the fruit is not a piece
                if not fruit.get('is_piece', False):
                    key_text = font.render(KEYS[fruit['required_key']], True, (255, 255, 255))
                    screen.blit(key_text, (fruit['x'] + 50, fruit['y'] - 20))

                # Remove the fruit if it falls to the bottom of the screen
                if fruit['y'] > HEIGHT:
                    fruits.remove(fruit)
                
                current_score, best_score = update_best_score(current_score, best_score)

                
                # When a fruit is not cut and falls to the bottom of the screen lose 1 life
                if not frenzy and frenzy_bonus <= 0:
                    fruit_uncut = fruit['image_name'].split('.')[0] 
                    if fruit['y'] > HEIGHT and not fruit['cut'] and not fruit.get('is_piece', False) and fruit_uncut in ['pasteque', 'banane', 'coco', 'citron', 'pomme', 'fraise', 'poire', 'orange']:
                        lifes -= 1
                else:
                    continue
        
        # Loses when lives are lost
        if lifes == 0:
            game_over()
                
        # Add the combo to the score if the combo is above 3 and the timer is end
        if combo_count >= 3 and combo_duration <= 0:
            current_score += combo_count
            combo_count = 0
        elif combo_count < 3 and combo_duration <= 0:
            combo_count = 0

        # Add fruit pieces to master list
        fruits.extend(fruits_to_add)
        fruits_to_add.clear()  # Empty temporary list

        # Display update and framerate management
        pygame.display.update()
        clock.tick(FPS * slow)

    # End of program
    pygame.quit()
everything()