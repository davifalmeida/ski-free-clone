import pygame
from settings import WIDTH, HEIGHT, ASSETS_PATH

class Skier:
    def __init__(self):

        self.sprites = {
            "reto": pygame.image.load(ASSETS_PATH + "skiador_reto.png"),
            "esquerda": pygame.image.load(ASSETS_PATH + "skiador_esquerda.png"),
            "direita": pygame.image.load(ASSETS_PATH + "skiador_direita.png"),
            "colisao": pygame.image.load(ASSETS_PATH + "skiador_colisão.png")
        }

        for key in self.sprites:
            self.sprites[key] = pygame.transform.scale(self.sprites[key], (40, 40))

        self.image = self.sprites["reto"]  # Começa reto
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 100))
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
            self.image = self.sprites["esquerda"]
        elif keys[pygame.K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += self.speed
            self.image = self.sprites["direita"]
        else:
            self.image = self.sprites["reto"] 

    def collide(self):
        """Muda o sprite para a colisão."""
        self.image = self.sprites["colisao"]

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
