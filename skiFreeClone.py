import pygame
import random

# Inicializar o pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SkiFree Clone")

# Cores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Fonte para o placar
font = pygame.font.SysFont(None, 36)

# Configuração do esquiador
skier = pygame.Rect(WIDTH // 2, HEIGHT - 100, 40, 40)
skier_speed = 5

# Obstáculos
obstacles = []
for _ in range(10):
    x = random.randint(0, WIDTH - 40)
    y = random.randint(-600, 0)
    obstacles.append(pygame.Rect(x, y, 40, 40))

# Monstro das neves
yeti = pygame.Rect(random.randint(0, WIDTH - 40), -100, 50, 50)
yeti_speed = 3

# Loop principal
running = True
clock = pygame.time.Clock()
distance = 0

while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and skier.x > 0:
        skier.x -= skier_speed
    if keys[pygame.K_RIGHT] and skier.x < WIDTH - skier.width:
        skier.x += skier_speed
    
    # Movimento dos obstáculos
    for obstacle in obstacles:
        obstacle.y += 5
        if obstacle.y > HEIGHT:
            obstacle.y = random.randint(-600, 0)
            obstacle.x = random.randint(0, WIDTH - 40)
        pygame.draw.rect(screen, GREEN, obstacle)
    
    # Monstro das neves começa a aparecer após 500 de distância
    if distance > 500:
        yeti.y += yeti_speed
        if yeti.y > HEIGHT:
            yeti.y = -100
            yeti.x = random.randint(0, WIDTH - 50)
        pygame.draw.rect(screen, RED, yeti)
    
    # Desenhando o esquiador
    pygame.draw.rect(screen, BLUE, skier)
    
    # Atualizar distância
    distance += 1
    
    # Exibir o placar
    score_text = font.render(f"Distância: {distance}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    # Verificando colisões
    for obstacle in obstacles:
        if skier.colliderect(obstacle):
            print("Você bateu em um obstáculo!")
            running = False
    
    if skier.colliderect(yeti):
        print("O monstro pegou você!")
        running = False
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()