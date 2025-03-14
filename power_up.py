import pygame
import random
from settings import WIDTH, HEIGHT, ASSETS_PATH

class Rampa:
    def __init__(self):
        # Carrega e dimensiona a imagem da rampa
        self.image = pygame.image.load(ASSETS_PATH + "rampa.png")
        self.image = pygame.transform.scale(self.image, (60, 60))
        
        # Cria um retângulo para posicionar a rampa
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 60)
        self.rect.y = random.randint(-600, 0)

        # Define o quanto essa rampa "impulsiona" a distância
        self.boost_distance = 150

    def update(self, speed):
        """Move a rampa para baixo na tela de acordo com a velocidade do jogo."""
        self.rect.y += speed

    def draw(self, screen):
        """Desenha a rampa na tela."""
        screen.blit(self.image, self.rect)