import pygame
import random
from pygame.math import Vector2
from settings import WIDTH, HEIGHT, ASSETS_PATH

class Yeti:
    def __init__(self, spawn_x=None, spawn_y=None):
        # Carregar os sprites do yeti para diferentes direções
        self.sprites = {
            "reto": pygame.image.load(ASSETS_PATH + "yeti_costa_reto.png"),
            "esquerda": pygame.image.load(ASSETS_PATH + "yeti_costa_esquerda.png"),
            "direita": pygame.image.load(ASSETS_PATH + "yeti_costa_direita.png")
        }
        # Sprite padrão
        self.image = pygame.transform.scale(self.sprites["reto"], (80, 80))
        self.rect = self.image.get_rect()

        # Se não forem fornecidas coords de spawn, coloca no centro
        if spawn_x is None:
            spawn_x = WIDTH // 2
        if spawn_y is None:
            spawn_y = -100  

        self.rect.x = spawn_x
        self.rect.y = spawn_y

        # Atributos de movimento
        self.base_speed = 2
        self.speed = self.base_speed
        self.max_speed = 12

    def chase(self, skier, obstacles):
        """
        Movimenta o Yeti em direção ao jogador e tenta evitar obstáculos.
        """
        chase_vector = Vector2(
            skier.rect.centerx - self.rect.centerx,
            skier.rect.centery - self.rect.centery
        )

        # Vetor de desvio de obstáculos
        avoid_vector = Vector2(0, 0)
        avoid_distance = 120  # Raio de "alerta"

        for obj in obstacles.obstacles:
            obstacle_vec = Vector2(
                obj["rect"].centerx - self.rect.centerx,
                obj["rect"].centery - self.rect.centery
            )
            dist = obstacle_vec.length()
            if 0 < dist < avoid_distance:
                force = (avoid_distance - dist) / avoid_distance
                obstacle_vec.scale_to_length(1)
                avoid_vector -= obstacle_vec * force

        # Soma perseguição + desvio
        final_vector = chase_vector + avoid_vector

        # Se o vetor final for zero, não movemos
        dist_final = final_vector.length()
        if dist_final == 0:
            return

        # Ajusta velocidade de acordo com a distância ao jogador
        distance_to_skier = chase_vector.length()
        self.speed = min(self.base_speed + 0.005 * distance_to_skier, self.max_speed)

        # Normaliza e aplica a velocidade
        final_vector.scale_to_length(self.speed)
        self.rect.x += final_vector.x
        self.rect.y += final_vector.y

        # Mantém dentro da tela
        self.rect.x = max(10, min(self.rect.x, WIDTH - self.rect.width - 10))
        self.rect.y = max(-200, min(self.rect.y, HEIGHT + 200))

        # Atualiza sprite conforme direção horizontal
        if final_vector.x > 0:
            self.update_animation(1)
        elif final_vector.x < 0:
            self.update_animation(-1)
        else:
            self.update_animation(0)

    def update_animation(self, direction):

        if direction > 0:
            self.image = self.sprites["direita"]
        elif direction < 0:
            self.image = self.sprites["esquerda"]
        else:
            self.image = self.sprites["reto"]

        self.image = pygame.transform.scale(self.image, (80, 80))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class YetiManager:

    def __init__(self):
        self.yetis_list = []
        self.yeti_collision_enabled = False

        # Definições de como escalar a quantidade de Yetis
        self.distance_step = 2000  
        self.last_spawn_distance = 0
        self.respawn_distance = 500  

    def update_and_draw(self, screen, skier, obstacles, distance):

        yetis_needed = 1 + int(distance // self.distance_step)


        while len(self.yetis_list) < yetis_needed:
            if len(self.yetis_list) == 0:
                # Primeiro Yeti surge no mesmo X do jogador
                spawn_x = skier.rect.x
            else:
                # Demais Yetis surgem em X aleatório
                spawn_x = random.randint(0, WIDTH - 80)

            spawn_y = HEIGHT + 300  # Surge abaixo da tela
            new_yeti = Yeti(spawn_x, spawn_y)
            self.yetis_list.append(new_yeti)

        # Habilitar colisão
        self.yeti_collision_enabled = True

        # Atualizar cada Yeti
        for y in self.yetis_list[:]:  # copiar a lista para remover com segurança
            y.chase(skier, obstacles)  
            y.draw(screen)

            # Se quiser remover o Yeti quando colide com obstáculo
            if self.yeti_collision_enabled:
                for obj in obstacles.obstacles:
                    if y.rect.colliderect(obj["rect"]):
                        self.yetis_list.remove(y)
                        break

        # Checar colisão com o jogador
        if self.yeti_collision_enabled:
            reduced_skier_rect = skier.rect.inflate(-10, -10)
            for y in self.yetis_list:
                reduced_yeti_rect = y.rect.inflate(-10, -10)
                if reduced_skier_rect.colliderect(reduced_yeti_rect):
                    return True  # Houve colisão

        return False