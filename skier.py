import pygame
from settings import WIDTH, HEIGHT, ASSETS_PATH

class Skier:
    def __init__(self):
        self.image = pygame.image.load(ASSETS_PATH + "skiador_reto.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 100))
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
