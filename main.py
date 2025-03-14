import pygame
from settings import WIDTH, HEIGHT, BLACK, FPS
from skier import Skier
from obstacle import Obstacle
from yeti import YetiManager

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SkiFree Clone")

# Carregar o tile de neve contínuo
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

# Controle da rolagem do chão
base_speed = 5
current_speed = base_speed
ground_y = 0

tile_width, tile_height = ground.get_size()

distance = 0  
running = True
clock = pygame.time.Clock()

while running:

    ground_y += current_speed
    if ground_y >= tile_height:
        ground_y = 0


    for y in range(-tile_height, HEIGHT, tile_height):
        for x in range(0, WIDTH, tile_width):
            screen.blit(ground, (x, y + ground_y))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()
    skier.move(keys)


    if keys[pygame.K_UP] and skier.rect.y > HEIGHT // 4:
        skier.rect.y -= skier.speed
        current_speed = base_speed * 1.5
    elif keys[pygame.K_DOWN] and skier.rect.y < HEIGHT - 100:
        skier.rect.y += skier.speed
        current_speed = base_speed * 0.5
    else:
        current_speed = base_speed

    
    for obj in obstacles.obstacles:
        obj["rect"].y += current_speed

    obstacles.update()
    obstacles.draw(screen)


    reduced_skier_rect = skier.rect.inflate(-10, -10)
    for obj in obstacles.obstacles:
        reduced_obj_rect = obj["rect"].inflate(-10, -10)
        if reduced_skier_rect.colliderect(reduced_obj_rect):
            print("Você bateu em um obstáculo!")
            running = False


    collision_with_yeti = manager.update_and_draw(
        screen=screen,
        skier=skier,
        obstacles=obstacles,
        distance=distance
    )
    if collision_with_yeti:

        running = False


    skier.draw(screen)


    distance += current_speed * 2


    score_text = font.render(f"Distância: {distance:.2f} m", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
