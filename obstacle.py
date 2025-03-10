import pygame
import random
from settings import WIDTH, HEIGHT, ASSETS_PATH

class Obstacle:
    def __init__(self):
       
        self.sprites = {
            "arvore1": pygame.image.load(ASSETS_PATH + "arvore1.png"),
            "arvore2": pygame.image.load(ASSETS_PATH + "arvore2.png"),
            "toco": pygame.image.load(ASSETS_PATH + "toco.png")
        }
        
       
        self.sprites["arvore1"] = pygame.transform.scale(self.sprites["arvore1"], (70, 100))  # Aumentando árvores
        self.sprites["arvore2"] = pygame.transform.scale(self.sprites["arvore2"], (75, 110))
        self.sprites["toco"] = pygame.transform.scale(self.sprites["toco"], (40, 40))
        
   
        self.obstacles = []
        self.generate_obstacles()

    def generate_obstacles(self):
        positions = []  
        
        for _ in range(10):
            obj_type = random.choice(["arvore1", "arvore2"]) 
            x = random.randint(0, WIDTH - 40)
            y = random.randint(-600, 0)
            rect = pygame.Rect(x, y, 40, 40)
            
            
            positions.append((x, y))
            self.obstacles.append({"type": obj_type, "rect": rect})
        
        # Adicionar tocos sem sobreposição
        for _ in range(5):
            while True:
                x = random.randint(0, WIDTH - 40)
                y = random.randint(-600, 0)
                rect = pygame.Rect(x, y, 40, 40)
                
                if not any(abs(x - px) < 50 and abs(y - py) < 50 for px, py in positions):
                    self.obstacles.append({"type": "toco", "rect": rect})
                    positions.append((x, y))
                    break

    def update(self):
        for obj in self.obstacles:
            obj["rect"].y += 5
            if obj["rect"].y > HEIGHT:
                obj["rect"].y = random.randint(-600, 0)
                obj["rect"].x = random.randint(0, WIDTH - 40)

    def draw(self, screen):
        for obj in self.obstacles:
            screen.blit(self.sprites[obj["type"]], obj["rect"].topleft)
