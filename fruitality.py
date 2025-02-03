import pygame
import random
import time
import json

# Initialization of Pygame
pygame.init()
pygame.mixer.init()

pygame.display.set_caption("Fruitality")
icon = pygame.image.load("images/fruits/icon.gif")  # Load an image
pygame.display.set_icon(icon)  # Define icon

# Load the sound
Menu_sound = pygame.mixer.Sound("son/slice.mp3")
Game_sound = pygame.mixer.Sound("son/slice(1).mp3")
Sword_sound = pygame.mixer.Sound("son/Sword-swipe-7.wav")
Throw_sound = pygame.mixer.Sound("son/Throw-fruit.wav")
Pause_sound = pygame.mixer.Sound("son/Pause.wav")
Unpause_sound = pygame.mixer.Sound("son/Unpause.wav")
Button_sound = pygame.mixer.Sound("son/Next-screen-button.wav")
Slice_sound = pygame.mixer.Sound("son/Pome-slice-1.wav")
Over_sound = pygame.mixer.Sound("son/Game-over.wav")
Start_sound = pygame.mixer.Sound("son/Game-start.wav")
Watermelon_sound = pygame.mixer.Sound("son/Impact-Watermelon.wav")
Apple_sound = pygame.mixer.Sound("son/Impact-Apple.wav")
Banana_sound = pygame.mixer.Sound("son/Impact-Banana.wav")
Coconut_sound = pygame.mixer.Sound("son/Impact-Coconut.wav")
OrangeLemon_sound = pygame.mixer.Sound("son/Impact-Orange.wav")
StrawberryPear_sound = pygame.mixer.Sound("son/Impact-Strawberry.wav")
Dragon_sound = pygame.mixer.Sound("son/dragonfruit.wav")
Bomb_sound = pygame.mixer.Sound("son/Bomb-Fuse.wav")
Boom_sound = pygame.mixer.Sound("son/Bomb-explode.wav")
Boost_sound = pygame.mixer.Sound("son/Bonus-Banana-X2.wav")
Freeze_sound = pygame.mixer.Sound("son/Bonus-Banana-Freeze.wav")
Frenzy_sound = pygame.mixer.Sound("son/Bonus-Banana-Frenzy.wav")
Pome_sound = pygame.mixer.Sound("son/pome-burst.wav")

# Definition of constants
WIDTH, HEIGHT = 1280, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60
GRAVITY = 0.4
no_music = False

menu_fond = pygame.image.load("images/fruitality.png")
fond = pygame.image.load("images/fond.png")
play = pygame.image.load("images/bouton_play.png")
diff = pygame.image.load("images/bouton_diff.png")
easy = pygame.image.load("images/bouton_easy.png")
mid = pygame.image.load("images/bouton_mid.png")
hard = pygame.image.load("images/bouton_hard.png")
restart = pygame.image.load("images/bouton_restart.png")
frenzy_1 = pygame.image.load("images/frenzy_1.png").convert_alpha()
frenzy_2 = pygame.image.load("images/frenzy_2.png")
strike_0 = pygame.image.load("images/0strike.png")
strike_1 = pygame.image.load("images/1strike.png")
strike_2 = pygame.image.load("images/2strike.png")
strike_3 = pygame.image.load("images/3strike.png")
mute = pygame.image.load("images/no_sound.png")
unmute = pygame.image.load("images/sound.png")


