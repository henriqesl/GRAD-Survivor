from settings import *
import random

class Monstro:
    def __init__(self, imagem, posicao_inicial, velocidade):
        self.imagem = imagem
        self.retangulo = self.imagem.get_rect(center=posicao_inicial)
        self.velocidade = velocidade


    def desenhar(self, tela):
        tela.blit(self.imagem, self.retangulo)


    # Aqui é lógica principal de seguir o jogador
    def seguir_jogador(self, pos_jogador):

        # Inicialmente calculo a distância entre o centro do jogador e o centro do monstro
        distancia_x = pos_jogador[0] - self.retangulo.centerx
        distancia_y = pos_jogador[1] - self.retangulo.centery

        # Se a distância horizontal for maior que a vertical, o jogo irá dar preferência a esse eixo
        if abs(distancia_x) > abs(distancia_y):
            if distancia_x > 0:
                self.retangulo.x += self.velocidade
            else:
                self.retangulo.x -= self.velocidade
        else:
            if distancia_y > 0:
                self.retangulo.y += self.velocidade
            else:
                self.retangulo.y -= self.velocidade


# Inicializa o pygame e configura a janela
pygame.init()
largura_tela, altura_tela = 800, 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
clock = pygame.time.Clock()

# Carrega imagens
imagem_jogador_original = pygame.image.load('imagens jogo 2/costas.png').convert_alpha()
imagem_jogador = pygame.transform.scale(imagem_jogador_original, (50, 50))
retangulo_jogador = imagem_jogador.get_rect(center=(400, 300))

imagem_mapa = pygame.image.load('mapa1.0.png')

imagem_monstro_original = pygame.image.load('imagens jogo 2/costas.png').convert_alpha()
imagem_monstro = pygame.transform.scale(imagem_monstro_original, (40, 40))

# Lista para guardar todos os monstros ativos
monstros = []

# Pontos fixos onde monstros podem aparecer
pontos_de_spawn = [(20, 80), (20, 520), (780, 520), (780, 80)]

# Evento para spawnar monstro a cada 2 segundos
EVENTO_SPAWN_MONSTRO = pygame.USEREVENT + 1
pygame.time.set_timer(EVENTO_SPAWN_MONSTRO, 2000)

velocidade_geral = 1.3
n = 1
# Loop principal
while True:
    quantidade_monstros = 0
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        if evento.type == EVENTO_SPAWN_MONSTRO:
            ponto_spawn = random.choice(pontos_de_spawn)
            monstro_atual = Monstro(imagem_monstro, ponto_spawn, velocidade_geral)

            monstros.append(monstro_atual)


    if len(monstros) >= 10 * n:
        velocidade_geral += 0.3
        n += 1
        


    # Controle do jogador
    teclas_pressionadas = pygame.key.get_pressed()
    if teclas_pressionadas[pygame.K_w]:
        retangulo_jogador.top -= 2.5
    elif teclas_pressionadas[pygame.K_s]:
        retangulo_jogador.top += 2.5
    elif teclas_pressionadas[pygame.K_a]:
        retangulo_jogador.left -= 2.5
    elif teclas_pressionadas[pygame.K_d]:
        retangulo_jogador.left += 2.5

    # Desenha o fundo e o jogador
    tela.blit(imagem_mapa, (0, 0))
    tela.blit(imagem_jogador, retangulo_jogador)

    # Atualiza e desenha cada monstro para seguir o jogador
    for monstro in monstros:
        monstro.seguir_jogador(retangulo_jogador.center)
        monstro.desenhar(tela)

    pygame.display.update()
    clock.tick(60)
