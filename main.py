import pygame
from settings import WIDTH, HEIGHT, WHITE, BLACK, FPS
from skier import Skier
from obstacle import Obstacle
from yeti import Yeti


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SkiFree Clone")


ground = pygame.image.load("assets/chão.png")


ground_size = 100  
ground = pygame.transform.scale(ground, (ground_size, ground_size))


font = pygame.font.SysFont(None, 36)


skier = Skier()
obstacles = Obstacle()
yeti = Yeti()

# Controle da rolagem do chão
ground_y = 0  
ground_speed = 5  

tile_width, tile_height = ground.get_size()

running = True
clock = pygame.time.Clock()
distance = 0

while running:
    # Movimento do chão (tiles rolando)
    ground_y += ground_speed
    if ground_y >= tile_height:
        ground_y = 0  

   
    for y in range(-tile_height, HEIGHT, tile_height):
        for x in range(0, WIDTH, tile_width):
            screen.blit(ground, (x, y + ground_y))

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    keys = pygame.key.get_pressed()
    skier.move(keys)

    
    obstacles.update()
    obstacles.draw(screen)

    
    if distance > 500:
        yeti.update()
        yeti.draw(screen)

   
    skier.draw(screen)

    distance += 1

   
    score_text = font.render(f"Distância: {distance}", True, BLACK)
    screen.blit(score_text, (10, 10))

    
    for obj in obstacles.obstacles:
        reduced_skier_rect = skier.rect.inflate(-10, -10)  
        reduced_obj_rect = obj["rect"].inflate(-10, -10)  
        
        if reduced_skier_rect.colliderect(reduced_obj_rect):
            print("Você bateu em um obstáculo!")
            running = False

    reduced_yeti_rect = yeti.rect.inflate(-10, -10)  
    if reduced_skier_rect.colliderect(reduced_yeti_rect):
        print("O monstro pegou você!")
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
