import pygame
import random
from settings import WIDTH, HEIGHT, ASSETS_PATH

class Yeti:
    def __init__(self):
        # Carregar os sprites do yeti para diferentes direções
        self.sprites = {
            "reto": pygame.image.load(ASSETS_PATH + "yeti_costa_reto.png"),
            "esquerda": pygame.image.load(ASSETS_PATH + "yeti_costa_esquerda.png"),
            "direita": pygame.image.load(ASSETS_PATH + "yeti_costa_direita.png")
        }


        self.image = self.sprites["reto"]
        self.image = pygame.transform.scale(self.image, (80, 80))  # Ajustar tamanho do yeti

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, WIDTH - 50)
        self.rect.y = -100 

        self.speed = 3  

    def chase(self, skier, obstacles):
        """ Movimenta o yeti em direção ao jogador, desviando dos obstáculos. """
        
        # Movimentação na direção do esquiador
        if self.rect.y < skier.rect.y - 50:
            self.rect.y += self.speed  # Aproxima-se do jogador
        
        # Ajustar horizontalmente para seguir o esquiador
        if self.rect.x < skier.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > skier.rect.x:
            self.rect.x -= self.speed

        # Atualizar animação baseada na direção
        self.update_animation(skier)

        # Tentar evitar obstáculos
        for obj in obstacles.obstacles:
            if self.rect.colliderect(obj["rect"]):
                self.avoid_obstacle()

    def avoid_obstacle(self):
        """ Move o Yeti para evitar colisões com obstáculos. """
        self.rect.x += random.choice([-20, 20])  # Move aleatoriamente para esquerda ou direita

    def update_animation(self, skier):
        """ Atualiza o sprite do yeti dependendo da direção do movimento. """
        if self.rect.x < skier.rect.x:
            self.image = self.sprites["direita"]
        elif self.rect.x > skier.rect.x:
            self.image = self.sprites["esquerda"]
        else:
            self.image = self.sprites["reto"]

        # Redimensiona para evitar mudanças de tamanho erradas
        self.image = pygame.transform.scale(self.image, (80, 80))

    def draw(self, screen):
        """ Desenha o Yeti na tela. """
        screen.blit(self.image, self.rect)
