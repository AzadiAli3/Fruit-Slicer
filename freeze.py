import pygame
import time

def slow_motion(duration, facteur):
    start_time = time.time()
    while time.time() - start_time < duration:
        pygame.time.delay(int(16 * 0.5))  #16ms ≈ 60 FPS