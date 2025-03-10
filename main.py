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
obstacles = Obstacle()  # Criar um único objeto de Obstacles que gerencia todos os obstáculos
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
    obstacles.update()
    obstacles.draw(screen)

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
    for obj in obstacles.obstacles:  # Corrigindo a iteração sobre os obstáculos
        if skier.rect.colliderect(obj["rect"]):
            print("Você bateu em um obstáculo!")
            running = False

    if skier.rect.colliderect(yeti.rect):
        print("O monstro pegou você!")
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()