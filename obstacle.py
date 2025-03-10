import pygame
import random
from settings import WIDTH, HEIGHT, GREEN

class Obstacle:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - 40), random.randint(-600, 0), 40, 40)

    def update(self):
        self.rect.y += 5
        if self.rect.y > HEIGHT:
            self.rect.y = random.randint(-600, 0)
            self.rect.x = random.randint(0, WIDTH - 40)

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)
