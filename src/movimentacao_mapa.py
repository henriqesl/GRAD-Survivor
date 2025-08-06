import pygame
import sys

pygame.init()
pygame.display.set_caption("GRAD-Survivor")
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
map = pygame.image.load('assets/images/mapa1.0.png')

# Definindo os retângulos de contato
parede1 = pygame.Rect((0, 0, 4, 600))
parede2 = pygame.Rect((796, 0, 4, 600))
parede3 = pygame.Rect((0, 0, 800, 4))
parede4 = pygame.Rect((0, 595, 800, 4))

porta1 = pygame.Rect((0, 56, 57, 3))
macaneta1 = pygame.Rect((40, 51, 12, 5))

porta2 = pygame.Rect((743, 53, 53, 3))
macaneta2 = pygame.Rect((746, 48, 12, 5))

porta3 = pygame.Rect((0, 493, 55, 3))
macaneta3 = pygame.Rect((40, 488, 12, 5))

porta4 = pygame.Rect((744, 492, 55, 3))
macaneta4 = pygame.Rect((747, 487, 12, 5))

mesa1 = pygame.Rect((0, 370, 185, 80))
mesa2 = pygame.Rect((0, 173, 185, 80))
mesa3 = pygame.Rect((620, 169, 185, 80))
mesa4 = pygame.Rect((620, 375, 185, 80))
mesa5 = pygame.Rect((464, 33, 88, 52))

tv = pygame.Rect((308, 4, 185, 4))


obstaculos = [parede1, parede2, parede3, parede4, porta1, porta2, porta3, porta4, macaneta1, macaneta2, macaneta3, macaneta4, mesa1, mesa2, mesa3, mesa4, mesa5, tv]


# ====== JOGADOR (RETÂNGULO AZUL) ======
player = pygame.Rect(100, 100, 30, 30)  # (x, y, largura, altura)
velocidade = 5

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    prev_x = player.x
    prev_y = player.y

    # Movimento
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= velocidade
    if keys[pygame.K_RIGHT]:
        player.x += velocidade
    if keys[pygame.K_UP]:
        player.y -= velocidade
    if keys[pygame.K_DOWN]:
        player.y += velocidade

    for obstaculo in obstaculos:
        if player.colliderect(obstaculo):
            print(f'Colisão no obstáculo: {obstaculo}')
            player.x = prev_x
            player.y = prev_y

    screen.blit(map, (0, 0))  # desenha o mapa no fundo
    pygame.draw.rect(screen, (0, 0, 255), player)  # desenha o jogador

    pygame.display.flip()
    clock.tick(60)