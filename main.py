import pygame
from settings import WIDTH, HEIGHT, WHITE, BLACK, FPS
from skier import Skier
from obstacle import Obstacle
from yeti import Yeti


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SkiFree Clone")


font = pygame.font.SysFont(None, 36)

skier = Skier()
obstacles = [Obstacle() for _ in range(10)]
yeti = Yeti()


running = True
clock = pygame.time.Clock()
distance = 0

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    skier.move(keys)

    # Atualizar obstáculos
    for obstacle in obstacles:
        obstacle.update()
        obstacle.draw(screen)

    # Atualizar monstro
    if distance > 500:
        yeti.update()
        yeti.draw(screen)

    # Desenhar o esquiador
    skier.draw(screen)

    # Atualizar distância
    distance += 1

    # Exibir o placar
    score_text = font.render(f"Distância: {distance}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Verificar colisões
    for obstacle in obstacles:
        if skier.rect.colliderect(obstacle.rect):
            print("Você bateu em um obstáculo!")
            running = False

    if skier.rect.colliderect(yeti.rect):
        print("O monstro pegou você!")
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
