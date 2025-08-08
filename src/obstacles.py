from settings import *

pygame.init()
pygame.display.set_caption("GRAD-Survivor")
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

map = pygame.image.load('assets/images/mapa1.0.png')

#Daqui pra cima morre!

class Obstaculos:
    def __init__(self, obstaculos):
        self.parede1 = pygame.Rect((0, 0, 4, 600))
        self.parede2 = pygame.Rect((796, 0, 4, 600))
        self.parede3 = pygame.Rect((0, 0, 800, 4))
        self.parede4 = pygame.Rect((0, 595, 800, 4))

        self.porta1 = pygame.Rect((0, 56, 57, 3))
        self.macaneta1 = pygame.Rect((40, 51, 12, 5))

        self.porta2 = pygame.Rect((743, 53, 53, 3))
        self.macaneta2 = pygame.Rect((746, 48, 12, 5))

        self.porta3 = pygame.Rect((0, 493, 55, 3))
        self.macaneta3 = pygame.Rect((40, 488, 12, 5))

        self.porta4 = pygame.Rect((744, 492, 55, 3))
        self.macaneta4 = pygame.Rect((747, 487, 12, 5))

        self.mesa1 = pygame.Rect((0, 369, 186, 82))
        self.mesa2 = pygame.Rect((0, 173, 186, 80))
        self.mesa3 = pygame.Rect((619, 169, 185, 80))
        self.mesa4 = pygame.Rect((619, 374, 185, 81))
        self.mesa5 = pygame.Rect((464, 33, 88, 52))

        self.tv = pygame.Rect((308, 4, 185, 4))


    def obstaculos(self):

        return (self.parede1, self.parede2, self.parede3, self.parede4, self.porta1, self.porta2, self.porta3, self.porta4, self.macaneta1, self.macaneta2, self.macaneta3, self.macaneta4, self.mesa1, self.mesa2, self.mesa3, self.mesa4, self.mesa5, self.tv)
    
        

#Daqui pra baixo some


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

    for obstaculo in Obstaculos(None).obstaculos():
        if player.colliderect(obstaculo):
            player.x = prev_x
            player.y = prev_y

    screen.blit(map, (0, 0))  # desenha o mapa no fundo
    pygame.draw.rect(screen, (0, 0, 255), player)  # desenha o jogador

    pygame.display.flip()
    clock.tick(60)