# Restart game
def everything(no_music):
    # Open json file
    with open('score.json', 'r') as f:
        data = json.load(f)
    
    # Set the value from zero
    best_score = data["best_score"]
    difficulty = 'mid'
    fruits = []
    current_score = 0
    lifes = 3
    combo_count = 0
    combo_duration = 0
    slow = 1
    slow_duration = 0
    frenzy = False
    frenzy_duration = 100
    frenzy_bonus = 0
    boost = False
    boost_duration = 300
    value = 1
    fade = True

    # Spawn fruit
    def spawn_fruits():
        
        fruits_list = [
            ("pasteque.gif", 10),  # 10% of chance
            ("banane.gif", 10),    # 10% of chance
            ("coco.gif", 10),      # 10% of chance
            ("citron.gif", 8),     # 8% of chance
            ("pomme.gif", 10),     # 10% of chance
            ("fraise.gif", 8),     # 8% of chance
            ("poire.gif", 8),      # 8% of chance
            ("orange.gif", 10),    # 10% of chance
            ("dragon.gif", 0.1),   # 0.1% of chance
            ("bleue.gif", 0.5),    # 0.5% of chance
            ("rouge.gif", 0.5),    # 0.5% of chance
            ("glace.gif", 0.3),    # 0.3% of chance
            ("bombe.gif", 3),      # 3% of chance
            ("grenade.gif", 1)     # 1% of chance
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
                    Throw_sound.play()
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

            if fruit_name == "bombe.gif":
                Bomb_sound.play()

    # happen when a fruit is cut
    def cutting_fruit(fruit, slow_duration, current_score, frenzy, boost):
        # Take the name of the fruit cut
        fruit_extension = fruit['image_name'].split('.')[0]   

        # Manage which fruit make what
        if fruit_extension in ['pasteque', 'banane', 'coco', 'citron', 'pomme', 'fraise', 'poire', 'orange']:
            if boost:
                current_score += 2
            else:
                current_score += 1
            if fruit_extension == 'pasteque':
                Watermelon_sound.play()
            if fruit_extension == 'banane':
                Banana_sound.play()
            if fruit_extension == 'coco':
                Coconut_sound.play()
            if fruit_extension == 'citron':
                OrangeLemon_sound.play()
            if fruit_extension == 'pomme':
                Apple_sound.play()
            if fruit_extension == 'fraise':
                StrawberryPear_sound.play()
            if fruit_extension == 'poire':
                StrawberryPear_sound.play()
            if fruit_extension == 'orange':
                OrangeLemon_sound.play()
        if fruit_extension == 'dragon' :
            Dragon_sound.play()
            if boost:
                current_score += 100
            else:
                current_score += 50
        if fruit_extension == 'glace':
            Freeze_sound.play()
            if boost:
                current_score += 2
            else:
                current_score += 1
            fruit['cut'] = True
            slow_duration = 60
            return [], slow_duration, current_score, frenzy, boost
        if fruit_extension == 'bleue':
            Boost_sound.play()
            if boost:
                current_score += 2
            else:
                current_score += 1
            fruit['cut'] = True
            boost = True
            return [], slow_duration, current_score, frenzy, boost
        if fruit_extension == 'rouge':
            Frenzy_sound.play()
            if boost:
                current_score += 2
            else:
                current_score += 1
            fruit['cut'] = True
            frenzy = True
            return [], slow_duration, current_score, frenzy, boost
        if fruit_extension == 'grenade':
            if 'hit_count' not in fruit:
                fruit['hit_count'] = 0
            fruit['hit_count'] += 1
            Slice_sound.play()
            if boost:
                current_score += 20
            else:
                current_score += 10
            if fruit['hit_count'] >= 5:
                Pome_sound.play()
                leftleft_piece = fruit.copy()
                leftright_piece = fruit.copy()
                rightleft_piece = fruit.copy()
                rightright_piece = fruit.copy()

                leftleft_piece['image'] = pygame.image.load(f"images/coupe/{fruit_extension}_gauchegauche.gif")
                leftright_piece['image'] = pygame.image.load(f"images/coupe/{fruit_extension}_gauchedroite.gif")
                rightleft_piece['image'] = pygame.image.load(f"images/coupe/{fruit_extension}_droitegauche.gif")
                rightright_piece['image'] = pygame.image.load(f"images/coupe/{fruit_extension}_droitedroite.gif")

                leftleft_piece['speed_x'] = fruit['speed_x'] * random.uniform(-10, -5)
                leftright_piece['speed_x'] = fruit['speed_x'] * random.uniform(-8, -5)
                rightleft_piece['speed_x'] = fruit['speed_x'] * random.uniform(8, 10)
                rightright_piece['speed_x'] = fruit['speed_x'] * random.uniform(5, 10)
                leftleft_piece['speed_y'] = fruit['speed_y'] * 0.3
                leftright_piece['speed_y'] = fruit['speed_y'] * 0.1
                rightleft_piece['speed_y'] = fruit['speed_y'] * 0.1
                rightright_piece['speed_y'] = fruit['speed_y'] * 0.3

                fruit['cut'] = True

                leftleft_piece['is_piece'] = True
                leftright_piece['is_piece'] = True
                rightleft_piece['is_piece'] = True
                rightright_piece['is_piece'] = True

                return [leftleft_piece, leftright_piece, rightleft_piece, rightright_piece], slow_duration, current_score, frenzy, boost
            else:
                fruit['required_key'] = random.choice(list(KEYS.keys()))
                return [], slow_duration, current_score, frenzy, boost
        if fruit_extension == 'bombe':
            Bomb_sound.fadeout(0)
            time.sleep(0.1)
            Boom_sound.play()
            fruit['cut'] = True
            if not no_music:
                Game_sound.fadeout(1000)
            game_over()
            return [], slow_duration, current_score, frenzy, boost
        
        # replace the fruit with his two pieces
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

        return [left_piece, right_piece], slow_duration, current_score, frenzy, boost


    # Main menu
    def menu(difficulty, begin, no_music):
        play_rect = play.get_rect(topleft=(488, 330))
        diff_rect = diff.get_rect(topleft=(488, 550))
        unmute_rect = unmute.get_rect(topleft=(50, 600))
        mute_rect = mute.get_rect(topleft=(50, 600))
        screen.blit(menu_fond, (0, 0))
        screen.blit(play, play_rect.topleft)
        screen.blit(diff, diff_rect.topleft)
        if difficulty == 'easy':
            screen.blit(pygame.transform.scale(easy, (easy.get_width() / 1.5, easy.get_height() / 1.5)), (888, 580))
        if difficulty == 'mid':
            screen.blit(pygame.transform.scale(mid, (mid.get_width() / 1.5, mid.get_height() / 1.5)), (888, 580))
        if difficulty == 'hard':
            screen.blit(pygame.transform.scale(hard, (hard.get_width() / 1.5, hard.get_height() / 1.5)), (888, 580))
        pygame.display.update()

        choosing = True
        while choosing:
            if no_music:
                screen.blit(mute, mute_rect.topleft)
                Menu_sound.fadeout(1000)
            elif not no_music:
                screen.blit(unmute, unmute_rect.topleft)
                if not pygame.mixer.get_busy():
                    Menu_sound.play(loops=-1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if play_rect.collidepoint(event.pos):
                            if not no_music:
                                Menu_sound.fadeout(1000)
                            Button_sound.play()
                            begin = False
                            choosing = False
                            time.sleep(0.5)
                            if not no_music:
                                Game_sound.play(loops=-1, fade_ms=2000)

                        elif diff_rect.collidepoint(event.pos):
                            Button_sound.play()
                            Pause_sound.play()
                            choosing = False
                            difficulty = choose_difficulty(difficulty)

                        elif unmute_rect.collidepoint(event.pos) and not no_music:
                            no_music = True
                            choosing = False
                        elif mute_rect.collidepoint(event.pos) and no_music:
                            no_music = False
                            choosing = False
            pygame.display.update()
        return difficulty, begin, no_music
    
    # Allows you to choose the difficulty
    def choose_difficulty(difficulty):
        y = -HEIGHT
        while y <= 50:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            screen.blit(fond, (0, y - 50))
            easy_rect = easy.get_rect(topleft=(488, y + 60))
            mid_rect = mid.get_rect(topleft=(488, y + 280))
            hard_rect = hard.get_rect(topleft=(488, y + 500))
            screen.blit(easy, easy_rect.topleft)
            screen.blit(mid, mid_rect.topleft)
            screen.blit(hard, hard_rect.topleft)
            pygame.display.update()
            y += 50

        choosing = True
        while choosing:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if easy_rect.collidepoint(event.pos):
                            Button_sound.play()
                            Unpause_sound.play()
                            difficulty = 'easy'
                            choosing = False
                        if mid_rect.collidepoint(event.pos):
                            Button_sound.play()
                            Unpause_sound.play()
                            difficulty = 'mid'
                            choosing = False
                        if hard_rect.collidepoint(event.pos):
                            Button_sound.play()
                            Unpause_sound.play()
                            difficulty = 'hard'
                            choosing = False

        y = 50
        while y >= -HEIGHT:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            screen.blit(menu_fond, (0, 0))
            screen.blit(play, (488, 330))
            screen.blit(diff, (488, 550))
            if difficulty == 'easy':
                screen.blit(pygame.transform.scale(easy, (easy.get_width() / 1.5, easy.get_height() / 1.5)), (888, 580))
            if difficulty == 'mid':
                screen.blit(pygame.transform.scale(mid, (mid.get_width() / 1.5, mid.get_height() / 1.5)), (888, 580))
            if difficulty == 'hard':
                screen.blit(pygame.transform.scale(hard, (hard.get_width() / 1.5, hard.get_height() / 1.5)), (888, 580))
            screen.blit(fond, (0, y - 50))
            screen.blit(easy, (488, y + 60))
            screen.blit(mid, (488, y + 280))
            screen.blit(hard, (488, y + 500))
            pygame.display.update()
            y -= 50
        return difficulty
    
    # Make loose the game
    def game_over():
        if Bomb_sound.get_num_channels() > 0:
            Bomb_sound.stop() 
        y = -HEIGHT
        while y <= 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            restart_rect = restart.get_rect(topleft=(488, y + 500))
            screen.blit(pygame.image.load("images/fail.png"), (0, y))
            screen.blit(restart, restart_rect.topleft)

            pygame.display.update()

            y += 187.5 # Animate the loosing screen with a sliding effect

        choosing = True
        while choosing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if restart_rect.collidepoint(event.pos):
                            Button_sound.play()
                            choosing = False
                            everything(no_music)

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
        difficulty, begin, no_music = menu(difficulty, begin, no_music)


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
        #slow_duration -= 0.5
        slow_duration -= 60
        if slow_duration >= 0:
            #slow = 0.5
            slow = 1/240
            screen.blit(pygame.image.load("images/glace.png"), (0, 0))
        else:
            slow = 1

        # Display of numerical values
        font = pygame.font.Font(None, 36)
        if boost:
            text_score = font.render(f"Score x2:  {current_score}", True, (89, 154, 255))
        else:
            text_score = font.render(f"Score:  {current_score}", True, (255, 255, 255))
        text_best_score = font.render(f"Best Score:  {best_score}", True, (255, 255, 255))
        screen.blit(text_score, (20, 20))
        screen.blit(text_best_score, (20, 60))
        if lifes == 3:
            screen.blit(strike_0, (0, 0))
        if lifes == 2:
            screen.blit(strike_1, (0, 0))
        if lifes == 1:
            screen.blit(strike_2, (0, 0))
        if lifes <= 0:
            screen.blit(strike_3, (0, 0))

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
                
        if not boost:
            boost_duration = 300
        if boost:
            boost_duration -= 0.5
            if boost_duration <= 0:
                boost = False

        # Event management
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                Sword_sound.play()
                fruit_coupe = False  # Variable to know if a valid fruit has been cut
                
                for fruit in fruits:
                    # Check that the fruit matches the key and has not already been cut
                    if event.key == fruit['required_key'] and not fruit['cut'] and not fruit.get('is_piece', False):
                        morceaux, slow_duration, current_score, frenzy, boost = cutting_fruit(fruit, slow_duration, current_score, frenzy, boost)
                        fruit_coupe = True  # A valid fruit has been cut
                        
                        if fruit['cut']:
                            combo_duration = 40
                            combo_count += 1
                        if morceaux:
                            fruits_to_add.extend(morceaux)

                # If no valid fruit has been cut, remove a life
                if not frenzy and frenzy_bonus <= 0:
                    if not fruit_coupe:
                        lifes -= 1


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
                fruit_uncut = fruit['image_name'].split('.')[0] 
                if fruit['x'] < 0:
                    # If it's a piece of grenade (and not a whole grenade), no bounce
                    if fruit.get('is_piece', False) and fruit_uncut == 'grenade':
                        fruit['speed_x'] = fruit['speed_x']
                    else:
                        fruit['x'] = 0
                        fruit['speed_x'] = -fruit['speed_x']  # Otherwise, classic bounce

                elif fruit['x'] > WIDTH - fruit['image'].get_width():
                    # If it's a piece of grenade (and not a whole grenade), no bounce
                    if fruit.get('is_piece', False) and fruit_uncut == 'grenade':
                        fruit['speed_x'] = fruit['speed_x']
                    else:
                        fruit['x'] = WIDTH - fruit['image'].get_width()
                        fruit['speed_x'] = -fruit['speed_x']  # Otherwise, classic bounce

                
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
                    if fruit['y'] > HEIGHT and not fruit['cut'] and not fruit.get('is_piece', False) and fruit_uncut in ['pasteque', 'banane', 'coco', 'citron', 'pomme', 'fraise', 'poire', 'orange', 'dragon']:
                        lifes -= 1
                    if fruit['y'] > HEIGHT and fruit_uncut == 'bombe':
                        Bomb_sound.fadeout(0)
                else:
                    continue

        # Screen effect due to frenzy
        if frenzy:
            screen.blit(frenzy_2, (0, 0))
            if fade:
                value += 0.5
                frenzy_1.set_alpha(int((value / 4.5) * 255))
                screen.blit(frenzy_1, (0, 0))
                if value >= 4.5:
                    fade = False
            elif not fade:
                value -= 0.5
                frenzy_1.set_alpha(int((value / 4.5) * 255))
                screen.blit(frenzy_1, (0, 0))
                if value <= 0:
                    fade = True
        
        # Loses when lives are lost
        if lifes <= 0:
            if not no_music:
                Game_sound.fadeout(1000)
            Over_sound.play()
            Over_sound.fadeout(2000)
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
everything(no_music)