import pygame
import time
from settings import WIDTH, HEIGHT, BLACK, FPS
from skier import Skier
from obstacle import Obstacle
from yeti import Yeti

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SkiFree Clone")

ground = pygame.image.load("assets/chão.png")  # Tile de neve contínuo

# Ajustar o tamanho do tile do chão
ground_size = 100  
ground = pygame.transform.scale(ground, (ground_size, ground_size))

# Fonte do placar
font = pygame.font.SysFont(None, 36)

# Criar objetos do jogo
skier = Skier()
skier.rect.y = HEIGHT // 2 
obstacles = Obstacle()
yeti = None
yeti_spawn_time = None
yeti_collision_enabled = False

# Controle da rolagem do chão
base_speed = 5  
current_speed = base_speed  
ground_y = 0  

tile_width, tile_height = ground.get_size()

distance = 0
next_yeti_spawn = 500  
yeti_respawn_distance = 300  

running = True
clock = pygame.time.Clock()

while running:
    # Movimento do chão (tiles rolando)
    ground_y += current_speed
    if ground_y >= tile_height:
        ground_y = 0  

    # Preencher a tela com múltiplos tiles
    for y in range(-tile_height, HEIGHT, tile_height):
        for x in range(0, WIDTH, tile_width):
            screen.blit(ground, (x, y + ground_y))

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    keys = pygame.key.get_pressed()
    skier.move(keys)

    # Ajustar velocidade com base no movimento vertical
    if keys[pygame.K_UP] and skier.rect.y > HEIGHT // 4:
        skier.rect.y -= skier.speed
        current_speed = base_speed * 1.5  
    elif keys[pygame.K_DOWN] and skier.rect.y < HEIGHT - 100:
        skier.rect.y += skier.speed
        current_speed = base_speed * 0.5  
    else:
        current_speed = base_speed  

    # Atualizar obstáculos conforme a rolagem
    for obj in obstacles.obstacles:
        obj["rect"].y += current_speed

    
    obstacles.update()
    obstacles.draw(screen)

    # Gerenciar o aparecimento do Yeti
    if distance >= next_yeti_spawn:
        if yeti is None:
            yeti = Yeti()
            yeti.rect.x = skier.rect.x  
            yeti.rect.y = skier.rect.y - -120
            yeti.image = pygame.transform.scale(yeti.image, (80, 80))  
            yeti.speed = base_speed *0.8
            yeti_spawn_time = time.time()
            yeti_collision_enabled= False

    if yeti_spawn_time and time.time() - yeti_spawn_time > 5:
        yeti_collision_enabled = True

    # Atualizar monstro
    if yeti:
        yeti.speed += 0.002 * (distance - next_yeti_spawn)
        yeti.speed = min(yeti.speed, base_speed * 1.5)
        yeti.chase(skier, obstacles)  # O Yeti tentará evitar obstáculos
        yeti.update_animation(skier)
        yeti.draw(screen)
        
        # Se o yeti colidir com um obstáculo, ele desaparece e reaparece mais à frente
        if yeti_collision_enabled:
            for obj in obstacles.obstacles:
                if yeti.rect.colliderect(obj["rect"]):
                    yeti = None  # Some temporariamente
                    next_yeti_spawn = distance + yeti_respawn_distance  # Define quando reaparecerá
                    break

    # Verificar colisões ajustando a área de detecção (somente após delay para o Yeti)
    for obj in obstacles.obstacles:
        reduced_skier_rect = skier.rect.inflate(-10, -10)  # Reduzindo a área de colisão
        reduced_obj_rect = obj["rect"].inflate(-10, -10)  # Reduzindo a área de colisão dos obstáculos
        
        if reduced_skier_rect.colliderect(reduced_obj_rect):
            print("Você bateu em um obstáculo!")
            running = False

    if yeti_collision_enabled and yeti:
        reduced_yeti_rect = yeti.rect.inflate(-10, -10)  # Reduzindo a colisão do yeti
        if reduced_skier_rect.colliderect(reduced_yeti_rect):
            print("O monstro pegou você!")
            running = False

  
    skier.draw(screen)

  
    distance += int(current_speed)  

    # Exibir o placar
    score_text = font.render(f"Distância: {distance}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()