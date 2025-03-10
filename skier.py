import pygame
from settings import WIDTH, HEIGHT, BLUE

class Skier:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT - 100, 40, 40)
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)
