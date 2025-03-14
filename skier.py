import pygame
from settings import WIDTH, HEIGHT, ASSETS_PATH

class Skier:
    def __init__(self):
        self.sprites = {
            "reto": pygame.image.load(ASSETS_PATH + "skiador_reto.png"),
            "esquerda": pygame.image.load(ASSETS_PATH + "skiador_esquerda.png"),
            "direita": pygame.image.load(ASSETS_PATH + "skiador_direita.png"),
            "colisao": pygame.image.load(ASSETS_PATH + "skiador_colisão.png"),
            "pulo": pygame.image.load(ASSETS_PATH + "skiador_pulo.png"),  # NOVO
        }
        for key in self.sprites:
            self.sprites[key] = pygame.transform.scale(self.sprites[key], (40, 40))

        self.image = self.sprites["reto"]
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 100))
        self.speed = 5

        # Controle de pulo
        self.is_jumping = False
        self.jump_timer = 0.0

    def move(self, keys):
        if not self.is_jumping:
            if keys[pygame.K_LEFT] and self.rect.x > 0:
                self.rect.x -= self.speed
                self.image = self.sprites["esquerda"]
            elif keys[pygame.K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
                self.rect.x += self.speed
                self.image = self.sprites["direita"]
            else:
                self.image = self.sprites["reto"]

    def start_jump(self, duration=1.0):
        self.is_jumping = True
        self.jump_timer = duration
        self.image = self.sprites["pulo"]  # Muda para sprite de pulo

    def update(self, dt):
        """
        dt = tempo decorrido em segundos (ex.: clock.get_time() / 1000).
        """
        if self.is_jumping:
            self.jump_timer -= dt
            if self.jump_timer <= 0:
                self.is_jumping = False
                self.image = self.sprites["reto"]  # Volta ao normal

    def collide(self):
        self.image = self.sprites["colisao"]

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
