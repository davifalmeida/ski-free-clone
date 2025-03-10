import pygame
import random
from settings import WIDTH, HEIGHT, RED

class Yeti:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - 50), -100, 50, 50)
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = -100
            self.rect.x = random.randint(0, WIDTH - 50)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)
