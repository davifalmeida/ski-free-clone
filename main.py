import pygame
import random
from settings import WIDTH, HEIGHT, BLACK, FPS
from skier import Skier
from obstacle import Obstacle
from yeti import YetiManager
from power_up import Rampa  # Importa a classe Rampa (uma única rampa)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SkiFree Clone")

# Carrega o tile de neve contínuo
ground = pygame.image.load("assets/chao.jpeg")
ground_size = 100
ground = pygame.transform.scale(ground, (ground_size, ground_size))

# Fonte do placar
font = pygame.font.SysFont(None, 36)

# Criar objetos do jogo
skier = Skier()
skier.rect.y = HEIGHT // 2
obstacles = Obstacle()
manager = YetiManager()

# Lista de rampas
rampas = []
# A cada 1500 metros, criaremos uma nova rampa
proxima_rampa = 1500  

# Controle da rolagem do chão
base_speed = 5
current_speed = base_speed
ground_y = 0
tile_width, tile_height = ground.get_size()

distance = 0.0
running = True
clock = pygame.time.Clock()

while running:
    dt = clock.get_time() / 1000.0  # tempo decorrido em segundos

    # ========== Desenhar chão rolando ==========
    ground_y += current_speed
    if ground_y >= tile_height:
        ground_y = 0

    for y in range(-tile_height, HEIGHT, tile_height):
        for x in range(0, WIDTH, tile_width):
            screen.blit(ground, (x, y + ground_y))

    # ========== Eventos ==========
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ========== Movimento do jogador ==========
    keys = pygame.key.get_pressed()
    skier.move(keys)
    skier.update(dt)  # Se tiver lógica de pulo, atualiza o timer

    # Ajuste de velocidade conforme o movimento vertical
    if keys[pygame.K_UP] and skier.rect.y > HEIGHT // 4:
        skier.rect.y -= skier.speed
        current_speed = base_speed * 1.5
    elif keys[pygame.K_DOWN] and skier.rect.y < HEIGHT - 100:
        skier.rect.y += skier.speed
        current_speed = base_speed * 0.5
    else:
        current_speed = base_speed

    # ========== Obstáculos ==========
    for obj in obstacles.obstacles:
        obj["rect"].y += current_speed
    obstacles.update()
    obstacles.draw(screen)

    # ========== Gerar rampas a cada 1500m ==========
    if distance >= proxima_rampa:
        rampas.append(Rampa())   # Cria uma nova instância de Rampa
        proxima_rampa += 1500    # Próxima rampa só depois de +1500m

    # ========== Atualizar e desenhar rampas ==========
    for rampa in rampas[:]:  # copiar a lista para remover com segurança
        rampa.update(current_speed)
        rampa.draw(screen)

        # Se a rampa saiu da tela, removemos
        if rampa.rect.y > HEIGHT + 100:
            rampas.remove(rampa)
            continue

        # Verificar colisão com o jogador
        reduced_skier_rect = skier.rect.inflate(-10, -10)
        if reduced_skier_rect.colliderect(rampa.rect):
            # Aumentar a distância
            distance += rampa.boost_distance
            print(f"Você usou a rampa! +{rampa.boost_distance}m")
            # Se quiser remover a rampa após o uso
            rampas.remove(rampa)

    # ========== Colisão com obstáculos (se não estiver pulando, etc.) ==========
    reduced_skier_rect = skier.rect.inflate(-10, -10)
    for obj in obstacles.obstacles:
        reduced_obj_rect = obj["rect"].inflate(-10, -10)
        if reduced_skier_rect.colliderect(reduced_obj_rect):
            print("Você bateu em um obstáculo!")
            running = False

    # ========== Yeti ==========
    collision_with_yeti = manager.update_and_draw(
        screen=screen,
        skier=skier,
        obstacles=obstacles,
        distance=distance
    )
    if collision_with_yeti:
        running = False

    # ========== Desenhar o jogador ==========
    skier.draw(screen)

    # ========== Atualizar distância ==========
    distance += current_speed * 0.5  # Ajuste o fator conforme desejado

    # ========== Exibir placar ==========
    score_text = font.render(f"Distância: {distance:.2f} m", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
